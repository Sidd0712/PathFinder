from functools import partial
from time import sleep
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

from runner import Runner

window = Tk()
window.title("Pathfinder")
window.config(padx=50, pady=50 , bg="black")
window.state("zoomed")
square = 8

START = 0
WALL = 1
END = 2
NONE = -1
block = [[0 for _ in range(square)] for _ in range(square)]
block_value = [[NONE for _ in range(square)] for _ in range(square)]
mode = START
startTaken = False
startValue = (-1, -1)
endTaken = False
endValue = (-1, -1)


def resize_image(image_path, width, height):
    image = Image.open(image_path)
    image = image.resize((width, height), Image.ANTIALIAS)
    return ImageTk.PhotoImage(image)


img_u = resize_image("arrow_up.png", 74, 80)
img_d = resize_image("arrow_down.png", 74, 80)
img_l = resize_image("arrow_left.png", 74, 80)
img_r = resize_image("arrow_right.png", 74, 80)


def clicked(button):
    global mode
    reset()
    if button == "start":
        button_border[0].config(highlightbackground="white")
        button_border[1].config(highlightbackground="black")
        button_border[2].config(highlightbackground="black")
        mode = START
    elif button == "wall":
        button_border[0].config(highlightbackground="black")
        button_border[1].config(highlightbackground="white")
        button_border[2].config(highlightbackground="black")
        mode = WALL
    else:
        button_border[0].config(highlightbackground="black")
        button_border[1].config(highlightbackground="black")
        button_border[2].config(highlightbackground="white")
        mode = END


def block_clicked(i, j):
    global startTaken, startValue, endValue, endTaken
    reset()
    if mode == START:
        if block_value[i][j] == START:
            block[startValue[0]][startValue[1]].config(bg="white")
            block_value[startValue[0]][startValue[1]] = NONE
            startTaken = False
            startValue = (-1, -1)
            return
        if startTaken:
            block[startValue[0]][startValue[1]].config(bg="white")
            block_value[startValue[0]][startValue[1]] = NONE
            startTaken = False
            startValue = (-1, -1)
        if block_value[i][j] == END:
            endTaken = False
            endValue = (-1, -1)
        block[i][j].config(bg="green")
        block_value[i][j] = START
        startTaken = True
        startValue = (i, j)
    elif mode == WALL:
        if block_value[i][j] == WALL:
            block[i][j].config(bg="white")
            block_value[i][j] = NONE
            return
        if block_value[i][j] == START:
            startTaken = False
            startValue = (-1, -1)
        if block_value[i][j] == END:
            endTaken = False
            endValue = (-1, -1)
        block[i][j].config(bg="grey")
        block_value[i][j] = WALL
    else:
        if block_value[i][j] == END:
            block[endValue[0]][endValue[1]].config(bg="white")
            block_value[endValue[0]][endValue[1]] = NONE
            endTaken = False
            endValue = (-1, -1)
            return
        if endTaken:
            block[endValue[0]][endValue[1]].config(bg="white")
            block_value[endValue[0]][endValue[1]] = NONE
            endTaken = False
            endValue = (-1, -1)
        if block_value[i][j] == START:
            startTaken = False
            startValue = (-1, -1)
        block[i][j].config(bg="red")
        block_value[i][j] = END
        endTaken = True
        endValue = (i, j)


def highlight(path):

    prev_x = startValue[0]
    prev_y = startValue[1]
    for item in path:
        x = int(item / square)
        y = item % square
        if y == prev_y:
            if x < prev_x:
                block[x][y].config(image=img_u, width=img_u.width(), height=img_u.height())
            else:
                block[x][y].config(image=img_d, width=img_d.width(), height=img_d.height())
        else:
            if y < prev_y:
                block[x][y].config(image=img_l, width=img_l.width(), height=img_l.height())
            else:
                block[x][y].config(image=img_r, width=img_r.width(), height=img_r.height())
        prev_x = x
        prev_y = y
        window.update()
        sleep(0.2)


def reset():
    for i in range(square):
        for j in range(square):
            if block_value[i][j] == NONE:
                block[i][j].config(bg="white", image="", width=10, height=5)
                block_value[i][j] = NONE


def resetAll():
    for i in range(square):
        for j in range(square):
            block[i][j].config(bg="white", image="", width=10, height=5)
            block_value[i][j] = NONE


def findPath():
    if startTaken and endTaken:
        run = Runner(block_value, square)
        run.mapSetUp()
        route = run.startRunning()
        if not route:
            messagebox.showerror("Error!", "No path found!")
            return
        route.pop(0)
        route.pop(len(route) - 1)
        highlight(route)


for i in range(square):
    for j in range(square):
        block[i][j] = Button(image="", bg="white", width=10, height=5, bd=1, command=partial(block_clicked, i, j))
        block[i][j].grid(row=i, column=j)

button_border = [Frame(highlightbackground="white", highlightthickness=2, bd=0) for x in range(3)]

btn_start = Button(button_border[0], text="Start", width=10, height=5, bg="green", bd=0, command=partial(clicked,
                                                                                                         "start"))
btn_start.pack()
button_border[0].grid(row=1, column=square, rowspan=2, padx=(250, 20))

btn_wall = Button(button_border[1], text="Wall", width=10, height=5, bg="grey", bd=0, command=partial(clicked,
                                                                                                      "wall"))
btn_wall.pack()
button_border[1].grid(row=1, column=square + 1, rowspan=2, padx=20)

btn_end = Button(button_border[2], text="End", width=10, height=5, bg="red", bd=0, command=partial(clicked,
                                                                                                   "end"))
btn_end.pack()
button_border[2].grid(row=1, column=square + 2, rowspan=2, padx=(20, 0))

button_border[1].config(highlightbackground="black")
button_border[2].config(highlightbackground="black")

btn_find = Button(text="Run PathFinder", width=45, height=5, bg="white", highlightbackground="black", highlightthickness=2, bd=0, command=findPath)
btn_find.grid(row=3, column=square, rowspan=2, columnspan=3, padx=(250, 0))

btn_reset = Button(text="Reset", width=45, height=5, bg="grey",highlightbackground="black", highlightthickness=2, bd=0, command=resetAll)
btn_reset.grid(row=4, column=square, rowspan=2, columnspan=3, padx=(250, 0), pady=(45, 0))

window.mainloop()
