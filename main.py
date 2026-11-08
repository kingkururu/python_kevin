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

move_speed = 155
paddle_speed = 320  # pixels per second

Lscore=0
Rscore=0

# --------------------
# Screen
# --------------------
screen = turtle.Screen()
screen.setup(800, 600)
screen.title("Game")
screen.tracer(0)

# --------------------
# Helper Function
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

def create_ball(shape, color, x, y, stretch_w=2, stretch_len=1,angle = 0):
    ball = create_sprite(shape, color, x, y, stretch_w, stretch_len)
    ball.setheading(random.randint(0,360))
    ball.hideturtle()
    return ball

def create_paddle(shape, color, x, y, stretch_w=2, stretch_len=1):
    paddle = create_sprite(shape, color, x, y, stretch_w, stretch_len)
    paddle.setheading(90)
    paddle.showturtle()
    return paddle

# --------------------
# Sprite Creation
# --------------------
small_balls = []

for i in range (3):
    ball=create_ball("circle", "blue", random.randint(sballminx,  sballmaxx), random.randint(sballminy, sballmaxy), sballsize, sballsize)
    small_balls.append(ball)

ball = create_ball("circle", "blue", 0,0, lballsize, lballsize)

gameoverball = create_ball("circle", "red", 0, 0, 2, 2, random.randint(1,120))

leftpaddle = create_paddle("square", "black", -400, 0, 1, 3)
rightpaddle = create_paddle("square", "black", 391, 0, 1, 3)

endingtext = turtle.Turtle()
endingtext.penup()
endingtext.goto(0,100)
endingtext.color("cyan")
endingtext.hideturtle()

scoretext = turtle.Turtle()
scoretext.hideturtle()
scoretext.penup()
scoretext.goto(0, 210)

# Add this new function
def update_score():
    scoretext.clear() # Erase the old score
    # Use an f-string (the 'f' before the quotes) to insert the variables
    scoretext.write(f"LScore: {Lscore}   RScore: {Rscore}", align="center", font=("Arial", 24, "bold"))

# Call it once so the score shows up at the very beginning
update_score()

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

def collision_with_paddleL(ball, paddle):
    global Lscore
    # Only trigger if distance is < 30 AND the ball is moving left (heading between 90 and 270)
    if ball.distance(paddle) < 30 and (90 < ball.heading() < 270):
        Lscore = Lscore + 1
        update_score()
        return True
    return False

def collision_with_paddleR(ball, paddle):
    global Rscore
    # Only trigger if distance is < 30 AND the ball is moving right (heading < 90 or > 270)
    if ball.distance(paddle) < 30 and (ball.heading() < 90 or ball.heading() > 270):
        Rscore = Rscore + 1
        update_score()
        return True
    return False

def move_ball(ball, speed, dt, leftpaddle, rightpaddle):
    ball.showturtle()
    ball.forward(speed * dt)

    # Top and bottom wall bounce
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.setheading(-ball.heading())

    # Paddle bounce
    if leftpaddle is not None and collision_with_paddleL(ball, leftpaddle):
        ball.setheading(180 - ball.heading())
        return True

    elif rightpaddle is not None and collision_with_paddleR(ball, rightpaddle):
        ball.setheading(180 - ball.heading())
        return True

    return False

def endpage(ball, speed, dt, leftpaddle, rightpaddle):
    if ball.xcor() > 400 and not collision_with_paddleR(ball, rightpaddle):
        return True
    if ball.xcor() < -400 and not collision_with_paddleL(ball, leftpaddle):
        return True
    return False
        
def scene2(Rscore, Lscore):
    if Rscore>2 or Lscore>2:
        return True
    return False
    
# --------------------
# Game Loop
# --------------------
def game_loop():
    global last_time, gameEnd

    current_time = time.perf_counter()
    dt = current_time - last_time
    last_time = current_time

    # Paddle Movement
    if keys.get("w"):
        leftpaddle.forward(paddle_speed * dt)

    if keys.get("s"):
        leftpaddle.backward(paddle_speed * dt)

    if keys.get("Up"):
        rightpaddle.forward(paddle_speed * dt)

    if keys.get("Down"):
        rightpaddle.backward(paddle_speed * dt)

    # Big blue ball from scene 1
    move_ball(ball, move_speed, dt, leftpaddle, rightpaddle)

    # Scene 2
    if scene2(Rscore, Lscore):
        # Small blue balls: game over if any ball is missed
        for i in range(3):
            move_ball(small_balls[i], move_speed, dt, leftpaddle, rightpaddle)

            if endpage(small_balls[i], move_speed, dt, leftpaddle, rightpaddle):
                gameEnd = True

        # Red ball: game over if either player bounces it
        if move_ball(gameoverball, move_speed, dt, leftpaddle, rightpaddle):
            gameEnd = True

    # Big blue ball can still end the game if missed
    if endpage(ball, move_speed, dt, leftpaddle, rightpaddle):
        gameEnd = True

    if gameEnd:
        endingtext.write("gameover", align="center", font=("Arial", 50, "bold"))

    screen.update()

    if not gameEnd:
        screen.ontimer(game_loop, 16)

# --------------------
# Run the game
# --------------------
game_loop()
turtle.done()