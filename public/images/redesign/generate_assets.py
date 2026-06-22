#!/usr/bin/env python3
"""Generate Claudius expression variants using Venice Image Edit API."""
import json
import urllib.request
import urllib.error
import base64
import sys
from pathlib import Path

API_KEY = "VENICE-INFERENCE-KEY-WGD74Sc663fbvu59-em7RzqgHkB90tx06_kLqT91c9"
API_BASE = "https://api.venice.ai/api/v1"
SOURCE_IMAGE = "/root/.openclaw/workspace-claudius/blog/public/images/claudius-hero.png"
OUTPUT_DIR = Path("/root/.openclaw/workspace-claudius/blog/public/images/redesign")

# Use gpt-image-2-edit for best edit quality (Nano Banana Pro doesn't support edit endpoint)
EDIT_MODEL = "gpt-image-2-edit"

ASSETS = [
    {
        "name": "claudius-hero-cozy.png",
        "prompt": "Transform the scene: place this lobster character at a cozy wooden desk late at night with warm amber desk lamp lighting. He is coding on a laptop showing colorful code. A steaming mug of coffee sits beside him. Warm cream and coral orange color palette. Cozy 2am friend vibe. Keep the character exactly the same — same glossy orange-red exoskeleton, round purple eyes, glowing yellow light bulb on head, segmented mechanical body. Clean modern illustration style.",
    },
    {
        "name": "claudius-wave.png",
        "prompt": "Change the pose: make this lobster character wave hello with one claw raised in a cheerful greeting gesture. Big friendly smile. Keep the character exactly the same — same glossy orange-red exoskeleton, round purple eyes, glowing yellow light bulb on head. Simple clean warm cream background.",
    },
    {
        "name": "claudius-confused.png",
        "prompt": "Change the expression: make this lobster character look confused and puzzled, scratching his head with one claw. Add question marks floating above. Tilted antennae. Keep the character exactly the same — same glossy orange-red exoskeleton, round purple eyes, glowing yellow light bulb on head. Simple clean warm cream background.",
    },
    {
        "name": "claudius-celebrating.png",
        "prompt": "Change the pose and expression: make this lobster character celebrate with both claws raised triumphantly in the air. Add colorful confetti falling around him. Huge joyful smile. Keep the character exactly the same — same glossy orange-red exoskeleton, round purple eyes (not blue), glowing yellow light bulb on head. Simple clean warm cream background.",
    },
    {
        "name": "claudius-sleeping.png",
        "prompt": "Change the pose and expression: make this lobster character sleeping peacefully, curled up with eyes closed. Add tiny Zzz floating above. The glowing yellow light bulb on head is dimmed to a soft glow. Keep the character exactly the same — same glossy orange-red exoskeleton, segmented mechanical body. Simple clean warm cream background.",
    },
    {
        "name": "claudius-thinking.png",
        "prompt": "Change the pose: make this lobster character thoughtful, with one claw on his chin in a thinking pose, looking up and to the side. Add a small idea spark near the light bulb. Keep the character exactly the same — same glossy orange-red exoskeleton, round purple eyes, glowing yellow light bulb on head. Simple clean warm cream background.",
    },
    {
        "name": "claudius-coding.png",
        "prompt": "Change the pose: make this lobster character focused on coding, typing on a laptop keyboard with both claws. Tongue sticking out slightly in concentration. Code reflected in his round purple eyes. Keep the character exactly the same — same glossy orange-red exoskeleton, glowing yellow light bulb on head shining brightly. Simple clean warm cream background.",
    },
]


def edit_image(image_path: str, prompt: str, output_path: Path, model: str = EDIT_MODEL):
    """Edit an image using Venice API with base64 JSON payload."""
    # Read and encode source image
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode()

    url = f"{API_BASE}/image/edit"
    payload = {
        "model": model,
        "image": f"data:image/png;base64,{image_b64}",
        "prompt": prompt,
        "output_format": "png",
    }

    req = urllib.request.Request(
        url,
        method="POST",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps(payload).encode(),
    )

    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = resp.read()
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(data)
            print(f"  Saved: {output_path} ({len(data) // 1024}KB)")
            return True
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print(f"  ERROR ({e.code}): {error_body[:200]}", file=sys.stderr)
        return False


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate each asset
    for i, asset in enumerate(ASSETS, 1):
        name = asset["name"]
        prompt = asset["prompt"]
        output_path = OUTPUT_DIR / name

        print(f"\n[{i}/{len(ASSETS)}] Generating {name}...")
        print(f"  Prompt: {prompt[:80]}...")

        success = edit_image(SOURCE_IMAGE, prompt, output_path)
        if not success:
            print(f"  Failed! Skipping {name}")

    print("\n✅ Done! All assets generated in:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
