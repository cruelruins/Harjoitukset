import turtle
import random

# Ikkuna
wn = turtle.Screen()
wn.title("Pong")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

# Pisteet ja nimet
score_a = 0
score_b = 0
name_a = "Pelaaja 1"
name_b = "Tietokone"
win_score = 3

# Maila A (pelaaja)
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Maila B (AI)
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# Pallo
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

# -------- PLAYER INPUT (P1 only) --------
move_a_up = False
move_a_down = False

def a_up_press():
    global move_a_up
    move_a_up = True

def a_up_release():
    global move_a_up
    move_a_up = False

def a_down_press():
    global move_a_down
    move_a_down = True

def a_down_release():
    global move_a_down
    move_a_down = False

wn.listen()
wn.onkeypress(a_up_press, "w")
wn.onkeyrelease(a_up_release, "w")
wn.onkeypress(a_down_press, "s")
wn.onkeyrelease(a_down_release, "s")

# -------- BALL RESET --------
def reset_ball():
    ball.goto(0, 0)
    ball.dx = 0
    ball.dy = 0

    def restart():
        ball.dx = random.choice([-3, 3])
        ball.dy = random.choice([-3, 3])

    wn.ontimer(restart, 500)

# -------- AI SETTINGS --------
ai_speed = 6          # difficulty
ai_error = 8          # bigger = more human mistakes

# -------- GAME LOOP --------
def game_loop():
    global score_a, score_b

    wn.update()

    # Player movement
    paddle_speed = 8

    if move_a_up:
        paddle_a.sety(paddle_a.ycor() + paddle_speed)
    if move_a_down:
        paddle_a.sety(paddle_a.ycor() - paddle_speed)

    # -------- AI (Paddle B) --------
    # Add "imperfect tracking"
    target_y = ball.ycor() + random.randint(-ai_error, ai_error)

    if paddle_b.ycor() < target_y - 10:
        paddle_b.sety(paddle_b.ycor() + ai_speed)
    elif paddle_b.ycor() > target_y + 10:
        paddle_b.sety(paddle_b.ycor() - ai_speed)

    # Ball movement
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Top/bottom wall
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1

    # Score right (AI misses)
    if ball.xcor() > 390:
        score_a += 1
        update_score()
        reset_ball()

    # Score left (player misses)
    if ball.xcor() < -390:
        score_b += 1
        update_score()
        reset_ball()

    # Paddle B collision (AI)
    if (340 < ball.xcor() < 350) and (paddle_b.ycor() - 50 < ball.ycor() < paddle_b.ycor() + 50):
        ball.setx(340)
        ball.dx *= -1.1

    # Paddle A collision (player)
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

# Start game
game_loop()
wn.mainloop()