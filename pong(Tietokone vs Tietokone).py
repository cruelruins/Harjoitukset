import turtle
import random

# Window
wn = turtle.Screen()
wn.title("Pong - MAX AI vs MAX AI")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

# Score
score_a = 0
score_b = 0
name_a = "TIETOKONE 1"
name_b = "TIETOKONE 2"
win_score = 3

# Paddles
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 5
ball.dy = -5

# Scoreboard
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)

def update_score():
    pen.clear()
    pen.write(f"{name_a}: {score_a}  |  {name_b}: {score_b}",
              align="center", font=("Courier", 18, "normal"))

update_score()

# -------- SETTINGS --------
ai_speed = 40  # VERY FAST movement (max AI feel)
ai_error = 0   # 0 = perfect tracking (increase for human-like mistakes)

# -------- BALL RESET --------
def reset_ball():
    ball.goto(0, 0)
    ball.dx = 0
    ball.dy = 0

    def restart():
        ball.dx = random.choice([-4, 4])
        ball.dy = random.choice([-4, 4])

    wn.ontimer(restart, 500)

# -------- AI (MAX SPEED + SMART TRACKING) --------
def move_ai(paddle, target_y):
    # Optional tiny randomness (set ai_error > 0 if you want chaos)
    target_y += random.randint(-ai_error, ai_error)

    # Clamp movement inside screen
    new_y = paddle.ycor()

    if new_y < target_y:
        new_y = min(new_y + ai_speed, target_y)
    elif new_y > target_y:
        new_y = max(new_y - ai_speed, target_y)

    # Keep paddle in bounds
    new_y = max(-250, min(250, new_y))

    paddle.sety(new_y)

# -------- GAME LOOP --------
def game_loop():
    global score_a, score_b

    wn.update()

    # ===== AI MOVEMENT (BOTH SIDES MAX SPEED) =====
    move_ai(paddle_a, ball.ycor())
    move_ai(paddle_b, ball.ycor())

    # Ball movement
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Wall bounce
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1

    # Right miss (AI B loses point)
    if ball.xcor() > 390:
        score_a += 1
        update_score()
        reset_ball()

    # Left miss (AI A loses point)
    if ball.xcor() < -390:
        score_b += 1
        update_score()
        reset_ball()

    # Paddle B collision
    if (340 < ball.xcor() < 350) and (paddle_b.ycor() - 50 < ball.ycor() < paddle_b.ycor() + 50):
        ball.setx(340)
        ball.dx *= -1.1

    # Paddle A collision
    if (-350 < ball.xcor() < -340) and (paddle_a.ycor() - 50 < ball.ycor() < paddle_a.ycor() + 50):
        ball.setx(-340)
        ball.dx *= -1.1

    # Win condition
    if score_a >= win_score:
        pen.clear()
        pen.write(f"{name_a} VOITTI!", align="center", font=("Courier", 30, "bold"))
        return

    if score_b >= win_score:
        pen.clear()
        pen.write(f"{name_b} VOITTI!", align="center", font=("Courier", 30, "bold"))
        return

    wn.ontimer(game_loop, 10)

# Start
game_loop()
wn.mainloop()