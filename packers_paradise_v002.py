#   A simple game designed to practice Tkinter and python.

from tkinter import *
from tkinter import ttk
from random import randint
root = Tk()

canvas_width = 500
canvas_height = 800

root.title("Packer's Paradise")
root.resizable(False, False)

w = Canvas(root, width = canvas_width, height = canvas_height)
w.pack()

# Score area
w.create_rectangle(401, 5, 500, 800, fill = 'grey'  )
score_label = w.create_text(
    (410, 10), font=('Helvetica', 24, 'bold'),
    text = 'SCORE', anchor = 'nw')
level_label = w.create_text(
    (410, 110), font=('Helvetica', 24, 'bold'),
    text = 'LEVEL', anchor = 'nw')
lines_label = w.create_text(
    (410, 210), font=('Helvetica', 24, 'bold'),
    text = 'LINES', anchor = 'nw')
score_value = w.create_text(
    (490, 50), font=('Helvetica', 24, 'bold'),
    text = '0', anchor = 'ne')
level_value = w.create_text(
    (490, 150), font=('Helvetica', 24, 'bold'),
    text = '1', anchor = 'ne')
lines_value = w.create_text(
    (490, 250), font=('Helvetica', 24, 'bold'),
    text = '0', anchor = 'ne')

# Score display
lines = 0
level = 0
score = 0

drop_rate = 24 # Larger is faster; use only 2,4,6,8,12,16,24

def update_score():
    global lines
    global level
    global score
    global drop_rate

    lines += 1
    #if lines > 9 and lines < 20:
    #    drop_rate = 12
    #if lines > 19 and lines < 30:
    #    drop_rate = 16
    #if lines > 29:
    #    drop_rate = 24

    level = int(drop_rate/2)
    score = int(lines * level)

    w.itemconfig(score_value, text = score)
    w.itemconfig(level_value, text = level)
    w.itemconfig(lines_value, text = lines)

# Shape dropping function
def drop_shape():

    # Randomly place next block at top of screen
    shape_start_x_position = (randint(0,7) * 48) + 10

    # define shape
    a = shape_start_x_position
    b = -47
    c = shape_start_x_position + 47
    d = 0
    shape1 = w.create_rectangle(a, b, c, d, fill = 'green', tags='block')

    global drop_rate
    height = int(48 / drop_rate)

    stop_position = int((800)/drop_rate)
    for x in range(stop_position):

        w.move(shape1, 0, drop_rate)

        current_position = w.coords(shape1)
        next_position_overlap = w.find_overlapping(
            current_position[0], (current_position[1]),
            current_position[2], (current_position[3]+1))

        if len(next_position_overlap) > 1:
            break

        # Stop blocks from dropping off canvas bottom
        if (current_position[3] + 48) > 840:
            break

        def leftKey(event):
            # Prevent moving off left canvas edge, stop ability to move at end
            if w.coords(shape1)[0] > 10:
                overlap = w.find_overlapping(
                    w.coords(shape1)[0]-1, w.coords(shape1)[1],
                    w.coords(shape1)[2], w.coords(shape1)[3]+1)
                if len(overlap) < 2:
                    w.move(shape1, -48, 0)

        def rightKey(event):
            # Prevent moving off right canvas edge, stop ability to move at end
            if w.coords(shape1)[0] < 320:
                overlap = w.find_overlapping(
                    w.coords(shape1)[0], w.coords(shape1)[1],
                    w.coords(shape1)[2]+1, w.coords(shape1)[3]+1)
                if len(overlap) < 2:
                    w.move(shape1, 48, 0)

        def downKey(event):
            if w.coords(shape1)[3] < 750:
                overlap = w.find_overlapping(
                    w.coords(shape1)[0], w.coords(shape1)[1],
                    w.coords(shape1)[2], (w.coords(shape1)[3] + 1))
                if len(overlap) < 2:
                    w.move(shape1, 0, 48)

        root.bind('<Left>', leftKey)
        root.bind('<Right>', rightKey)
        root.bind('<Down>', downKey)

        root.update()

    # If row completed, delete row, add points and shift everything down
    row_level = 766
    overlap = w.find_overlapping(10, row_level, 394, row_level)
    if len(overlap) > 7:
        update_score()
        for shape in overlap:
            w.delete(shape)
        w.move('block', 0, 48)

for number in range(400):
    overlap = w.find_overlapping(10, 10, 400, 11)
    if len(overlap) > 0:
        w.create_rectangle(15, 350, 390, 450, fill = 'white'  )
        game_label = w.create_text(
            (70, 380), font=('Helvetica', 40, 'bold'),
            text = 'GAME OVER!', anchor = 'nw')
        break
    drop_shape()
root.mainloop()
