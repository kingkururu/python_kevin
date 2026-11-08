# import turtle

# text = turtle.Turtle()
# text.hideturtle()
# text.penup()

# text.goto(0, 0)
# text.write("Hello World!", align="center", font=("Arial", 24, "bold"))

# turtle.done()

import turtle
import time
import random

# --------------------
# Variables
# --------------------
last_time = time.perf_counter()
gameEnd = False

# Keyboard state
up = False
down = False
left = False
right = False

# Sprite Settings
sballminx = -350
sballmaxx = 350
sballminy = -250
sballmaxy = 250

sballsize=1.2
lballsize=2

move_speed = 100  
paddle_speed = 200  # pixels per second

# --------------------
# Screen
# --------------------
screen = turtle.Screen()
screen.setup(800, 600)
screen.title("Game")
screen.tracer(0)

# --------------------
# Input Handling
# --------------------
keys = {}

def set_key(key, state):
    keys[key] = state

# Register all controls for both players dynamically
controls = ["Up", "Down", "Left", "Right", "w", "s", "a", "d"]

screen.listen()
for k in controls:
    screen.onkeypress(lambda k=k: set_key(k, True), k)
    screen.onkeyrelease(lambda k=k: set_key(k, False), k)

# --------------------
# Sprite Creation Helper Function
# --------------------
def create_sprite(shape, color, x, y, stretch_w=2, stretch_len=1):
    sprite = turtle.Turtle()
    sprite.speed(0)
    sprite.shape(shape)
    sprite.color(color)
    sprite.shapesize(stretch_wid=stretch_w, stretch_len=stretch_len)
    sprite.penup()
    sprite.goto(x, y)
    return sprite

def create_ball(shape, color, x, y, stretch_w=2, stretch_len=1, angle = 0):
    ball = create_sprite(shape, color, x, y, stretch_w, stretch_len)
    ball.setheading(random.randint(1,360))
    ball.hideturtle()
    return ball

def create_paddle(shape, color, x, y, stretch_w=2, stretch_len=1):
    paddle = create_sprite(shape, color, x, y, stretch_w, stretch_len)
    paddle.setheading(90)
    return paddle

# --------------------
# Sprite Creation
# --------------------

small_balls = []

for i in range(6):
    ball = create_ball("circle", "blue", random.randint(sballminx, sballmaxx), random.randint(sballminy, sballmaxy), sballsize, sballsize)
    small_balls.append(ball)

ball = create_ball("circle", "blue", random.randint(-350, 350), random.randint(-300,300), lballsize, lballsize)

gameoverball = create_ball("circle", "red", 0, 0, 2, 2, random.randint(1,120))

leftpaddle = create_paddle("square", "black", -400, 0, 1, 3)
rightpaddle = create_paddle("square", "black", 391, 0, 1, 3)

# --------------------
# Sprite Movement Helper Functions
# --------------------
def collision_with_paddle(ball, paddle):
    if ball.distance(paddle) < 50:
       return True
    return False

def move_ball(ball, speed, dt, paddle=None, paddle2=None):
    ball.showturtle()
    ball.forward(speed * dt)

    if ball.ycor() < -270 or ball.ycor() > 270:
        ball.setheading(-ball.heading())

    if paddle is not None and collision_with_paddle(ball, paddle) or (paddle2 is not None and collision_with_paddle(ball, paddle2)):
        # Bounce off walls
        if ball.xcor() < -370 or ball.xcor() > 370:
            ball.setheading(180 - ball.heading())

# --------------------
# Game Loop
# --------------------

def game_loop():
    global last_time, gameEnd

    current_time = time.perf_counter()
    dt = current_time - last_time
    last_time = current_time

    ball.forward(move_speed * dt)

    move_ball(ball, move_speed, dt, leftpaddle, rightpaddle)

    # Paddle Movement
    if keys.get("w"):
        leftpaddle.forward(paddle_speed * dt)

    if keys.get("s"):
        leftpaddle.backward(paddle_speed * dt)

    if keys.get("Up"):
        rightpaddle.forward(paddle_speed * dt)

    if keys.get("Down"):
        rightpaddle.backward(paddle_speed * dt)

    screen.update()

    if not gameEnd:
        screen.ontimer(game_loop, 16)

# --------------------
# Run the game
# --------------------
game_loop()
turtle.done()