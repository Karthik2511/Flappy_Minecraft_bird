# Flappy Minecraft Bird

A simple Flappy Bird-style game made with Python and Pygame, using Minecraft-themed sprites.

## Features

- Side-scrolling background
- Bird movement with gravity and jump physics
- Randomized pipe generation
- Collision detection
- Score tracking
- Start menu and pause menu

## Requirements

- Python 3.8+
- Pygame

Install dependency:

```bash
pip install pygame
```

## Project Files

- `game.py` - main game source code
- `bird.png` - bird sprite
- `pipe.png` - pipe sprite
- `background.png` - scrolling background image
- `pause.png` - pause icon

## How to Run

From the project directory:

```bash
python game.py
```

## Controls

- `Space` - make the bird jump
- Mouse click on `Start` - begin game from main menu
- Mouse click on pause icon (top-left) - open pause menu
- Mouse click on `Resume` - continue game
- Mouse click on `Exit` - quit from pause menu

## Gameplay

- Avoid hitting pipes.
- Passing each pipe increases score by 1.
- The game ends on collision.

## Notes

- Keep all image files in the same directory as `game.py`.
- If an image is missing, Pygame will raise a file loading error at startup.
