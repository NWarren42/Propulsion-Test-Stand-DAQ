from tkinter import *

root = Tk()

def myClick():
    myLabel = Label(root, text = "Christmas!!", fg = "blue")
    myLabel.pack()

myButton = Button(root, text = "Buttttooooonnn", command = myClick, fg = "red", bg = "green")
myButton.pack()


root.mainloop()
