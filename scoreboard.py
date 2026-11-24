"""HUD rendering and JSON high-score persistence for Breakout."""

import json
from turtle import Turtle

HIGH_SCORE_FILE = "high_score.json"


class Scoreboard(Turtle):
    """Displays score, lives, high score, and end-of-game messages."""

    def __init__(self, starting_lives=3, high_score_file=HIGH_SCORE_FILE):
        """Initialise score state, load persisted high score, and draw the HUD."""
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.high_score_file = high_score_file
        self.score = 0
        self.lives = starting_lives
        self.high_score = self._load_high_score()
        self.update_scoreboard()

    def _load_high_score(self):
        """Load the saved high score, creating the JSON file with 0 if missing."""
        try:
            with open(self.high_score_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                return int(data.get("high_score", 0))
        except (FileNotFoundError, json.JSONDecodeError, ValueError, TypeError):
            self._save_high_score(0)
            return 0

    def _save_high_score(self, value):
        """Write the given high score value to the JSON file."""
        with open(self.high_score_file, "w", encoding="utf-8") as file:
            json.dump({"high_score": value}, file, indent=4)

    def update_scoreboard(self):
        """Clear and redraw high score, lives, and current score on the canvas."""
        self.clear()

        # High score in the top-left margin above the brick grid
        self.goto(-360, 273)
        self.write(
            f"HIGH SCORE: {self.high_score}",
            align="left",
            font=("Courier", 15, "bold"),
        )

        # Remaining lives in the top-right margin above the brick grid
        self.goto(360, 273)
        self.write(
            f"LIVES: {self.lives}",
            align="right",
            font=("Courier", 15, "bold"),
        )

        # Current score centred in the open space below the paddle
        self.goto(0, -280)
        self.write(
            f"SCORE: {self.score}",
            align="center",
            font=("Courier", 24, "bold"),
        )

    def add_points(self, points):
        """Add points to the score and persist immediately on a new high score."""
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score
            self._save_high_score(self.high_score)
        self.update_scoreboard()

    def lose_life(self):
        """Decrement remaining lives by one and refresh the HUD."""
        self.lives -= 1
        self.update_scoreboard()

    def show_end_message(self, won=False):
        """Display the final win or game-over banner in the centre of the screen."""
        self.goto(0, -40)
        message = "YOU WIN!" if won else "GAME OVER"
        self.write(message, align="center", font=("Courier", 36, "bold"))