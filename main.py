import tkinter as tk
import dijkstra

# Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 600

# functions
def run_algorithm():
    if (algorithm.get() == 0):
        dijkstra.dijkstra(speed.get())
    elif (algorithm.get() == 1):
        return

# screen
screen = tk.Tk()
screen.title('Pathfinding Visualizer')

canvas = tk.Canvas(screen, height=SCREEN_HEIGHT, width=SCREEN_WIDTH)
canvas.pack()

# how to use text
T = tk.Text(screen, height=10, width=60)
T.place(anchor=tk.CENTER, relx=0.5, rely=0.2)
T.insert(tk.END, "How to use:\n" + \
            " 1. Select the algorithm and speed you wish to have\n" + \
            " 2. Click \"Start visualization\"\n" + \
            " 3. Draw the map you want:\n    - First two clicks are start and end respectively\n    - Following clicks are walls\n" + \
            " 4. Right click to remove colored nodes\n" + \
            " 5. Press space to start visualization\n" + \
            " 6. When simulation ends, do NOT close the simulation tab\n" + \
            " 7. Go back to step 1 to continue using\n")

# algorithm buttons
algorithm = tk.IntVar()

dijkstra_button = tk.Checkbutton(screen, text="Dijkstra", font="30", variable=algorithm, onvalue=0)
dijkstra_button.place(anchor=tk.CENTER, relx=0.3, rely=0.5)

a_star_button = tk.Checkbutton(screen, text="A*", font="30", variable=algorithm, onvalue=1)
a_star_button.place(anchor=tk.CENTER, relx=0.7, rely=0.5)

# speed input
speed = tk.IntVar()

slow_button = tk.Checkbutton(screen, text="Slow", font="30", variable=speed, onvalue=10)
slow_button.place(anchor=tk.CENTER, relx=0.2, rely=0.7)

medium_button = tk.Checkbutton(screen, text="Medium", font="30", variable=speed, onvalue=60)
medium_button.place(anchor=tk.CENTER, relx=0.5, rely=0.7)

fast_button = tk.Checkbutton(screen, text="Fast (Default)", font="30", variable=speed, onvalue=256)
fast_button.place(anchor=tk.CENTER, relx=0.8, rely=0.7)

# button to start visualization
start_button = tk.Button(screen, text="Start visualization", command=lambda: run_algorithm())
start_button.place(anchor=tk.CENTER, relx=0.5, rely=0.9)

screen.mainloop()