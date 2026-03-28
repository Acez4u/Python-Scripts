#!/usr/bin/env python3
import os
import sys
import random
import time
from datetime import datetime

try:
    from pyfiglet import Figlet
except ImportError:
    Figlet = None

APP_TITLE = "Name Art Gen"
APP_VERSION = "1.0"
DEVELOPER_NAME = "Acez Scripts"

WHITE = "\033[37m"
GREEN = "\033[32m"
CYAN = "\033[36m"
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

TITLE_START = (255, 120, 220)  # pink
TITLE_END = (80, 255, 255)     # cyan

PAGE_SIZE = 20
RESULT_COUNT = 50

FONT_POOL = [
    "slant", "big", "block", "banner", "3-d", "standard", "shadow", "bubble",
    "digital", "mini", "small", "script", "univers", "stop", "lean", "mnemonic",
    "marquee", "puffy", "rectangles", "doom", "crazy", "colossal", "cyberlarge",
    "eftiwater", "isometric1", "poison", "roman", "speed", "starwars", "graceful",
    "whimsy", "chunky", "thin", "avatar", "bell", "contrast", "cricket", "tengwar",
    "merlin", "tombstone", "isometric2", "isometric3", "isometric4", "larry3d",
    "oogie", "pawp", "sweet", "lefttoright", "righttoleft", "epic", "bulbhead",
    "acrobatic", "cosmic", "double", "fuzzy", "goofy", "tinker-toy", "invita",
    "jazmine",
]


def clear():
    os.system("clear" if os.name != "nt" else "cls")


def rgb_escape(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"


def sleep_short():
    time.sleep(0.03)


def script_dir():
    return os.path.dirname(os.path.abspath(__file__))


def log_path():
    return os.path.join(script_dir(), "log.txt")


def append_log(text):
    with open(log_path(), "a", encoding="utf-8") as f:
        f.write(text)
        if not text.endswith("\n"):
            f.write("\n")


def render_figlet(text, font_name):
    if Figlet:
        try:
            return Figlet(font=font_name).renderText(text)
        except Exception:
            pass

    width = len(text) + 10
    border = "*" * width
    return f"{border}\n***  {text}  ***\n{border}\n"


def gradient_line(line, start_rgb, end_rgb):
    visible = [ch for ch in line if ch != " "]
    count = max(len(visible) - 1, 1)
    result = []
    visible_index = 0

    for ch in line:
        if ch == " ":
            result.append(ch)
            continue

        t = visible_index / count
        r = round(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * t)
        g = round(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * t)
        b = round(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * t)
        result.append(f"{rgb_escape(r, g, b)}{ch}{RESET}")
        visible_index += 1

    return "".join(result)


def gradient_block(block, start_rgb, end_rgb):
    return "\n".join(gradient_line(line, start_rgb, end_rgb) for line in block.splitlines())


def hacker_noise(width=42):
    chars = "01ABCDEF#$%&@*+=-"
    return "".join(random.choice(chars) for _ in range(width))


def loading_intro():
    clear()
    intro_title = render_figlet(APP_TITLE, "slant")
    intro_title = gradient_block(intro_title, TITLE_START, TITLE_END)
    print(intro_title)
    print(f"{BOLD}{DEVELOPER_NAME}{RESET}  |  v{APP_VERSION}\n")

    boot_lines = [
        "Initializing terminal interface...",
        "Loading ASCII engines...",
        "Calibrating font matrix...",
        "Warming up style generator...",
        "Preparing secure visual layers...",
        "SYSTEM READY",
    ]

    for i, line in enumerate(boot_lines, start=1):
        bar = "[" + "#" * i + "." * (len(boot_lines) - i) + "]"
        print(f"{GREEN}{bar}{RESET} {DIM}{hacker_noise(28)}{RESET}")
        time.sleep(0.15)
        print(f"{CYAN}{line}{RESET}")
        sleep_short()

    print()
    for _ in range(4):
        print(f"{GREEN}{hacker_noise(60)}{RESET}")
        sleep_short()

    print(f"\n{BOLD}{GREEN}ACCESS GRANTED{RESET}\n")
    time.sleep(0.6)


def ask_name():
    placeholder = "Enter your name here"
    while True:
        name = input(f"{placeholder}: ").strip()
        if name:
            return name
        print("Name cannot be empty.")


def build_random_styles():
    styles = FONT_POOL[:]
    random.shuffle(styles)

    selected = []
    seen = set()

    for font_name in styles:
        if font_name not in seen:
            seen.add(font_name)
            selected.append(font_name)
        if len(selected) >= RESULT_COUNT:
            break

    return selected


def show_title():
    title_art = render_figlet(APP_TITLE, "slant")
    title_art = gradient_block(title_art, TITLE_START, TITLE_END)
    print(title_art)
    print(f"{BOLD}Developer: {DEVELOPER_NAME}    Version: {APP_VERSION}{RESET}\n")


def build_page_text(name, styles, start_index, page_size=PAGE_SIZE):
    end_index = min(start_index + page_size, len(styles))
    parts = []

    parts.append(f"{APP_TITLE} v{APP_VERSION}")
    parts.append(f"Developer: {DEVELOPER_NAME}")
    parts.append(f"Name: {name}")
    parts.append(f"Showing results {start_index + 1}-{end_index} of {len(styles)}")
    parts.append("")

    for i in range(start_index, end_index):
        font_name = styles[i]
        art = render_figlet(name, font_name)
        parts.append(f"--- Style {i + 1}: {font_name} ---")
        parts.append(art.rstrip("\n"))
        parts.append("")

    return "\n".join(parts), end_index


def show_page(name, styles, start_index, page_size=PAGE_SIZE):
    page_text, end_index = build_page_text(name, styles, start_index, page_size)

    print(f"{BOLD}Name:{RESET} {name}")
    print(f"{BOLD}Showing results {start_index + 1}-{end_index} of {len(styles)}{RESET}\n")

    for i in range(start_index, end_index):
        font_name = styles[i]
        art = render_figlet(name, font_name)

        print(f"{DIM}--- Style {i + 1}: {font_name} ---{RESET}")
        print(f"{WHITE}{art}{RESET}")
        print()

    return page_text, end_index


def log_design(name, page_text):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = (
        f"\n{'=' * 70}\n"
        f"Saved: {timestamp}\n"
        f"Name: {name}\n"
        f"{'=' * 70}\n"
        f"{page_text}\n"
    )
    append_log(entry)


def art_session(name):
    styles = build_random_styles()
    start_index = 0

    while True:
        clear()
        show_title()

        print(f"{GREEN}{hacker_noise(55)}{RESET}")
        page_text, next_index = show_page(name, styles, start_index, PAGE_SIZE)
        print(f"{GREEN}{hacker_noise(55)}{RESET}\n")

        log_design(name, page_text)

        if next_index >= len(styles):
            choice = input("No more styles left. [M]ain menu or [Q]uit: ").strip().lower()
            if choice == "q":
                print("\nExiting...")
                sys.exit(0)
            return

        print(f"{CYAN}Options: [L]oad more   [M]ain menu   [Q]uit{RESET}")
        choice = input("Choose: ").strip().lower()

        if choice == "l":
            start_index = next_index
            continue
        if choice == "m":
            return
        if choice == "q":
            print("\nExiting...")
            sys.exit(0)

        print("Invalid choice. Returning to main menu...")
        input("Press Enter to continue...")
        return


def main():
    loading_intro()

    while True:
        clear()
        show_title()
        name = ask_name()
        art_session(name)

        clear()
        show_title()
        again = input("Back to main menu? (y/n): ").strip().lower()
        if again != "y":
            print("\nExiting...")
            sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")