# # from tkinter import *

# # root = Tk()
# # root.title("Testing")

# # def myClick():
# #     myLabel = Label(root, text = "Christmas!!", fg = "blue")
# #     myLabel.pack()

# # myButton = Button(root, text = "Buttttooooonnn", padx = 30, pady = 20, command = myClick, fg = "red", bg = "green")
# # myButton.pack()

# # root.mainloop()



# from matplotlib import pyplot as plt
# from matplotlib.animation import FuncAnimation
# import time
# import random
# import numpy as np

# print(plt.syle.available)
# plt.style.use('fivethirtyeight')

# ages_x = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
# dev_y = [38496, 42000, 46752, 49320, 53200, 56000, 62316, 64928, 67317, 68748, 73752]

# py_dev_y = [45372, 48876, 53850, 57287, 63016, 65998, 70003, 70000, 71496, 75370, 83640]

# js_dev_y = [37810, 43515, 46823, 49293, 53437, 56373, 62375, 66674, 68745, 68746, 74583]

# plt.plot(ages_x, py_dev_y, color = 'b', marker = 'o', linewidth = 3, label = 'Python')
# plt.plot(ages_x, js_dev_y, color = 'r', marker = '.', linewidth = 3, label = 'JavaScript')
# plt.plot(ages_x, dev_y, color = '#444444', linestyle = '--', label = 'All Devs')

# plt.xlabel('Ages (years)')
# plt.ylabel('Median Salary (USD)')
# plt.title('Median Salary (USD) by Age')

# plt.legend()

# plt.grid(True)

# plt.tight_layout()

# plt.show()

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import random
import numpy as np

fig, axs = plt.subplots(2, 2)

for ax in axs.flat:
    ax.set(xlabel='x-label', ylabel='y-label')

time_vals = []
y_vals_1 = []
y_vals_2 = []
y_vals_3 = []
y_vals_4 = []

y_values = [y_vals_1, y_vals_2, y_vals_3, y_vals_4]

startTime = time.time()
num_subplots = 4
num = 0

for ax in axs.flat:
    ax.set(xlabel = 'x-label', ylabel = 'y-label')

def getTimeElapsed():
    elapsed = time.time() - startTime
    return elapsed

data1 = random.randint(0,10)
data2 = random.randint(10,20)
data3 = random.randint(20,30)
data4 = random.randint(30,40)

def getData(a,b):
    data = random.randint(a,b)
    return data



def animate(i):
    time_vals.append(getTimeElapsed())
    y_values[0].append(random.randint(0,10))
    y_values[1].append(random.randint(10,20))
    y_values[2].append(random.randint(20,30))
    y_values[3].append(getData(0,100))

    for j in range(num_subplots):
        axs.flat[j].clear()
        axs.flat[j].plot(time_vals[:i+1], y_values[j][:i+1])

ani = FuncAnimation(fig, animate, interval = 100)

plt.tight_layout()
plt.show()