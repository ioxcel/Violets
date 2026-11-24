"""Violet's: a terminal toolkit of network, OSINT, forensics and Discord
utilities, each self-contained and run from a paged menu.

Copyright (c) 2026 Matas. All rights reserved.
Unauthorised copying, modification or distribution of this software, in whole
or in part, is prohibited. See the LICENSE file for the full terms.
"""
import functools
import importlib
import os
import random
import re
import shlex
import shutil
import subprocess
import sys
import time
import traceback

WINDOWS = sys.platform == "win32"
MAC = sys.platform == "darwin"

if WINDOWS:
    import ctypes
    import msvcrt
else:
    import select
    import termios
    import tty

sys.dont_write_bytecode = True

FEATURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Violet's Features")
sys.path.insert(0, FEATURES_DIR)

ART = [
    "\033[0;37m        \033[0;97m▄\033[0;37m    \033[0;97m▄▄\033[0;37m▄▄▄\033[0;90m▄▄\033[0;37m     \033[0;97m▄\033[0;37m▄▄▄\033[0;90m▄\033[0;37m      \033[0;97m▄▄\033[0;37m▄▄\033[0;90m▄\033[0;37m     \033[0;97m▄▄\033[0;37m▄▄▄\033[0;90m▄▄▄▄▄\033[0;97m▄▄\033[0;37m▄▄▄\033[0;90m▄▄▄▄▄▄▄\033[0;97m▄▄\033[0;37m▄\033[0;90m▄\033[0;37m   \033[0;97m▄\033[0;37m▄▄\033[0;90m▄▄▄▄▄\033[0;37m  \033[0m",
    "\033[0;37m  \033[0;97m▄\033[0;97;45m▀\033[0;90m█\033[0;37m  \033[0;97m█\033[0;95;45m░\033[0;37;45m▀\033[0;90m▄\033[0;37m \033[0;97m▀\033[0;97;45m▄\033[0;95;45m░▒▒▒▓\033[0;90m█▀\033[0;37m  \033[0;97m▄\033[0;97;45m▀\033[0;95;45m░▒▒▒░\033[0;90;45m▀\033[0;90m▄\033[0;37m  \033[0;97m▄\033[0;97;45m▀\033[0;95;45m░▒█\033[0;90;45m▄\033[0;90m▀\033[0;37m    \033[0;97m▀\033[0;97;45m▄\033[0;95;45m░▒▒▒▓▓▓█\033[0;90;45m▐\033[0;97;45m▌ \033[0;95;45m░░▒▒▒▒▓▓█\033[0;90m▌\033[0;97m█\033[0;95;45m▓▒░\033[0;35m▌\033[0;97m▄\033[0;97;45m▀\033[0;95;45m░▒▒▓▓█▓▒\033[0;90m█▄\033[0m",
    "\033[0;37m \033[0;97m▐\033[0;95;45m░░\033[0;90m█\033[0;37m  ▀\033[0;90;45m▄\033[0;95;45m░░\033[0;90m▌\033[0;37m  \033[0;35;47m▐\033[0;95;45m░▒\033[0;90;45m▄\033[0;90m█\033[0;37m   \033[0;97m▐\033[0;95;45m░░\033[0;90;45m▄\033[0;90m▀▀▀\033[0;90;45m▄\033[0;95;45m░░\033[0;90m▌\033[0;37m  █\033[0;95;45m▒▓▓\033[0;90m▌\033[0;37m       \033[0;35;47m▐\033[0;95;45m░▒\033[0;90;45m▄\033[0;90m▀▀▀\033[0;90;45m▄\033[0;90m█\033[0;37m▀\033[0;90m▀▀▀\033[0;90;45m▌\033[0;95;45m░▒\033[0;90;45m▐\033[0;90m▀▀▀\033[0;37m \033[0;97;47m▌\033[0;95;45m░▒\033[0;35m▌\033[0;37m \033[0;97;45m▌\033[0;95;45m░░\033[0;90;45m▄\033[0;90m▀▀▀▀▀█▀\033[0;37m \033[0m",
    "\033[0;37m \033[0;97;45m▌\033[0;35m▓\033[0;35;45m \033[0;90m▌\033[0;37m   \033[0;90m█\033[0;35;45m \033[0;35m▓\033[0;90;45m▐\033[0;37m  \033[0;35;47m▐\033[0;35m▓\033[0;35;45m \033[0;90;45m▓\033[0;90m▌\033[0;37m   \033[0;97;45m▌\033[0;35m▓\033[0;35;45m \033[0;90m▌\033[0;37m   ▐\033[0;35;45m \033[0;35m▓\033[0;90;45m▐\033[0;37m  ▐\033[0;37;45m \033[0;95;45m▒▒\033[0;90m▌\033[0;37m       \033[0;35;47m▐\033[0;35m▓\033[0;35;45m \033[0;90;45m▐\033[0;90m▄▄▄\033[0;37m      \033[0;90;45m▌ \033[0;95;45m░\033[0;90;45m▐\033[0;37m    \033[0;90;47m▓\033[0;90;45m░▒\033[0;90m▄\033[0;37m ▐\033[0;37;45m   \033[0;90;45m▀▀▀▀\033[0;90m▄\033[0;37m   \033[0m",
    "\033[0;37m▐\033[0;35m▓▒█\033[0;90m▌\033[0;37m   \033[0;90m█\033[0;37;45m▌\033[0;35m▒\033[0;90m█\033[0;37m  \033[0;90;45m▌\033[0;35m▒▓▓\033[0;90m▌\033[0;37m  ▐\033[0;35m▓▒\033[0;90;45m▐\033[0;37m     \033[0;37;45m▌\033[0;35m▒▓\033[0;90m▌\033[0;37m \033[0;90m▐\033[0;35m░▒▓\033[0;90m▌\033[0;37m       \033[0;90;45m▌\033[0;35m▒▓▓▒░\033[0;90m▌\033[0;37m      \033[0;90m▌\033[0;35m▓\033[0;35;45m \033[0;90;45m▐\033[0;37m    \033[0;90m██▓▒▌\033[0;37m ▀\033[0;90;45m▄▄▄\033[0;35m█▓▓▒\033[0;90;45m▀\033[0;90m▄\033[0;37m \033[0m",
    "\033[0;37m \033[0;35;47m▐\033[0;35m▒░\033[0;90;45m▐\033[0;37m  \033[0;90m▐▌\033[0;35m░▒\033[0;90m█\033[0;37m  \033[0;90m▌\033[0;35m░\033[0;37m \033[0;90;45m▐\033[0;90m▌\033[0;37m   \033[0;35;47m▐\033[0;35m▒░\033[0;90m▌\033[0;37m   ▐\033[0;35m░▒\033[0;90;45m▐\033[0;37m  \033[0;90m▐\033[0;37m \033[0;35m░░\033[0;90m▌\033[0;37m   \033[0;90m▄\033[0;37m   \033[0;90m▌\033[0;35m░\033[0;37m \033[0;90;45m▐\033[0;90m▀▀\033[0;37m       ▌ \033[0;35m▓\033[0;90;45m▐\033[0;37m     \033[0;90m▀▀▀\033[0;37m ▄▄\033[0;90m▄▄\033[0;37m \033[0;90m▀\033[0;90;45m▌\033[0;35m▒░░\033[0;90;45m▐\033[0;90m▌\033[0m",
    "\033[0;37m \033[0;90m▀\033[0;90;45m▄\033[0;35m░░\033[0;90m▀▄▌\033[0;35m░░\033[0;90;45m▄\033[0;37m   \033[0;90m▌\033[0;37m   \033[0;90m█\033[0;37m   \033[0;90m▐\033[0;35m░░\033[0;90m▀▄▄▄\033[0;37m▀\033[0;35m░░\033[0;90m▌\033[0;37m  ▐   \033[0;90m▀▀▀▀\033[0;37m \033[0;90m▌\033[0;37m  \033[0;90m▌\033[0;37m  \033[0;90m▀▄▄▄▀█\033[0;37m    ▌ \033[0;35m▒\033[0;90m▐\033[0;37m         ▐  \033[0;90m▀▄▄▀\033[0;37m \033[0;35m░\033[0;37m \033[0;90m█▌\033[0m",
    "\033[0;37m   \033[0;90m▀▄\033[0;37m   \033[0;90m▄▀\033[0;37m  \033[0;90m▄▀\033[0;37m  \033[0;90m░▓█▄\033[0;37m   \033[0;90m▀▄\033[0;37m     \033[0;90m▄▀\033[0;37m   ▌        \033[0;90m▐▄▀\033[0;37m        \033[0;90m▐\033[0;37m   ▐    \033[0;90m▌\033[0;37m        \033[0;90m▐▌\033[0;37m      \033[0;90m▄▄▀\033[0;37m \033[0m",
    "\033[0;37m     \033[0;90m▀▀▀\033[0;37m     \033[0;90m▀▀▀▀▀▀\033[0;37m      \033[0;90m▀▀▀▀▀\033[0;37m    ▀\033[0;90m▀▀▀▀▀▀▀▀▀▀\033[0;37m \033[0;90m▀▀▀▀▀▀▀▀▀▀\033[0;37m   ▀\033[0;90m▀▀▀▀\033[0;37m          \033[0;90m▀▀▀▀▀▀▀\033[0;37m    \033[0m",
]

COLORS = {
    "background": "#000000",
    "color5": "#AA00AA",
    "color7": "#AAAAAA",
    "color8": "#555555",
    "color13": "#FF55FF",
    "color15": "#FFFFFF",
}
COLORS_256 = {
    "background": 16,
    "color5": 127,
    "color7": 248,
    "color8": 240,
    "color13": 207,
    "color15": 231,
}
FOREGROUND = {"35": "color5", "37": "color7", "90": "color8", "95": "color13", "97": "color15"}
BACKGROUND = {"45": "color5", "47": "color7"}
TRUECOLOR = WINDOWS or os.environ.get("COLORTERM") in ("truecolor", "24bit")
MIN_COLUMNS = 90
MIN_ROWS = 24


FEATURES = [
    "Ping",
    "Port Scanner",
    "IP / Domain Lookup",
    "DNS Records",
    "WHOIS",
    "SSL Inspector",
    "Subdomain Finder",
    "Website Info",
    "Wayback Machine",
    "Google Dork Builder",
    "Username Search",
    "Email Recon",
    "Pwned Password",
    "Geolocator",
    "Image EXIF",
    "Photo Geotag",
    "Image Strings",
    "Stego Detector",
    "Reverse Image Search",
    "Hashes",
    "Snowflake Decoder",
    "Invite Inspector",
    "Webhook Inspector",
    "Webhook Tester",
    "Embed Builder",
    "Phone Lookup",
    "MAC Vendor",
    "PDF Metadata",
    "Password Tools",
    "BIN Lookup",
]
PER_PAGE = 10
MENU_ROWS = 5
MENU_WIDTH = 42
PAGE_TITLES = {
    0: "Network & Web",
    1: "OSINT & Forensics",
    2: ("Discord", "Identity & Metadata"),
}

FPS = 30
STEP_TIME = 0.07
COLUMN_DELAY = 0.02
ROW_DELAY = 0.07
JITTER = 0.25
STEPS = [("0;90", "░"), ("0;35", "▒"), ("0;95", "▓"), ("0;97", "█")]


def parse_art():
    rows = []
    for line in ART:
        cells = []
        for style, text in re.findall(r"\033\[([\d;]+)m([^\033]*)", line):
            cells += [(style, char) for char in text]
        rows.append(cells)
    return rows


def is_empty(style, char):
    return char == " " and not {"45", "47"} & set(style.split(";"))


def page_count():
    return (len(FEATURES) + PER_PAGE - 1) // PER_PAGE


def make_starts(rows):
    return [
        [
            col * COLUMN_DELAY
            + (len(rows) - 1 - y) * ROW_DELAY
            + random.uniform(0, JITTER)
            for col in range(len(row))
        ]
        for y, row in enumerate(rows)
    ]


@functools.lru_cache(maxsize=None)
def paint(style):
    codes = style.split(";")
    fg = next((FOREGROUND[c] for c in codes if c in FOREGROUND), "color7")
    bg = next((BACKGROUND[c] for c in codes if c in BACKGROUND), "background")
    parts = ["0"]
    for target, name in (("38", fg), ("48", bg)):
        if TRUECOLOR:
            value = COLORS[name].lstrip("#")
            rgb = ";".join(str(int(value[i:i + 2], 16)) for i in (0, 2, 4))
            parts.append(f"{target};2;{rgb}")
        else:
            parts.append(f"{target};5;{COLORS_256[name]}")
    return f"\033[{';'.join(parts)}m"


def paint_line(line):
    return re.sub(r"\033\[([\d;]+)m", lambda match: paint(match.group(1)), line)


def art_lines(rows, starts, elapsed):
    lines = []
    for row, row_starts in zip(rows, starts):
        out = []
        last = None
        for (style, char), start in zip(row, row_starts):
            step = int((elapsed - start) // STEP_TIME)
            if step < 0 or is_empty(style, char):
                style, char = "0", " "
            elif step < len(STEPS):
                style, char = STEPS[step]
            if style != last:
                out.append(f"\033[{style}m")
                last = style
            out.append(char)
        lines.append("".join(out))
    return lines


def styled_title(name):
    return f"\033[0;95m<.>\033[0;97m {name} \033[0;95m<.>\033[0m"


def title_cell(name):
    if not name:
        return " " * MENU_WIDTH
    text = f"<.> {name} <.>"
    pad = max(0, (MENU_WIDTH - len(text)) // 2)
    return " " * pad + styled_title(name) + " " * max(0, MENU_WIDTH - pad - len(text))


def title_line(page):
    title = PAGE_TITLES.get(page)
    if not title:
        return None
    if isinstance(title, (tuple, list)):
        left, right = title
        if not left and not right:
            return None
        return "  " + title_cell(left) + title_cell(right)
    items = FEATURES[page * PER_PAGE:page * PER_PAGE + MENU_ROWS]
    left_end = 7 + max((len(item[:MENU_WIDTH - 6]) for item in items), default=0)
    center = (left_end + 2 + MENU_WIDTH) // 2
    text = f"<.> {title} <.>"
    pad = max(0, center - len(text) // 2)
    return " " * pad + styled_title(title)


def menu_lines(page):
    first = page * PER_PAGE
    items = FEATURES[first:first + PER_PAGE]
    lines = []
    title = title_line(page)
    if title:
        lines += [title, ""]
    for row in range(MENU_ROWS):
        out = "  "
        for index in range(row, len(items), MENU_ROWS):
            number = f"[{first + index + 1}]".rjust(4)
            label = items[index][:MENU_WIDTH - 6].ljust(MENU_WIDTH - 5)
            out += f"\033[0;95m{number}\033[0;97m {label}"
        lines.append(out)
    left = "<- " if page > 0 else "   "
    right = " ->" if page < page_count() - 1 else ""
    lines.append("")
    lines.append(f"   \033[0;95m{left}\033[0;37mPage {page + 1}/{page_count()}\033[0;95m{right}")
    return lines


def input_lines(value, message):
    return [
        f"   \033[0;97mValue: \033[0;95m{value}_  \033[0;37m{message}",
        "   \033[0;90mpress esc to exit",
        "   \033[0;90m© 2026 Matas  ·  All Rights Reserved",
    ]


def draw(lines):
    height = shutil.get_terminal_size().lines
    blank = paint("0")
    out = []
    for y, line in enumerate(lines[:height], 1):
        out.append(f"\033[{y};1H{blank}{paint_line(line)}{blank}\033[K")
    out.append("\033[J")
    sys.stdout.write("".join(out))
    sys.stdout.flush()


def save_terminal():
    if WINDOWS:
        return None
    return termios.tcgetattr(0)


def restore_terminal(old):
    if not WINDOWS:
        termios.tcsetattr(0, termios.TCSADRAIN, old)


def raw_terminal():
    if not WINDOWS:
        tty.setcbreak(0)
        return
    kernel32 = ctypes.windll.kernel32
    kernel32.GetStdHandle.restype = ctypes.c_void_p
    handle = ctypes.c_void_p(kernel32.GetStdHandle(-11))
    mode = ctypes.c_uint32()
    if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
        kernel32.SetConsoleMode(handle, mode.value | 0x0005)


def flush_input():
    if not WINDOWS:
        termios.tcflush(0, termios.TCIFLUSH)
        return
    while msvcrt.kbhit():
        msvcrt.getwch()


def read_keys_windows(timeout):
    end = time.monotonic() + timeout
    while not msvcrt.kbhit():
        if time.monotonic() >= end:
            return []
        time.sleep(0.01)
    keys = []
    while msvcrt.kbhit():
        char = msvcrt.getwch()
        if char in ("\x00", "\xe0"):
            code = msvcrt.getwch()
            if code == "M":
                keys.append("right")
            elif code == "K":
                keys.append("left")
        elif char == "\x03":
            raise KeyboardInterrupt
        elif char == "\x1b":
            keys.append("esc")
        elif char in ("\r", "\n"):
            keys.append("enter")
        elif char == "\x08":
            keys.append("backspace")
        elif char in "0123456789":
            keys.append(char)
    return keys


def read_keys_posix(timeout):
    if not select.select([0], [], [], timeout)[0]:
        return []
    data = os.read(0, 1024)
    if not data:
        return ["esc"]
    while data.endswith((b"\033", b"\033[", b"\033O")):
        if not select.select([0], [], [], 0.05)[0]:
            break
        more = os.read(0, 1024)
        if not more:
            break
        data += more
    keys = []
    for token in re.findall(rb"\033\[[0-?]*[ -/]*[@-~]|\033O.|\033[^\033\[O]|\033|[^\033]", data):
        if token in (b"\033[C", b"\033OC"):
            keys.append("right")
        elif token in (b"\033[D", b"\033OD"):
            keys.append("left")
        elif token == b"\033":
            keys.append("esc")
        elif token in (b"\r", b"\n"):
            keys.append("enter")
        elif token in (b"\x7f", b"\x08"):
            keys.append("backspace")
        elif token in b"0123456789":
            keys.append(token.decode())
    return keys


def read_keys(timeout):
    if WINDOWS:
        return read_keys_windows(timeout)
    return read_keys_posix(timeout)


def call_feature(number):
    name = f"F{number}"
    sys.modules.pop(name, None)
    importlib.invalidate_caches()
    module = importlib.import_module(name)
    getattr(module, name)()


def enter_menu_screen():
    flush_input()
    raw_terminal()
    sys.stdout.write(f"\033[?1049h\033[?25l\033[?7l{paint('0')}\033[2J")
    sys.stdout.flush()


def leave_menu_screen(old):
    sys.stdout.write("\033[0m\033[?7h\033[?25h\033[?1049l")
    sys.stdout.flush()
    restore_terminal(old)


def run_feature(old, number):
    leave_menu_screen(old)
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()
    try:
        call_feature(number)
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception:
        traceback.print_exc()
    if sys.stdin.closed:
        sys.stdin = open(0, closefd=False)
    sys.stderr.flush()
    raw_terminal()
    sys.stdout.write("\033[0m\n\033[0;90mpress esc to return\033[0m")
    sys.stdout.flush()
    flush_input()
    try:
        while "esc" not in read_keys(0.25):
            pass
    except KeyboardInterrupt:
        pass
    enter_menu_screen()


def run_menu(old):
    rows = parse_art()
    page = 0
    value = ""
    message = ""
    time.sleep(0.4)
    while True:
        starts = make_starts(rows)
        total = max(map(max, starts)) + (len(STEPS) + 1) * STEP_TIME
        menu = menu_lines(page)
        begin = time.monotonic()
        new_page = page
        selected = None
        drawn = None
        finished = False
        while new_page == page and selected is None:
            elapsed = min(time.monotonic() - begin, total)
            state = (shutil.get_terminal_size(), value, message)
            if not finished or state != drawn:
                draw(art_lines(rows, starts, elapsed) + [""] + menu + input_lines(value, message))
                drawn = state
                finished = elapsed >= total
            for key in read_keys(0.25 if finished else 1 / FPS):
                message = ""
                if key == "esc":
                    return
                if key == "right":
                    new_page = min(page_count() - 1, new_page + 1)
                elif key == "left":
                    new_page = max(0, new_page - 1)
                elif key == "backspace":
                    value = value[:-1]
                elif key == "enter":
                    if value and 1 <= int(value) <= len(FEATURES):
                        selected = int(value)
                        value = ""
                        break
                    if value:
                        message = f"enter 1-{len(FEATURES)}"
                    value = ""
                elif len(value) < 2:
                    value += key
        page = new_page
        if selected is not None:
            run_feature(old, selected)


def show():
    if sys.stdout.encoding.lower().replace("-", "") != "utf8":
        sys.stdout.reconfigure(encoding="utf-8")
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        print("\n".join(ART + [""] + menu_lines(0)) + "\033[0m")
        return
    old = save_terminal()
    try:
        raw_terminal()
        sys.stdout.write("\033]0;Violet's\007")
        size = shutil.get_terminal_size()
        if size.columns < MIN_COLUMNS or size.lines < MIN_ROWS:
            rows = max(size.lines, MIN_ROWS)
            columns = max(size.columns, MIN_COLUMNS)
            sys.stdout.write(f"\033[8;{rows};{columns}t")
        enter_menu_screen()
        run_menu(old)
    except KeyboardInterrupt:
        pass
    finally:
        leave_menu_screen(old)


def terminal_command(command):
    kitty = ["kitty", "--title", "Violet's", "-o", "background_opacity=1"]
    for name, value in COLORS.items():
        kitty += ["-o", f"{name}={value}"]
    terminals = [
        kitty,
        ["ghostty", "-e"],
        ["alacritty", "-e"],
        ["wezterm", "start", "--"],
        ["foot"],
        ["konsole", "-e"],
        ["ptyxis", "--"],
        ["kgx", "--"],
        ["gnome-terminal", "--"],
        ["xfce4-terminal", "-x"],
        ["mate-terminal", "-x"],
        ["tilix", "-e"],
        ["x-terminal-emulator", "-e"],
        ["xterm", "-e"],
    ]
    for terminal in terminals:
        if shutil.which(terminal[0]):
            if terminal[0] == "tilix":
                return terminal + [shlex.join(command)]
            return terminal + command
    return None


def open_terminal(command):
    if WINDOWS:
        subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
        return True
    if MAC:
        text = shlex.join(command).replace("\\", "\\\\").replace('"', '\\"')
        launch = ["osascript", "-e", f'tell application "Terminal" to do script "{text}; exit"',
                  "-e", 'tell application "Terminal" to activate']
    elif os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"):
        launch = terminal_command(command)
    else:
        launch = None
    if launch is None:
        return False
    subprocess.Popen(launch, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL, start_new_session=True)
    return True


def main():
    if "--show" in sys.argv:
        show()
        return
    python = sys.executable
    if WINDOWS and os.path.basename(python).lower() == "pythonw.exe":
        python = os.path.join(os.path.dirname(python), "python.exe")
    if not open_terminal([python, os.path.abspath(__file__), "--show"]):
        show()


if __name__ == "__main__":
    main()
