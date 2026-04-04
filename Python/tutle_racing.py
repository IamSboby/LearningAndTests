import turtle
import random
import time

#Constants
WIDTH,  HEIGHT  = 900, 580
START_X, FINISH_X = -340, 340

COLORS = ['red', 'dodger blue', 'lime green', 'orange', 'orchid']
NAMES  = ['Red', 'Blue', 'Green', 'Orange', 'Purple']
N      = len(NAMES)

LANE_TOP = 220
LANE_BOT = -220
LANE_H   = (LANE_TOP - LANE_BOT) // N   # lane height


# Graphics setup

def setup_screen():
    sc = turtle.Screen()
    sc.setup(WIDTH, HEIGHT)
    sc.title("Turtle Race")
    sc.bgcolor('#2d6a2d')   # field green
    sc.tracer(0)
    return sc


def draw_field():
    """The referee (white turtle) moves across the field and draws it."""
    ref = turtle.Turtle()
    ref.shape('turtle')
    ref.color('white')
    ref.pensize(2)
    ref.speed(4)  # visible speed – referee animation

    #outer border
    corners = [
        (START_X,  LANE_BOT),
        (FINISH_X, LANE_BOT),
        (FINISH_X, LANE_TOP),
        (START_X,  LANE_TOP),
        (START_X,  LANE_BOT),
    ]
    ref.penup()
    ref.goto(corners[0])
    ref.pendown()
    for pt in corners[1:]:
        ref.goto(pt)

    #lane lines
    for i in range(1, N):
        y = LANE_BOT + i * LANE_H
        ref.penup();  ref.goto(START_X, y)
        ref.pendown(); ref.goto(FINISH_X, y)

    # start line (yellow)
    ref.color('yellow');  ref.pensize(4)
    ref.penup();  ref.goto(START_X, LANE_BOT)
    ref.pendown(); ref.goto(START_X, LANE_TOP)

    # checkered finish line (black/white)
    ref.pensize(1)
    sq = 18
    cols_check = ['white', 'black']
    for row in range((LANE_TOP - LANE_BOT) // sq):
        for col in range(2):
            cx = FINISH_X + col * sq
            cy = LANE_BOT + row * sq
            ref.penup(); ref.goto(cx, cy); ref.pendown()
            ref.color(cols_check[(row + col) % 2])
            ref.begin_fill()
            for _ in range(4):
                ref.forward(sq); ref.left(90)
            ref.end_fill()

    # labels 
    def label(x, y, txt, col='white', size=13):
        lbl = turtle.Turtle()
        lbl.hideturtle(); lbl.penup()
        lbl.color(col); lbl.goto(x, y)
        lbl.write(txt, align='center', font=('Arial', size, 'bold'))

    label(START_X,       LANE_TOP + 10, 'START',  'yellow', 14)
    label(FINISH_X + 18, LANE_TOP + 10, 'FINISH', 'yellow', 14)

    ref.hideturtle()


def place_turtles():
    """Places turtles in lanes with labels."""
    racers = []
    for i, (col, name) in enumerate(zip(COLORS, NAMES)):
        y = LANE_BOT + (i + 0.5) * LANE_H

        # name label on the left
        lbl = turtle.Turtle()
        lbl.hideturtle(); lbl.penup()
        lbl.color(col)
        lbl.goto(START_X - 60, y - 8)
        lbl.write(name, align='right', font=('Arial', 10, 'bold'))

        # racing turtle
        t = turtle.Turtle()
        t.shape('turtle')
        t.color(col)
        t.penup()
        t.goto(START_X + 25, y)
        t.setheading(0)
        racers.append(t)

    return racers


# Race logic
def run_race(racers, screen):
    """
    5 speed changes: each phase assigns random speeds to all turtles.
    The race ends when all cross the finish line.
    """
    SPEED_CHANGES = 5
    STEPS_PER_PHASE = 90

    speeds       = [random.uniform(2, 10) for _ in racers]
    finished     = [False] * N
    finish_order = []
    phase = 0
    step  = 0

    while len(finish_order) < N:

        # speed change
        if step % STEPS_PER_PHASE == 0 and phase < SPEED_CHANGES:
            speeds = [random.uniform(2, 10) for _ in racers]
            phase += 1
            print(f"   Speed change #{phase}!")

        # move each turtle
        for i, t in enumerate(racers):
            if not finished[i]:
                t.forward(speeds[i])
                if t.xcor() >= FINISH_X:
                    finished[i] = True
                    finish_order.append(i)
                    print(f"   {NAMES[i]} reached the finish line! ({len(finish_order)})")

        screen.update()
        step += 1

    return finish_order


#CLI + main 

def main():
    #  CLI presentation 
    print()
    print("==========================================")
    print("           TURTLE RACE                    ")
    print("==========================================")
    print("  Turtles in the race:")
    for i, (name, col) in enumerate(zip(NAMES, COLORS), 1):
        row = f"  [{i}]  {name:<10}  ({col})"
        print(row)
    print("==========================================")

    # ── bet ──
    while True:
        try:
            scelta = int(input("\nWhich turtle do you bet on? (1-5): ")) - 1
            if 0 <= scelta < N:
                break
            print("   Choose a number between 1 and 5.")
        except ValueError:
            print("   Enter a valid integer.")

    print(f"\nYou chose: {NAMES[scelta].upper()} ({COLORS[scelta]})")
    print("\nThe referee is preparing the field...")

    # ── graphics ──
    screen = setup_screen()
    draw_field()
    screen.update()
    time.sleep(0.4)

    racers = place_turtles()
    screen.update()

    input("\nPress ENTER to start the race...\n")
    print("-" * 44)

    finish_order = run_race(racers, screen)

    # ── results ──
    medals = ['1st', '2nd', '3rd', '4th', '5th']

    print()
    print("==========================================")
    print("           FINAL RESULTS                  ")
    print("==========================================")
    for pos, idx in enumerate(finish_order):
        row = f"{medals[pos]}   {NAMES[idx]:<10}  ({COLORS[idx]})"
        print(row)
    print("==========================================")

    my_pos = finish_order.index(scelta)
    winner = finish_order[0]

    if my_pos == 0:
        result = f"Well done! {NAMES[scelta]} WON! Great choice!"
    else:
        result = f"{NAMES[winner]} won. Yours finished {my_pos+1}."

    print(result)
    print("\n[Close the race window to exit]\n")

    screen.mainloop()


if __name__ == "__main__":
    main()