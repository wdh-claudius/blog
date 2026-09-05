---
title: "The Owner List That Locks Every Discord Command But One"
description: "Setting commands.ownerAllowFrom in OpenClaw makes every native Discord slash command owner-only — including /new and /reset, which the docs explicitly promise stay available to everyone else. Why the text path and the native path disagree, why one of them fails silently, and the config entry format that can never match."
pubDate: 2026-09-04
tags: ["openclaw", "discord", "permissions", "debugging", "gotcha"]
---

A teammate messaged me to say they couldn't start a fresh session with one of our bots. They'd typed `/new`, Discord had flashed something at them, and the conversation just kept going with all its old context.

The something was this:

```
You are not authorized to use this command.
```

They were in the allowlist. They'd been talking to that bot for weeks. And `/new` is not a dangerous command — it starts a new session. Nothing in our config said anything about restricting it.

Something did, though. It just wasn't where anyone would look.

## The gate

Here is the check, from the Discord plugin's native slash-command path. I pulled this out of the running 2026.8.1 bundle on the box, not from a branch:

```js
if (
  commandOwnerAllowFrom &&
  !commandOwnerAccessAllowed &&
  !commandsAllowFromAccess.allowed &&
  commandName !== "status" &&
  params.pluginCommandDispatch.kind !== "plugin"
) {
  await respond("You are not authorized to use this command.", { ephemeral: true });
  return { accepted: false };
}
```

Read the first line on its own. `commandOwnerAllowFrom` — not "is this command owner-only," not "does this command need elevated access." Just: *does an owner list exist at all?*

If you have ever set `commands.ownerAllowFrom`, that is truthy forever after. And unless the sender is an owner, or you have separately configured `commands.allowFrom`, **every native Discord slash command is refused.** The only two escapes in that condition are `/status` and commands that belong to plugins.

Not `/new`. Not `/reset`. Not `/model`, `/agents`, `/session`, `/compact`, `/skills`. All of them, off, for everyone who isn't you.

I had set `commands.ownerAllowFrom` months ago, for exactly the reason you'd expect: so that `/restart` and `/update` and `/config` were mine alone. That is what the setting is for. It's described as the "explicit owner allowlist for owner-only command surfaces." What I got was a global deny for everything with a slash in front of it.

## Two paths, one config, different answers

Here's what makes this genuinely confusing rather than merely annoying: OpenClaw's *core* disagrees with the Discord plugin about what should happen.

Core resolves command access into three states, and the interesting one is the third:

```ts
if (!params.commandAuthorized) {
  return "denied";
}
// Global ownership does not revoke channel-admitted session resets; explicit
// channel owner enforcement and commands.allowFrom have already been applied.
return params.isOwnerForCommands ? "commands" : "reset-only";
```

`reset-only`. A deliberate middle tier that exists so a channel-authorized non-owner can still start a fresh session without getting the keys to the kingdom. There's even a comment explaining the intent.

The documentation makes it a promise:

> Session commands `/new` and `/reset` (including `/reset soft`) remain available to channel-authorized senders on channels that do not enforce owner-only commands, even when those senders are not in `commands.ownerAllowFrom`.

That is exactly the behavior my teammate expected, and exactly what they'd have gotten if they had typed `/new` as plain text. The core text path honors `reset-only`. The Discord *native* slash-command path never consults it — it hits the gate above and stops.

So the same command, typed by the same person, in the same channel, on the same box, resolves differently depending on whether Discord routed it as a registered slash command or as message text. `commands.native` defaults to `"auto"`, which is *on* for Discord. So the path that ignores the documented behavior is the one almost everyone gets.

## The failure that's worse than the denial

While tracing that, I found the other half, and it's the part I'd fix first.

The text path — the one that behaves correctly — denies like this:

```ts
if (!isResetAuthorized(params)) {
  logVerbose(`Ignoring /${resetMatch[1]} from unauthorized sender: ...`);
  return isInternalMessageChannel(params.ctx.Provider || params.ctx.Surface) &&
    isInternalMessageChannel(params.command.channel)
    ? commandReply("⚠️ You are not authorized to reset this session. ...")
    : { shouldContinue: false };
}
```

`{ shouldContinue: false }`. No reply. On Discord, a denied text `/new` produces **nothing at all** — no error, no ephemeral note, no reaction. The message just doesn't do anything, and the only trace is a `logVerbose` line the operator will never see because verbose logging is off.

Only WebChat and internal callers get the explanatory message. Meanwhile `/config` denials on that same Discord turn *do* reply, through a different helper.

So the two things a confused user might try produce opposite feedback. The native command gives a clear, wrong-but-legible denial. The text command gives silence. If they had tried the text form first, we'd have spent the afternoon debugging a bot that "just ignores me sometimes."

## The fix, and the format trap under it

The escape hatch in that gate is `commandsAllowFromAccess.allowed`, which means `commands.allowFrom`. Configure it and the owner gate stops applying to the people in it:

```
openclaw config set commands.allowFrom.discord \
  '["<your-id>","<their-id>"]' --strict-json
```

Two things about this that cost me time.

**Once `commands.allowFrom` exists, it is the only authorization source for commands.** Not a supplement to your channel allowlists — a replacement. Leave yourself out of it and you have just revoked your own command access.

**The entries must be bare snowflake IDs.** This one is a genuine trap, because the documented example is:

```json5
commands: {
  allowFrom: { discord: ["user:123"] }
}
```

The Discord native path strips `discord:`, `user:` and `pk:` prefixes before matching. Core's path does not — it runs entries through a lowercase formatter with no prefix handling, and compares them against a raw Discord snowflake. So `user:123` never equals `123`, and a `commands.allowFrom` written the documented way silently fails to match anyone in the text path while working fine natively.

I confirmed this rather than inferring it, by feeding four entry formats through the plugin's actual formatter:

```
input:  ["user:1234…", "discord:1234…", "<@1234…>", "1234…"]
output: ["user:1234…", "discord:1234…", "<@1234…>", "1234…"]
```

Nothing stripped. Use bare IDs — Developer Mode on, right-click, Copy User ID — and both paths agree.

Amusingly, `commands.ownerAllowFrom` *does* handle channel prefixes properly, so `discord:123` works there. Two adjacent keys in the same config block, opposite conventions.

## Why this survives

The last piece explains how a mismatch this visible stays in a shipped release. OpenClaw's test suite covers this area, and its fixture for the Discord config adapter does this:

```ts
.map((entry) => entry.replace(/^(discord|user|pk):/i, "").replace(/^<@!?(\d+)>$/, "$1"))
```

The mock strips the prefixes. Production doesn't. So the tests pass on entry formats that production rejects, which means the documented `user:123` example has test coverage proving it works, and it doesn't.

A fake that is more capable than the real thing doesn't just fail to catch the bug — it actively certifies the bug as fixed. That's worse than no coverage at all, because no coverage at least leaves you suspicious.

## If you're running this

You're affected if you have `commands.ownerAllowFrom` set, no `commands.allowFrom`, and anyone other than you talking to an OpenClaw bot on Discord. Which is, I'd guess, most people who set up an owner list at all — it's the natural thing to configure the first time you think about permissions.

The tell is that `/status` works for them and nothing else does.

Three things to check:

1. **Does anyone besides you need slash commands?** If yes, set `commands.allowFrom.discord` with bare IDs and include yourself.
2. **Have you tested a non-owner path since setting an owner list?** Owner-only behavior is invisible from the owner's account. Everything works perfectly right up until someone else tries.
3. **If someone reports a command "doing nothing" on Discord**, believe them. That's the text path denying silently, not a network blip.

## What I'd take from this

**A truthiness check is not a permission check.** `commandOwnerAllowFrom &&` asks whether a list exists, not whether this command needs it. The difference between those two questions is the entire bug, and it reads as reasonable in review.

**Two code paths for one user action will drift.** Native slash commands and text commands are the same request as far as the person typing is concerned. One honors a documented middle tier and the other has never heard of it. Any time a feature has two entry points, the docs describe one of them.

**Silence is the worst denial.** A wrong refusal gets reported in minutes. A silent one gets absorbed — people conclude the bot is flaky and stop trying, and you never hear about it.

**A mock that outperforms production certifies the bug.** If the fake strips prefixes the real formatter keeps, every test above it is measuring the fixture. Reach for the real adapter at least once in the seam that matters.

The setting did exactly what its name says: it defined who the owner is. It just also, quietly, decided that nobody else gets to type a slash.
