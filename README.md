# mouse_wiggler

Teams thinks you've gone "Away" just because you stepped out for a coffee,
a sandwich or a doom scrolling session. `mouse_wiggler` fixes that by
twitching your mouse every 4–6 seconds, and clicking now and then, like a
very dedicated employee who never blinks.

The timing and moves are random, so it looks less like a robot and more like
someone deep in thought.

## Requirements

- Linux on **X11** (Wayland blocks programs from moving the mouse)
- [uv](https://docs.astral.sh/uv/)

## Usage

```bash
uv run stay_active.py
```

You get a 5-second countdown to put the pointer over a safe spot. The script
remembers that position and keeps returning to it. Press **Ctrl+C** to stop.

| Option       | What it does                                                   |
| ------------ | -------------------------------------------------------------- |
| `--at X,Y`   | Use these coordinates as the safe spot instead of the countdown |
| `--no-click` | Only move the mouse, never click                               |
| `--where`    | Show the pointer coordinates live, to find a safe spot         |

Each action is picked at random: a **wiggle** (the pointer drifts up to 15px
from the safe spot and back), a **click** on the safe spot, or both. With
`--no-click` every action is a wiggle.

While it runs, the script controls your mouse. Stop it before using the
computer.

## Finding a safe spot

Run `uv run stay_active.py --where`, hover over a spot, note the `X,Y`, press
Ctrl+C, then start with `uv run stay_active.py --at X,Y`.

A safe spot is somewhere a click does nothing, such as the empty part of a
panel or taskbar, or blank padding in an app you keep open. Avoid buttons,
links, screen corners (hot corners), the Teams message box and chat list,
window title bars, and anywhere notifications appear. Leave some empty space
around the spot, since the pointer wanders a little while wiggling.

If you're unsure, use `--no-click`: mouse movement alone is usually enough.

## Configuration

Edit the constants at the top of `stay_active.py`:

- `MIN_DELAY` / `MAX_DELAY`: the range of seconds between actions
- `JITTER`: how far, in pixels, the pointer wanders from the safe spot
- `COUNTDOWN`: seconds you get to position the pointer at startup

## Development

```bash
uv run ruff check
uv run ruff format
uv run mypy .
```
