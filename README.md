# Live Chat TTS

Listen to YouTube live chat instead of reading it. Paste a live chat link, and this tool reads messages aloud while you watch the stream.

For example, if someone named Alex sends `Hello!`, you will hear **“Alex says Hello!”**

## What it does

- Reads the sender's name and their message aloud.
- Skips emojis such as 😆 and emoji codes such as `:grinning_squinting_face:`.
- Stays silent when a message contains only emojis.
- Keeps listening if one message cannot be read aloud.
- Tries again every 10 seconds if it cannot connect to the chat at startup.

You need an internet connection and a YouTube stream with live chat available. Speech is generated using Microsoft's online text-to-speech service, so the text being spoken is sent to that service. No API key is needed.

## Before you start

This project has been used on Linux with Python 3.10. Instructions for macOS and Windows are also included, but have not been tested here.

You will use a **terminal**: an app where you type commands. Open Terminal on Linux or macOS, or PowerShell on Windows. Copy commands one line at a time and press Enter after each line.

You need two programs:

- **Python 3.10 or newer**, which runs this tool.
- **mpv**, which plays the spoken audio.

### Install them on Linux

For Ubuntu or Debian:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip mpv
```

For Arch Linux or Omarchy:

```bash
sudo pacman -Syu python python-pip mpv
```

If asked for your computer password, type it and press Enter. It is normal for nothing to appear while you type the password.

### Install them on macOS

Install Python from [python.org](https://www.python.org/downloads/). Install mpv using one of the options on the [mpv installation page](https://mpv.io/installation/). If you already use Homebrew, you can run `brew install mpv`.

### Install them on Windows

Install Python from [python.org](https://www.python.org/downloads/). Install mpv using one of the Windows options on the [mpv installation page](https://mpv.io/installation/).

The folder containing `mpv.exe` must be in your **Path**, the list of folders Windows searches for programs. Search the Start menu for “Edit environment variables for your account”, open **Path → Edit → New**, and add that folder. Close and reopen PowerShell afterward.

Run `python --version` and `mpv --version` in PowerShell to check that both programs are available. Python should report version 3.10 or newer.

## Download this project

1. Open [this project's GitHub page](https://github.com/anupPradhan0/live-chat-tts).
2. Click the green **Code** button, then **Download ZIP**.
3. Extract the ZIP file. You should get a folder called `live-chat-tts-main`.
4. Open that folder in your file manager, then open a terminal there. On many Linux desktops, right-click inside the folder and choose **Open in Terminal**. On Windows, right-click and choose **Open in Terminal**. On macOS, right-click the folder and look under **Services → New Terminal at Folder**.

The terminal must be inside the folder containing `main.py` and `requirements.txt` before you run the next commands.

## First-time setup

These commands create a separate folder for the tool's Python packages and install what it needs. You only need to do this once.

**Linux or macOS:**

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Start listening

From the project folder, run:

**Linux or macOS:**

```bash
.venv/bin/python main.py
```

**Windows PowerShell:**

```powershell
.\.venv\Scripts\python.exe main.py
```

When you see `Paste your live chat URL:`, paste the YouTube link and press Enter.

You can use the full stream link from your browser's address bar, such as `https://www.youtube.com/watch?v=VIDEO_ID`, or a pop-out chat link such as `https://www.youtube.com/live_chat?is_popout=1&v=VIDEO_ID`. Use your stream's actual link; `VIDEO_ID` is only an example. The link must contain `v=`. Short `youtu.be` links and `/live/` links are not supported directly.

Wait for **Connected to chat.** New text messages will then be read aloud. Keep the terminal open while listening. Press **Ctrl+C** to stop.

Next time, open the project folder in a terminal and run the same start command. You do not need to repeat the installation.

## If something goes wrong

- **No sound:** Check your speakers, headphones, and system volume. Emoji-only messages are intentionally silent.
- **“mpv” cannot be found:** Install mpv and check that `mpv --version` works in your terminal.
- **“Need a YouTube link with ?v=VIDEO_ID”:** Use a full `watch?v=...` or pop-out chat link as shown above.
- **“Chat not available yet”:** Check that the stream is live and has chat enabled. The tool will keep trying; press Ctrl+C to stop it.
- **“Speech failed”:** That message was skipped. Check your internet connection. If this keeps happening, update the Python packages using the command below, then restart the tool.

To update the packages on **Linux or macOS**:

```bash
.venv/bin/python -m pip install --upgrade -r requirements.txt
```

On **Windows PowerShell**:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade -r requirements.txt
```

Messages are read one at a time, so speech can fall behind in a very busy chat.
