"""Main entry point and game loop for Breakout."""

import time
from turtle import Screen

from ball import Ball
from bricks import BrickManager
from paddle import Paddle
from scoreboard import Scoreboard

# Configure main game window with manual frame updates (tracer=0) for smooth animation
screen = Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Breakout")
screen.tracer(0)

# Initialise core game entities
paddle = Paddle((0, -200))
ball = Ball(base_speed=2.0)
scoreboard = Scoreboard(starting_lives=3)
brick_manager = BrickManager()

# Bind keyboard controls (mouse dragging is bound inside Paddle.__init__)
screen.listen()
screen.onkey(paddle.go_right, "Right")
screen.onkey(paddle.go_left, "Left")

# Trackers for classic Breakout speed-up milestones
paddle_hits = 0
hit_orange = False
hit_red = False

game_is_on = True
while game_is_on:
    time.sleep(0.01)
    screen.update()
    ball.move()

    # Check brick collisions and trigger colour-based speed milestones
    hit_brick = brick_manager.check_collision(ball, ball_radius=10)
    if hit_brick:
        scoreboard.add_points(hit_brick.points)

        if hit_brick.brick_color == "orange" and not hit_orange:
            hit_orange = True
            ball.increase_speed()
        elif hit_brick.brick_color == "red" and not hit_red:
            hit_red = True
            ball.increase_speed()

        # Clear remaining sprites and flush one final frame once all bricks are broken
        if not brick_manager.bricks:
            ball.hideturtle()
            paddle.ondrag(None)
            paddle.hideturtle()
            scoreboard.show_end_message(won=True)
            screen.update()
            game_is_on = False
            break

    # Side wall bounce (direction check prevents the ball getting stuck in a wall)
    if (ball.xcor() > 380 and ball.x_move > 0) or (ball.xcor() < -380 and ball.x_move < 0):
        ball.bounce_x()

    # Ceiling bounce (triggers classic one-time paddle shrink)
    if ball.ycor() > 280 and ball.y_move > 0:
        ball.bounce_y()
        paddle.shrink()

    # Rectangular bounding-box check against the paddle (includes 10px ball radius)
    paddle_half_width = paddle.width / 2.0
    within_x = abs(ball.xcor() - paddle.xcor()) <= (paddle_half_width + 10)
    within_y = (paddle.ycor() - 10) <= ball.ycor() <= (paddle.ycor() + 20)

    if within_x and within_y and ball.y_move < 0:
        ball.bounce_paddle(paddle)
        paddle_hits += 1
        if paddle_hits in (4, 12):
            ball.increase_speed()

    # Handle missed ball below the paddle plane
    if ball.ycor() < -220:
        scoreboard.lose_life()
        if scoreboard.lives <= 0:
            scoreboard.show_end_message(won=False)
            screen.update()
            game_is_on = False
        else:
            ball.reset_position()
            paddle_hits = 0
            hit_orange = False
            hit_red = False

screen.exitonclick()