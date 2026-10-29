import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import random

N_korak = 200000
x_lista, y_lista = [], []
x, y = 0, 0

for i in range(1, N_korak):
    x_lista.append(x)
    y_lista.append(y)
    r = random.random()
    xp = x

    if r <= 0.1:
        x = 0.05 * xp
        y = 0.6 * y
    elif r <= 0.2:
        x = 0.05 * xp
        y = -0.5 * y + 1
    elif r <= 0.4:
        x = 0.46 * xp - 0.15 * y
        y = 0.39 * xp + 0.38 * y + 0.6
    elif r <= 0.6:
        x = 0.47 * xp - 0.15 * y
        y = 0.17 * xp + 0.42 * y + 1.1
    elif r <= 0.8:
        x = 0.43 * xp + 0.28 * y
        y = -0.25 * xp + 0.45 * y + 1
    elif r <= 1:
        x = 0.42 * xp + 0.26 * y
        y = -0.35 * xp + 0.31 * y + 0.7

with open("tree-100(b).txt", "w") as f:
    f.write("k\tx\t\ty\n")
    for k, (x, y) in enumerate(zip(x_lista[:100], y_lista[:100]), start=1):
        f.write(f"{k}\t{x}\t{y}\n")

fig, ax = plt.subplots()
ax.set_xlim(min(x_lista), max(x_lista))
ax.set_ylim(min(y_lista), max(y_lista))
ax.set_title('Stablo: N=100')
line, = ax.plot([], [], 'g-')

#animacija
def update(frame):
    line.set_data(x_lista[:frame], y_lista[:frame])
    return line,

ani = animation.FuncAnimation(fig, update, frames=100, interval=50, blit=True)
ani.save("sim_100_koraka(b).gif", writer=animation.PillowWriter(fps=5))

plt.show()

fig, ax = plt.subplots()
ax.set_xlim(min(x_lista), max(x_lista))
ax.set_ylim(min(y_lista), max(y_lista))
ax.set_title('Stablo: N = 200 000')
scatter = ax.scatter([], [], c='g', s=0.5)

def update(frame):
    scatter.set_offsets(np.c_[x_lista[:frame], y_lista[:frame]]) 
    return scatter,

f = range(0,len(x_lista), 3000)
ani = animation.FuncAnimation(fig, update, frames=f, interval=1, blit=True)

ani.save("stablo_1.2b.gif", writer=animation.PillowWriter(fps=30))
plt.savefig("stablo_1.2b.png", dpi=300)
plt.show()
print('Gotovo')