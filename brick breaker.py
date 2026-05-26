# ════════════════════════════════════════════
# 🧱 BRICK BREAKER
# LEFT / RIGHT or A / D — Move paddle
# SPACE — Launch ball
# Break all bricks to win!
# Press R to restart
# Press P to pause
# ════════════════════════════════════════════

import turtle
import random

# Screen
screen = turtle.Screen()
screen.setup(700, 650)
screen.bgcolor("#0f172a")
screen.title("🧱 Brick Breaker")
screen.tracer(0)


# HELPERS

def make_t(shape, color, x, y, sw=1.0, sh=1.0, visible=True):
    t = turtle.Turtle()
    t.shape(shape)
    t.color(color)
    t.shapesize(sh, sw)
    t.penup(); t.speed(0)
    t.goto(x, y)
    if not visible: t.hideturtle()
    return t

# Paddle
PADDLE_W  = 6.2   # shapesize width units
paddle    = make_t("square", "#4ade80", 0, -260, sw=PADDLE_W, sh=0.6)
PADDLE_STEP  = 40
PADDLE_LIMIT = 400 

# Ball 
ball    = make_t("circle", "white", 0, -240, sw=0.6, sh=0.6)
ball.dx = 0.0
ball.dy = 0.0
BALL_SPEED = 6.5
launched   = [False]

# HUD Pen 
hud = turtle.Turtle()
hud.hideturtle(); hud.penup(); hud.speed(0)

# Walls (visual)
wall_pen = turtle.Turtle()
wall_pen.hideturtle(); wall_pen.penup()
wall_pen.color("#334155"); wall_pen.pensize(4)
# Left
wall_pen.goto(-340, 300); wall_pen.pendown()
wall_pen.goto(-340, -300); wall_pen.penup()
# Right
wall_pen.goto(340, 300); wall_pen.pendown()
wall_pen.goto(340, -300); wall_pen.penup()
# Top
wall_pen.goto(-340, 300); wall_pen.pendown()
wall_pen.goto(340, 300); wall_pen.penup()

# ════════════════════════════════════════════
# BRICKS
# ════════════════════════════════════════════

BRICK_ROWS = 6
BRICK_COLS = 10
BRICK_W    = 5.8    # shapesize
BRICK_H    = 0.85
BRICK_START_Y = 210
BRICK_GAP_X   = 64
BRICK_GAP_Y   = 25

ROW_COLORS = [
    "#ef4444",   # Row 1 — Red     (3 hits)
    "#f97316",   # Row 2 — Orange  (2 hits)
    "#f59e0b",   # Row 3 — Yellow  (2 hits)
    "#22c55e",   # Row 4 — Green   (1 hit)
    "#3b82f6",   # Row 5 — Blue    (1 hit)
    "#a855f7",   # Row 6 — Purple  (1 hit)
]
ROW_HITS   = [3, 2, 2, 1, 1, 1]   # Hits needed per row

# Hit colors (progressively lighter)
HIT_COLORS = {
    3: "#ef4444",
    2: "#fca5a5",
    1: "#fee2e2",
}

bricks       = []    # list of turtle objects
brick_hits   = []    # remaining hits for each brick
brick_points = []    # points for each brick

def build_bricks():
    """Create all brick turtles and position them."""
    bricks.clear()
    brick_hits.clear()
    brick_points.clear()

    for row in range(BRICK_ROWS):
        color  = ROW_COLORS[row]
        hits   = ROW_HITS[row]
        pts    = hits * 10

        for col in range(BRICK_COLS):
            x = -288 + col * BRICK_GAP_X
            y = BRICK_START_Y - row * BRICK_GAP_Y

            b = make_t("square", color, x, y, sw=BRICK_W, sh=BRICK_H)
            bricks.append(b)
            brick_hits.append(hits)
            brick_points.append(pts)

# ── Score / Lives 
score   = [0]
lives   = [3]
level   = [1]
running = [True]
paused  = [False]

def draw_hud():
    hud.clear()
    hud.color("white")
    hud.goto(-330, 275)
    hud.write(f"Score: {score[0]}", font=("Arial", 12, "bold"))
    hud.color("#fbbf24")
    hud.goto(0, 275)
    hud.write(f"Level {level[0]}", align="center", font=("Arial", 12, "bold"))
    hud.color("#f87171")
    hud.goto(330, 275)
    hud.write("❤ " * lives[0], align="right", font=("Arial", 12, "bold"))

def launch_hint():
    hud.color("#64748b")
    hud.goto(0, -295)
    hud.write("← → Move   SPACE Launch   P Pause   R Restart",
              align="center", font=("Arial", 9, "normal"))

# ── Pause Toggle ──────────────────────────
def toggle_pause():
    if not running[0]:
        return

    paused[0] = not paused[0]
    if paused[0]:
        hud.goto(0, 0)
        hud.color("#fbbf24")
        hud.write("PAUSED", align="center", font=("Arial", 24, "bold"))
        screen.update()
    else:
        hud.clear()
        draw_hud()
        launch_hint()
        screen.update()
        game_loop()

# ── Ball Launch ───────────────────────────
def launch():
    if not launched[0]:
        ball.dx =  BALL_SPEED
        ball.dy =  BALL_SPEED
        launched[0] = True

# ── Paddle Move ───────────────────────────
def move_left():
    x = paddle.xcor()
    if x > -PADDLE_LIMIT + 60:
        paddle.setx(x - PADDLE_STEP)

def move_right():
    x = paddle.xcor()
    if x < PADDLE_LIMIT - 60:
        paddle.setx(x + PADDLE_STEP)

screen.listen()
screen.onkey(move_left,  "Left")
screen.onkey(move_right, "Right")
screen.onkey(move_left,  "a")
screen.onkey(move_right, "d")
screen.onkey(launch,     "space")
screen.onkey(toggle_pause, "p")
screen.onkey(toggle_pause, "P")

# ── Reset Ball Position ───────────────────
def reset_ball():
    ball.goto(paddle.xcor(), -225)
    ball.dx = 0.0
    ball.dy = 0.0
    launched[0] = False

# ── Game Over / Win ───────────────────────
def show_message(title, title_color, sub="Press  R  to Restart"):
    hud.clear()
    hud.color(title_color)
    hud.goto(0, 50)
    hud.write(title, align="center", font=("Arial", 30, "bold"))
    hud.color("white")
    hud.goto(0, 0)
    hud.write(f"Score: {score[0]}", align="center", font=("Arial", 16, "normal"))
    hud.color("#94a3b8")
    hud.goto(0, -45)
    hud.write(sub, align="center", font=("Arial", 12, "normal"))

# ── Next Level ────────────────────────────
def next_level():
    level[0] += 1
    hud.color("#4ade80")
    hud.goto(0, 20)
    hud.write(f"LEVEL {level[0]}!", align="center", font=("Arial", 30, "bold"))
    screen.update()

    def continue_game():
        hud.clear()
        build_bricks()
        reset_ball()
        draw_hud()
        launch_hint()
        game_loop()

    screen.ontimer(continue_game, 1500)

# ── Restart ───────────────────────────────
def restart():
    score[0]   = 0
    lives[0]   = 3
    level[0]   = 1
    running[0] = True
    paused[0]  = False

    for b in bricks:
        b.hideturtle()

    build_bricks()
    reset_ball()
    draw_hud()
    launch_hint()
    game_loop()

screen.onkey(restart, "r")
screen.onkey(restart, "R")

# ════════════════════════════════════════════
# MAIN GAME LOOP
# ════════════════════════════════════════════

def game_loop():
    if not running[0] or paused[0]:
        return

    # If ball not launched, stick to paddle
    if not launched[0]:
        ball.goto(paddle.xcor(), -225)
        screen.update()
        screen.ontimer(game_loop, 16)
        return

    # Move ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    bx = ball.xcor()
    by = ball.ycor()

    # ── Wall bounces ─────────────────────
    if bx > 328:  ball.setx(328); ball.dx *= -1
    if bx < -328: ball.setx(-328); ball.dx *= -1
    if by > 290:  ball.sety(290); ball.dy *= -1

    # ── Ball falls below paddle ───────────
    if by < -295:
        lives[0] -= 1
        draw_hud()
        if lives[0] <= 0:
            running[0] = False
            show_message("GAME OVER", "#f87171")
            screen.update()
            return
        reset_ball()
        screen.update()
        screen.ontimer(game_loop, 16)
        return

    # ── Paddle bounce ─────────────────────
    pw = PADDLE_W * 10   # paddle half-width in pixels
    if (paddle.xcor() - pw < bx < paddle.xcor() + pw and
            -265 < by < -250):
        ball.sety(-250)
        ball.dy = abs(ball.dy)   # Always bounce up
        # Angle based on hit position
        offset = (bx - paddle.xcor()) / pw
        ball.dx = BALL_SPEED * offset * 1.5

    # ── Brick collision ───────────────────
    for i, b in enumerate(bricks):
        if not b.isvisible():
            continue

        bk_x = b.xcor()
        bk_y = b.ycor()
        bk_hw = BRICK_W * 10     # half-width
        bk_hh = BRICK_H * 10 + 2  # half-height

        if (bk_x - bk_hw < bx < bk_x + bk_hw and
                bk_y - bk_hh < by < bk_y + bk_hh):

            brick_hits[i] -= 1

            if brick_hits[i] <= 0:
                # Brick destroyed
                score[0] += brick_points[i]
                b.hideturtle()
            else:
                # Brick damaged — change color
                b.color(HIT_COLORS.get(brick_hits[i], "white"))

            # Bounce ball
            ball.dy *= -1
            draw_hud()
            break

    # ── Check win — all bricks gone ───────
    if all(not b.isvisible() for b in bricks):
        running[0] = False
        next_level()
        return

    screen.update()
    screen.ontimer(game_loop, 16)

# ════════════════════════════════════════════
# START
# ════════════════════════════════════════════
build_bricks()
reset_ball()
draw_hud()
launch_hint()
game_loop()
turtle.done()
