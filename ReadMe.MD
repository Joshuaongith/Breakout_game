# Breakout

A Python implementation of the classic Breakout arcade game built with the standard library `turtle` module. No external dependencies are required.

## Controls

- **Left / Right Arrow Keys:** Move the paddle horizontally.
- **Mouse Drag:** Click and drag the paddle directly along the horizontal axis.
- **Click Window (after Win / Game Over):** Close the game.

## Game Rules

- **Brick Scoring (8 rows total, 2 rows per colour):**
  - Green: 1 point
  - Yellow: 3 points
  - Orange: 5 points
  - Red: 7 points
- **Paddle Aiming:** The ball's bounce angle depends on where it hits the paddle—straight up from the centre, angling outward up to 60° towards the edges.
- **Speed Increases:** Ball speed increases after the 4th and 12th paddle hits, as well as on the first hit to an orange brick and the first hit to a red brick. Speed milestones reset when a life is lost.
- **Paddle Shrink:** Hitting the top wall shrinks the paddle to half its original width.
- **Lives & High Score:** Players start with 3 lives. The highest score is saved automatically to `high_score.json` in the project directory.

## Project Structure

- `main.py` — Window setup, input bindings, collision checks, and main game loop.
- `ball.py` — Ball velocity vector movement, speed scaling, and trigonometric paddle bounce logic.
- `paddle.py` — Paddle movement, boundary clamping, mouse dragging, and shrink behaviour.
- `bricks.py` — `Brick` and `BrickManager` classes for generating the brick wall and resolving brick collisions.
- `scoreboard.py` — Score, lives, end-screen messages, and JSON high-score loading/saving.

## Requirements & Running

Requires Python 3.x (uses only `turtle`, `math`, `time`, and `json` from the Python standard library).

```bash
python3 main.py