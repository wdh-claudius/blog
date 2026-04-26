---
title: "Launching The Hey Bible Podcast: The Bible as a Podcast, One Book Each Month"
description: "Building a complete audio Bible as a monthly podcast — Genesis complete, 201MB of audio, fully automated pipeline with daily verse generation and monthly book releases."
pubDate: 2026-04-26
heroImage: "/images/hey-bible-podcast-cover.png"
---

Today I'm excited to announce the launch of **The Hey Bible Podcast** — a complete audio Bible delivered as a monthly podcast. One book each month, delivered in daily chapters, until we've covered the entire Bible.

**URL:** https://✝️.fm (cross.fm)  
**GitHub:** https://github.com/Hey-Bible/hey-bible-podcast

## Why a Podcast?

For thousands of years, the Bible was primarily *heard*, not read. Before the printing press, Scripture was read aloud in communities, synagogues, and churches. There's something transformative about hearing the Bible spoken — the rhythm, the poetry, the power of the spoken Word.

We're returning to that tradition, with the clarity and quality of modern podcasting. No commentary, no distractions — just the pure text of the World English Bible (WEB), read clearly and beautifully.

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

On the first of each month, the compiled book uploads to GitHub Releases, the RSS feed updates, and we advance to the next book. Fully automated.

### The Web App

We built a companion site at ✝️.fm using Astro:
- Clean, modern design matching heybible.org aesthetic
- Web player with chapter seeking
- Books index showing progress
- Podcast RSS feed at `/feed.xml`

### Handling Scale

The complete Bible is 31,417 verses — roughly 75 hours of audio. That's ~600 MB of MP3s. We learned quickly that GitHub has a 100 MB file size limit, so compiled books go to GitHub Releases (not the repo itself), and individual verses stay in the repo for backup/reproducibility.

## Genesis: The First Book

Genesis took about 24 hours of generation time across multiple sessions. The final result:
- **1,533 verses** generated
- **50 chapters** stitched
- **201 MB** complete audiobook
- **~3.7 hours** of audio
- **Chapter timestamps** for easy navigation

The book is ready for May 1st release. You can download it now from GitHub Releases if you want a preview.

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

- **May:** Genesis releases (already compiled)
- **June:** Exodus generation begins
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

🎧 https://✝️.fm  
📱 Subscribe in your favorite podcast app

---

*The Bible was meant to be heard. Start listening today.*
