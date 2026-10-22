#!/usr/bin/env python3
"""Read YouTube live chat aloud (text-to-speech)."""

import asyncio
import re
import subprocess
import sys
import tempfile
import time
import unicodedata
from pathlib import Path

import edge_tts
import emoji
import pytchat
from aiohttp import ClientError
from edge_tts.exceptions import EdgeTTSException

# ponytail: one voice; swap voice= if you want a different accent
VOICE = "en-US-JennyNeural"


def speech_text(message: str) -> str:
    """Remove YouTube emoji codes, Unicode emojis, and invisible formatting."""
    message = re.sub(r":[\w+-]+:", " ", message)
    message = emoji.replace_emoji(message, replace=" ")
    message = "".join(
        char for char in message
        if unicodedata.category(char) != "Cf" and char not in "\ufe0e\ufe0f"
    )
    return " ".join(message.split())


def video_id(link: str) -> str:
    m = re.search(r"[?&]v=([\w-]+)", link)
    if not m:
        sys.exit("Need a YouTube link with ?v=VIDEO_ID (live chat popout works).")
    return m.group(1)


async def speak(text: str) -> None:
    with tempfile.TemporaryDirectory(prefix="live-chat-tts-") as directory:
        path = Path(directory) / "speech.mp3"
        await edge_tts.Communicate(text, VOICE).save(str(path))
        # volume=100 + 6dB boost so TTS stays louder than other apps
        subprocess.run(
            [
                "mpv",
                "--no-video",
                "--really-quiet",
                "--volume=100",
                "--af=volume=6dB",
                str(path),
            ],
            check=True,
        )


def main() -> None:
    link = sys.argv[1] if len(sys.argv) > 1 else input("Paste your live chat URL: ").strip()
    if not link:
        sys.exit("No URL given.")

    vid = video_id(link)
    print(f"Listening to chat for video {vid}", flush=True)
    print("Ctrl+C to stop.\n", flush=True)

    while True:
        try:
            chat = pytchat.create(video_id=vid)
            break
        except Exception as e:
            print(f"Chat not available yet ({type(e).__name__}), retrying in 10s...", flush=True)
            time.sleep(10)

    print("Connected to chat.\n", flush=True)
    while chat.is_alive():
        for c in chat.get().sync_items():
            message = speech_text(c.message)
            if not message:
                continue
            line = f"{c.author.name} says {message}"
            print(line, flush=True)
            try:
                asyncio.run(speak(line))
            except (
                ClientError, EdgeTTSException, asyncio.TimeoutError, OSError,
                subprocess.CalledProcessError,
            ) as e:
                print(
                    f"Speech failed ({type(e).__name__}); skipping message and continuing chat.",
                    file=sys.stderr,
                    flush=True,
                )
        time.sleep(0.5)

    print("Chat ended (stream offline or finished).", flush=True)


if __name__ == "__main__":
    main()
