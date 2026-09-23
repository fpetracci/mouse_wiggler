"""Keep the session active by nudging the mouse and clicking a safe spot.

Usage:
    uv run stay_active.py            # hover over a safe spot during the countdown
    uv run stay_active.py --at 50,900
    uv run stay_active.py --no-click # only wiggle, never click
    uv run stay_active.py --where    # show pointer coordinates to find a safe spot

Press Ctrl+C to stop.
"""

import argparse
import random
import time

from pynput.mouse import Button, Controller

MIN_DELAY = 4.0
MAX_DELAY = 6.0
JITTER = 15  # max pixels the pointer wanders around the safe spot
COUNTDOWN = 5


def parse_point(value: str) -> tuple[int, int]:
    x, y = value.split(",")
    return int(x), int(y)


def glide(mouse: Controller, target: tuple[int, int], steps: int) -> None:
    """Move the pointer to target in small steps so it looks like a real movement."""
    sx, sy = mouse.position
    tx, ty = target
    for i in range(1, steps + 1):
        mouse.position = (
            round(sx + (tx - sx) * i / steps),
            round(sy + (ty - sy) * i / steps),
        )
        time.sleep(random.uniform(0.005, 0.02))


def act(mouse: Controller, safe: tuple[int, int], click: bool) -> str:
    action = random.choice(["wiggle", "click", "wiggle+click"]) if click else "wiggle"
    if "wiggle" in action:
        for _ in range(random.randint(1, 3)):
            offset = (
                safe[0] + random.randint(-JITTER, JITTER),
                safe[1] + random.randint(-JITTER, JITTER),
            )
            glide(mouse, offset, random.randint(5, 15))
    glide(mouse, safe, random.randint(5, 15))
    if "click" in action:
        mouse.click(Button.left)
    return action


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--at",
        type=parse_point,
        help="safe spot to click, as X,Y (default: pointer position after countdown)",
    )
    parser.add_argument(
        "--no-click", action="store_true", help="only move the mouse, never click"
    )
    parser.add_argument(
        "--where",
        action="store_true",
        help="print the pointer position live, to find a safe spot",
    )
    args = parser.parse_args()

    mouse = Controller()
    try:
        if args.where:
            while True:
                x, y = (int(c) for c in mouse.position)
                print(f"\rPointer at {x},{y}      ", end="", flush=True)
                time.sleep(0.1)
        if args.at:
            safe: tuple[int, int] = args.at
        else:
            print("Move the mouse over a safe spot (empty desktop / blank area)...")
            for i in range(COUNTDOWN, 0, -1):
                print(f"  {i}", flush=True)
                time.sleep(1)
            x, y = mouse.position
            safe = (int(x), int(y))
        print(f"Safe spot: {safe}. Running, press Ctrl+C to stop.")

        while True:
            delay = random.uniform(MIN_DELAY, MAX_DELAY)
            time.sleep(delay)
            action = act(mouse, safe, click=not args.no_click)
            print(
                f"[{time.strftime('%H:%M:%S')}] {action} (waited {delay:.1f}s)",
                flush=True,
            )
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
