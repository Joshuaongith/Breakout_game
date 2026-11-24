"""Ball entity and movement physics for Breakout."""

import math
from turtle import Turtle


class Ball(Turtle):
    """Represents the game ball, managing its velocity vector and bounce maths."""

    def __init__(self, base_speed=2.0, radius=10):
        """Initialise the ball at the centre of the screen moving straight down."""
        super().__init__()
        self.color("white")
        self.shape("circle")
        self.penup()

        # Total speed in pixels per frame; x_move and y_move form the velocity vector
        self.base_speed = base_speed
        self.move_speed = base_speed
        self.radius = radius
        self.x_move = 0.0
        self.y_move = -self.move_speed

    def move(self):
        """Advance the ball by one frame using its current X and Y velocity."""
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        """Invert vertical velocity for ceiling and top/bottom brick collisions."""
        self.y_move *= -1

    def bounce_x(self):
        """Invert horizontal velocity for side wall and side brick collisions."""
        self.x_move *= -1

    def increase_speed(self, increment=0.75):
        """Increase speed and scale the current velocity vector to keep the angle."""
        old_speed = self.move_speed
        self.move_speed += increment
        scale = self.move_speed / old_speed
        self.x_move *= scale
        self.y_move *= scale

    def check_brick_collision(self, brick, radius=None):
        """Test circle-to-rectangle collision against a brick and bounce on impact.

        Returns True if the ball collided with the brick, otherwise False.
        """
        check_radius = self.radius if radius is None else radius
        closest_x, closest_y = brick.closest_point(self.xcor(), self.ycor())

        # True circular check from the ball's centre to the nearest edge point
        if self.distance(closest_x, closest_y) > check_radius:
            return False

        dx = self.xcor() - closest_x
        dy = self.ycor() - closest_y

        if dx == 0 and dy == 0:
            # Fallback if high speed places the ball's centre inside the brick
            overlap_x = (brick.width / 2.0) - abs(self.xcor() - brick.xcor())
            overlap_y = (brick.height / 2.0) - abs(self.ycor() - brick.ycor())
            if overlap_x < overlap_y:
                self.bounce_x()
            else:
                self.bounce_y()
        elif abs(dx) > abs(dy):
            # Greater horizontal separation indicates a left or right side hit
            self.bounce_x()
        else:
            # Greater or equal vertical separation indicates a top or underside hit
            self.bounce_y()

        return True

    def bounce_paddle(self, paddle):
        """Compute an outbound bounce angle based on where the ball hits the paddle."""
        # Snap ball onto the paddle's top surface (10px paddle + 10px ball radius)
        # to prevent tunnelling through the paddle on subsequent frames.
        self.sety(paddle.ycor() + 20)

        # Normalise the horizontal hit position to [-1.0 (left), 1.0 (right)]
        offset = self.xcor() - paddle.xcor()
        half_width = paddle.width / 2.0
        ratio = max(-1.0, min(1.0, offset / half_width))

        # Map ratio to a bounce angle: 90° is straight up, ±60° max deflection
        bounce_angle_degrees = 90 - (ratio * 60)
        angle_radians = math.radians(bounce_angle_degrees)

        # Reconstruct velocity components; abs() ensures the ball always moves upward
        self.x_move = self.move_speed * math.cos(angle_radians)
        self.y_move = abs(self.move_speed * math.sin(angle_radians))

    def reset_position(self):
        """Return the ball to the origin at base speed after a missed serve."""
        self.goto(0, 0)
        self.move_speed = self.base_speed
        self.x_move = 0.0
        self.y_move = -self.move_speed