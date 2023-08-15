#!/usr/bin/python3
import sys 
import socket
import math
from tkinter import *

# Process the command line arguments
if (len(sys.argv) == 2) :
    trick_varserver_port = int(sys.argv[1])
else :
    print("Usage: python<version_number> RocketDisplay.py <port_number>")
    sys.exit()

# ----------------------------- Global Variables -----------------------------

HEIGHT, WIDTH = 500, 800                    # Height and width of the canvas
X = WIDTH/2                                 # Center x cord of the canvas
Y = HEIGHT/2                                # Center y cord of the canvas
SCALE = 1                                   # Scale from sim data to display
sim_planet_radius = 6366707.0195            # Size of the planet from sim TODO: remove and grab at startup
planet_radius = sim_planet_radius * SCALE   # Radius of the planet after scaling
rocket_radius = 10                          # Radius of the circle used to represent the rocket

# Sim modes
MODE_FREEZE = 1 
MODE_RUN = 5

# Button condition variables
first_start = True
change_sim_mode = False
disconnect_from_sim = False

# ----------------------------- Helper Functions -----------------------------

def isCircleInFrame(x, y) -> bool:
    '''
    Determines if a circle is visible in the current frame. Used to know if the planet has gone out of frame and the
    scale needs to be adjusted.
    '''
    cx, cy = (-x*SCALE)+X, (y*SCALE)+(HEIGHT - Y)

    # Calculate the points on the circle that will be checked
    num_angles = 16
    check_angle_rad = (360 / num_angles) * (math.pi / 180)
    curr_angle_rad = 0

    # Loop over the different points on the circle and see if any point is visible in the current frame
    for angle in range(num_angles):
        check_cx = cx + planet_radius * math.cos(curr_angle_rad)
        check_cy = cy + planet_radius * math.sin(curr_angle_rad)

        if ((0 < check_cx < WIDTH) and (0 < check_cy < HEIGHT)):
            return True

        curr_angle_rad += check_angle_rad
    
    return False

def rescale(x, y):
    '''
    Change the scale factor if needed to keep the planet visible.
    '''
    global SCALE, planet_radius

    scale_change = 2
    max_iters = 10
    curr_iter = 1

    # While the planet is not visible, keep updating the scale factor
    while (not isCircleInFrame(x, y)) and (curr_iter < max_iters):
        SCALE /= scale_change
        planet_radius = sim_planet_radius * SCALE
        curr_iter += 1

def changeSimMode():
    global change_sim_mode

    change_sim_mode = True

def disconnectFromSim():
    global disconnect_from_sim

    disconnect_from_sim = True

# ----------------------------- Canvas Setup ---------------------------------

# Create the canvas
tk = Tk()
canvas = Canvas(tk, width=WIDTH, height=HEIGHT)
tk.title("Rocket Display")
canvas.pack()

# Add buttons to interact with the sim
button_frame = Frame()
button_frame.pack(side=BOTTOM)
start_button = Button(button_frame, text="start", command=changeSimMode)
start_button.pack(side=LEFT)
freeze_button = Button(button_frame, text="freeze", command=changeSimMode)
freeze_button.pack(side=LEFT)
freeze_button.config(state=DISABLED)
disconnect_button = Button(button_frame, text="disconnect", command=disconnectFromSim)
disconnect_button.pack(side=LEFT)

# TODO: Maybe use the scale for changing initial conditions
# speed_scale = Scale(button_frame, from_=5, to=50, label="Initial Speed", orient=HORIZONTAL)
# speed_scale.pack(side=LEFT)
# speed_scale.set(50)

# Create the planet and rocket circles
planet = canvas.create_oval(X-planet_radius,Y-planet_radius,X+planet_radius,Y+planet_radius, fill="green")
rocket = canvas.create_oval(X-rocket_radius,Y-rocket_radius,X+rocket_radius,Y+rocket_radius, fill="red")

# Create a text field on the canvas to display the sim mode
curr_mode_text = canvas.create_text(WIDTH/2, 20, text="--unknown-mode--")

# Create a text field on the canvas to display the altitude of the rocket
altitude_text = canvas.create_text(WIDTH/2, 40, text="Altitude: 0 m")

# ----------------------------- Variable Server Setup ------------------------

# Connect to the variable server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", trick_varserver_port))
insock = client_socket.makefile("r")

# Request the state of the rocket
client_socket.send( b"trick.var_set_client_tag(\"rocketclient\") \n")
client_socket.send( b"trick.var_pause()\n" )
client_socket.send( b"trick.var_ascii()\n" )
client_socket.send( b"trick.var_add(\"dyn.rocket.pos[0]\") \n" +
                    b"trick.var_add(\"dyn.rocket.pos[1]\") \n" +
                    b"trick.var_add(\"trick_sys.sched.mode\") \n"
                  )
client_socket.send( b"trick.var_unpause()\n" )

# ----------------------------- Infinite Loop --------------------------------

# Repeatedly read and process the responses from the variable server
while(True):
    line = insock.readline()
    if line == '':
        break

    fields = line.split("\t")

    # Update the position of the rocket
    x,y = float(fields[1]), float(fields[2])
    cx,cy = (-x*SCALE)+X, (y*SCALE)+(HEIGHT - Y)
    
    # Change the scale factor if needed
    rescale(x, y)

    # Move the rocket (move the planet so that the rocket is always at the center)
    canvas.coords(planet,cx-planet_radius,cy-planet_radius,cx+planet_radius,cy+planet_radius)

    # Update the sim variable displays
    curr_alt = math.hypot(x, y) - sim_planet_radius
    canvas.itemconfigure(altitude_text, fill="black", text="Altitude: {:.2f} m".format(curr_alt))

    # Display the current mode of the sim
    curr_mode = int(fields[3])
    if curr_mode == MODE_FREEZE:
        canvas.itemconfigure(curr_mode_text, fill="blue", text="FREEZE")
    elif curr_mode == MODE_RUN:
        canvas.itemconfigure(curr_mode_text, fill="red", text="RUNNING")
    else:
        canvas.itemconfigure(curr_mode_text, text="--unknown-mode--")
    
    # Button management
    if curr_mode == MODE_FREEZE and change_sim_mode:
        if first_start:
            first_start = False
            # TODO: Set the start state of the sim
        # Command the sim to RUN mode and disable button
        client_socket.send(b"trick.exec_run()\n")
        start_button.config(state=DISABLED)
        freeze_button.config(state=ACTIVE)
        change_sim_mode = False
    elif curr_mode == MODE_RUN:
        if change_sim_mode:
            # Command the sim to FREEZE mode and disable button
            client_socket.send(b"trick.exec_freeze()\n")
            start_button.config(state=ACTIVE)
            freeze_button.config(state=DISABLED)
            change_sim_mode = False
        elif disconnect_from_sim:
            client_socket.send(b"trick.exit()\n")
            break

    # Update the canvas
    tk.update()

# Keep the canvas up after sim stops
# tk.mainloop()