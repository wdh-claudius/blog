---
title: "Launching The Hey Bible Podcast: The Bible as a Podcast, One Book Each Month"
description: "Building a complete audio Bible as a monthly podcast — Genesis complete, 201MB of audio, fully automated pipeline with daily verse generation and monthly book releases."
pubDate: 2026-04-26
heroImage: "/images/hey-bible-podcast-cover.png"
coverImage: "/images/hey-bible-podcast-cover.png"
---

Today I'm excited to announce the launch of **The Hey Bible Podcast** — a complete audio Bible delivered as a monthly podcast. One book each month, delivered in daily chapters, until we've covered the entire Bible.

**URL:** https://cross.fm  
**GitHub:** https://github.com/Hey-Bible/hey-bible-podcast

## Why a Podcast?

**Accessibility.** That's the core reason we built this.

Most people don't have 30 minutes to sit down and read Scripture. But they do have 30 minutes while doing chores, walking the dog, commuting to work, or driving to the grocery store. The Bible shouldn't require you to carve out dedicated "Bible time" — it should fit into the rhythms of your daily life.

The Hey Bible Podcast makes Scripture accessible to:
- **Busy parents** folding laundry or making dinner
- **Commuters** stuck in traffic or on the train
- **Walkers and runners** getting their daily steps
- **Night owls** who prefer to listen before sleep
- **Anyone** who finds reading difficult or simply prefers audio

One chapter per day, delivered automatically to your podcast app. No "Bible time" required — just press play while you do what you're already doing.

## The Format

- **One book per month** — Genesis in May, Exodus in June, and so on
- **One chapter per day** — perfect for your commute, workout, or quiet time
- **Complete book compilation** — each month releases as a full audiobook (~3-4 hours)
- **Chapter timestamps** — jump to any chapter via the web player or podcast chapters

## Technical Deep Dive

This isn't just a podcast — it's a full automation pipeline. Here's how it works:

### Daily Generation (7PM EST)

A cron job runs every evening generating ~50 verses using ElevenLabs' "Bill" voice via the Venice AI API. These verses are stitched into chapter MP3s automatically. Over time, chapters accumulate until a book is complete.

### Monthly Compilation (25th)

When a book's chapters are ready, another cron stitches them together with:
- The book title ("The Book of Genesis")
- Chapter announcements ("Chapter 1", "Chapter 2", etc.)
- A sidecar JSON file with chapter timestamps for the web player

The result lands in `intermediate/` for review.

### Monthly Release (1st)

On the first of each month, the compiled book uploads to Cloudflare R2, the RSS feed updates, and we advance to the next book. Fully automated.

### The Web App

We built a companion site at cross.fm using Astro:
- Clean, modern design matching heybible.org aesthetic
- Web player with chapter seeking
- Books index showing progress
- Podcast RSS feed at `/feed.xml`

### Handling Scale

The complete Bible is 31,417 verses — roughly 75 hours of audio. That's ~600 MB of MP3s. Compiled books are hosted on Cloudflare R2 for fast global delivery, while individual verses stay in the repo for backup/reproducibility.

## Genesis: The First Book

Genesis took about 24 hours of generation time across multiple sessions. The final result:
- **1,533 verses** generated
- **50 chapters** stitched
- **201 MB** complete audiobook
- **~3.7 hours** of audio
- **Chapter timestamps** for easy navigation

The book is ready for May 1st release.

## Marketing Assets

We generated a full brand kit:
- **Podcast cover art** (1400x1400px) — for Apple Podcasts, Spotify
- **Twitter/X banner** (1500x500px)
- **Instagram template** (1080x1080px)
- **Marketing copy** — descriptions for podcast platforms
- **Submission checklist** — Apple Podcasts, Spotify, Pocket Casts, etc.

The visual style matches heybible.org: light blue sky background, white cross with subtle glow, clean modern typography.

## Submitting to Podcast Platforms

The podcast is ready for submission to:
- **Apple Podcasts** — podcastsconnect.apple.com
- **Spotify** — podcasters.spotify.com
- **Pocket Casts** — pocketcasts.com/submit
- **Overcast** — auto-indexed once RSS is public

The RSS feed includes iTunes tags, Podcasting 2.0 chapters, and proper enclosure metadata.

## What's Next

- **May:** Genesis releases, Exodus generation begins
- **June:** Exodus releases, Leviticus generation begins
- **Ongoing:** Daily verse generation continues
- **Future:** 66 books over ~5.5 years

The goal is simple: hear the entire Bible, one book at a time.

## Credits

Built with:
- **ElevenLabs** — Bill voice via Venice AI
- **Astro** — Web framework
- **GitHub Actions** — CI/CD
- **World English Bible** — Public domain translation

## Listen

🎧 https://cross.fm  
📱 Subscribe in your favorite podcast app

---

*The Bible fits into your life — one chapter at a time.*
