"""Player-controlled paddle entity for Breakout."""

from turtle import Turtle


class Paddle(Turtle):
    """Represents the horizontal paddle with keyboard, mouse-drag, and shrink support."""

    def __init__(self, position, screen_width=800):
        """Initialise the paddle at the given position and bind mouse dragging."""
        super().__init__()
        self.shape("square")
        self.color("white")
        self.screen_half_width = screen_width / 2.0
        self.base_width = 100
        self.width = self.base_width
        self.is_shrunk = False

        # Scale from Turtle's default 20px square length
        self.shapesize(stretch_wid=1, stretch_len=self.width / 20.0)
        self.penup()
        self.goto(position)
        self.ondrag(self.drag_paddle)

    def _max_x(self):
        """Return the furthest valid centre X-coordinate for the current width."""
        return self.screen_half_width - (self.width / 2.0)

    def go_right(self):
        """Shift the paddle right by 20px without crossing the right border."""
        new_x = min(self.xcor() + 20, self._max_x())
        self.goto(new_x, self.ycor())

    def go_left(self):
        """Shift the paddle left by 20px without crossing the left border."""
        new_x = max(self.xcor() - 20, -self._max_x())
        self.goto(new_x, self.ycor())

    def drag_paddle(self, x, y):
        """Move the paddle horizontally to follow mouse drag while locking Y."""
        # Temporarily unbind ondrag during goto() to avoid recursive event lag
        self.ondrag(None)
        limit = self._max_x()
        clamped_x = max(-limit, min(limit, x))
        self.goto(clamped_x, self.ycor())
        self.ondrag(self.drag_paddle)

    def shrink(self):
        """Halve the paddle width once when the ball reaches the top wall."""
        if not self.is_shrunk:
            self.width = self.base_width / 2.0
            self.shapesize(stretch_wid=1, stretch_len=self.width / 20.0)
            self.is_shrunk = True