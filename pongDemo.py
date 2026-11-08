import turtle

# --- Screen Setup ---
win = turtle.Screen()
win.title("Pong")
win.bgcolor("black")
win.setup(width=800, height=600)
win.tracer(0)  # Stops screen from updating automatically (speeds up game)

# --- Game Objects Function ---
def create_sprite(shape, color, x, y, stretch_w=1, stretch_len=1):
    sprite = turtle.Turtle()
    sprite.speed(0)
    sprite.shape(shape)
    sprite.color(color)
    sprite.shapesize(stretch_wid=stretch_w, stretch_len=stretch_len)
    sprite.penup()
    sprite.goto(x, y)
    return sprite

# Create paddles and ball
paddle_a = create_sprite("square", "white", -350, 0, stretch_w=5, stretch_len=1)
paddle_b = create_sprite("square", "white", 350, 0, stretch_w=5, stretch_len=1)
ball = create_sprite("circle", "white", 0, 0)
ball.dx = 0.2  # Ball speed X
ball.dy = 0.2  # Ball speed Y

# --- Scoreboard ---
score_a, score_b = 0, 0
pen = create_sprite("square", "white", 0, 260)
pen.hideturtle()
pen.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))

# --- Movement Functions ---
def paddle_a_up(): paddle_a.sety(min(250, paddle_a.ycor() + 20))
def paddle_a_down(): paddle_a.sety(max(-250, paddle_a.ycor() - 20))
def paddle_b_up(): paddle_b.sety(min(250, paddle_b.ycor() + 20))
def paddle_b_down(): paddle_b.sety(max(-250, paddle_b.ycor() - 20))

# --- Key Bindings ---
win.listen()
win.onkeypress(paddle_a_up, "w")
win.onkeypress(paddle_a_down, "s")
win.onkeypress(paddle_b_up, "Up")
win.onkeypress(paddle_b_down, "Down")

# --- Main Game Loop ---
while True:
    win.update()  # Manually update the screen

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Top and Bottom Border Collisions
    if ball.ycor() > 290 or ball.ycor() < -290:
        ball.dy *= -1

    # Left and Right Goal Collisions
    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_a += 1
        pen.clear()
        pen.write(f"Player A: {score_a}  Player B: {score_b}", align="center", font=("Courier", 24, "normal"))

    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_b += 1
        pen.clear()
        pen.write(f"Player A: {score_a}  Player B: {score_b}", align="center", font=("Courier", 24, "normal"))

    # Paddle and Ball Collisions
    if (340 < ball.xcor() < 350) and (paddle_b.ycor() - 50 < ball.ycor() < paddle_b.ycor() + 50):
        ball.setx(340)
        ball.dx *= -1

    if (-350 < ball.xcor() < -340) and (paddle_a.ycor() - 50 < ball.ycor() < paddle_a.ycor() + 50):
        ball.setx(-340)
        ball.dx *= -1