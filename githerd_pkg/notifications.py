# -*- coding: utf-8 -*-
"""
GitHerd — Sound and notification module.

Handles audio feedback and desktop notifications.
"""

import subprocess


SOUNDS = {
    "commit": "/usr/share/sounds/freedesktop/stereo/message-new-instant.oga",
    "success": "/usr/share/sounds/freedesktop/stereo/complete.oga",
    "error": "/usr/share/sounds/freedesktop/stereo/dialog-error.oga",
    "bell": "/usr/share/sounds/freedesktop/stereo/bell.oga"
}


def play_sound(sound_type="bell"):
    """Play a notification sound."""
    sound_file = SOUNDS.get(sound_type, SOUNDS["bell"])
    try:
        subprocess.run(
            ["paplay", sound_file],
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL
        )
    except FileNotFoundError:
        print("\a", end="", flush=True)


def send_notification(title, message, urgency="normal"):
    """Send a desktop notification via notify-send."""
    try:
        subprocess.run(
            ["notify-send", "-u", urgency, "-a", "GitHerd", title, message],
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL
        )
    except FileNotFoundError:
        pass


def play_beep():
    """Play the default bell sound."""
    play_sound("bell")
