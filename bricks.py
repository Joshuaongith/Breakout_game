"""Brick entity and grid collision manager for Breakout."""

from turtle import Turtle


class Brick(Turtle):
    """Represents a single destructible brick with a colour and point value."""

    def __init__(self, position, color, points, width=60, height=20):
        """Initialise a brick scaled from Turtle's default 20x20px square."""
        super().__init__()
        self.shape("square")
        self.color(color)
        # Store colour name explicitly; Turtle.color() returns a (pen, fill) tuple
        self.brick_color = color
        self.width = width
        self.height = height
        self.points = points
        self.shapesize(stretch_wid=height / 20.0, stretch_len=width / 20.0)
        self.penup()
        self.goto(position)

    def closest_point(self, x, y):
        """Clamp (x, y) to the nearest point on or inside this brick's bounds."""
        half_w = self.width / 2.0
        half_h = self.height / 2.0
        closest_x = max(self.xcor() - half_w, min(x, self.xcor() + half_w))
        closest_y = max(self.ycor() - half_h, min(y, self.ycor() + half_h))
        return closest_x, closest_y


class BrickManager:
    """Builds the multi-row brick layout and resolves ball-to-brick collisions."""

    def __init__(
        self,
        screen_width=800,
        top_y=260,
        gap=10,
        brick_width=60,
        brick_height=20,
    ):
        """Configure grid dimensions and populate the initial wall of bricks."""
        self.screen_width = screen_width
        self.top_y = top_y
        self.gap = gap
        self.brick_width = brick_width
        self.brick_height = brick_height
        self.bricks = []
        self._create_grid()

    def _create_grid(self):
        """Generate 8 centred rows of bricks (2 rows per classic colour tier)."""
        # Row definitions ordered from top row downwards: (colour, points)
        rows = [
            ("red", 7),
            ("orange", 5),
            ("yellow", 3),
            ("green", 1),
        ]

        # Calculate how many columns fit cleanly within a 40px horizontal margin
        usable_width = self.screen_width - 80
        step_x = self.brick_width + self.gap
        cols = max(1, (usable_width + self.gap) // step_x)

        # Compute the left-most brick centre so the grid sits symmetrically on X=0
        total_grid_width = cols * self.brick_width + (cols - 1) * self.gap
        start_x = -(total_grid_width / 2.0) + (self.brick_width / 2.0)
        step_y = self.brick_height + self.gap

        rows_per_color = 2
        total_rows = len(rows) * rows_per_color

        for i in range(total_rows):
            color, points = rows[i // rows_per_color]
            y_pos = self.top_y - (i * step_y)

            for col_index in range(cols):
                x_pos = start_x + (col_index * step_x)
                brick = Brick(
                    position=(x_pos, y_pos),
                    color=color,
                    points=points,
                    width=self.brick_width,
                    height=self.brick_height,
                )
                self.bricks.append(brick)

    def check_collision(self, ball, ball_radius=None):
        """Check all bricks for a collision with the ball and remove any hit brick.

        Returns the destroyed Brick instance on collision, or None if no hit occurred.
        """
        # Iterate over a shallow copy so removing a brick mid-loop is safe
        for brick in list(self.bricks):
            if ball.check_brick_collision(brick, radius=ball_radius):
                # Hide visually before removing; Turtle retains internal canvas refs
                brick.hideturtle()
                self.bricks.remove(brick)
                return brick

        return None