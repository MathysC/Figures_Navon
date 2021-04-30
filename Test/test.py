from tkinter import *
from functools import partial

def main():
    master = Tk()
    # Right side of the screen / img holder
    right_frame = Frame(master, width=500, height=500, cursor="dot")
    right_frame.pack(side=LEFT)

    # Create canvas
    canvas = Canvas(right_frame, width=800, height=700)
    #canvas.create_image(0, 0, image=photo, anchor="nw")
    canvas.pack()
    canvas.bind("<B1-Motion>", partial(paint, canvas))
    message = Label(right_frame, text="Press the mouse to draw")
    message.pack(side=BOTTOM)

    mainloop()

def paint(canvas, event):
    python_green = "#476042"
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    canvas.create_oval(x1, y1, x2, y2, fill=python_green)

if __name__ == "__main__":
    main()