# # from tkinter import *

# # root = Tk()
# # root.title("Testing")

# # def myClick():
# #     myLabel = Label(root, text = "Christmas!!", fg = "blue")
# #     myLabel.pack()

# # myButton = Button(root, text = "Buttttooooonnn", padx = 30, pady = 20, command = myClick, fg = "red", bg = "green")
# # myButton.pack()

# # root.mainloop()



from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import random

# print(plt.syle.available)
plt.style.use('fivethirtyeight')

ages_x = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
dev_y = [38496, 42000, 46752, 49320, 53200, 56000, 62316, 64928, 67317, 68748, 73752]

py_dev_y = [45372, 48876, 53850, 57287, 63016, 65998, 70003, 70000, 71496, 75370, 83640]

js_dev_y = [37810, 43515, 46823, 49293, 53437, 56373, 62375, 66674, 68745, 68746, 74583]

plt.plot(ages_x, py_dev_y, color = 'b', marker = 'o', linewidth = 3, label = 'Python')
plt.plot(ages_x, js_dev_y, color = 'r', marker = '.', linewidth = 3, label = 'JavaScript')
plt.plot(ages_x, dev_y, color = '#444444', linestyle = '--', label = 'All Devs')

plt.xlabel('Ages (years)')
plt.ylabel('Median Salary (USD)')
plt.title('Median Salary (USD) by Age')

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.show()

# time_vals = []
# y_vals = []

# startTime = time.time()

# def getTimeElapsed():
#     elapsed = time.time() - startTime
#     return elapsed


# def animate(i):
#     time_vals.append(getTimeElapsed())
#     y_vals.append(random.randint(0,10))

#     plt.cla()
#     plt.plot(time_vals, y_vals)

# ani = FuncAnimation(plt.gcf(), animate, interval = 1000)

# plt.tigh_layout()
# plt.show()