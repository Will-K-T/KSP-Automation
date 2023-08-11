#!/usr/bin/python3
import sys 
import socket
import math
from tkinter import *

# 1.0 Process the command line arguments.
if ( len(sys.argv) == 2) :
    trick_varserver_port = int(sys.argv[1])
else :
    print( "Usage: python<version_number> CannonDisplay_Rev1.py <port_number>")
    sys.exit()

# Create the canvas
HEIGHT, WIDTH = 500, 800
X = WIDTH/2
Y = HEIGHT/2
SCALE = 0.000015706706
# planetRadius = 6366707
planetRadius = 100
rocketRadius = 10

tk = Tk()
canvas = Canvas(tk, width=WIDTH, height=HEIGHT)
tk.title("Rocket Display")
canvas.pack()

planet = canvas.create_oval(X-planetRadius,Y-planetRadius,X+planetRadius,Y+planetRadius, fill="green")
rocket = canvas.create_oval(X-rocketRadius,Y-rocketRadius,X+rocketRadius,Y+rocketRadius, fill="red")

# 2.0 Connect to the variable server.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect( ("localhost", trick_varserver_port) )
insock = client_socket.makefile("r")

# 3.0 Request the cannon ball position.
client_socket.send( b"trick.var_pause()\n" )
client_socket.send( b"trick.var_ascii()\n" )
client_socket.send( b"trick.var_add(\"dyn.rocket.pos[0]\") \n" +
                    b"trick.var_add(\"dyn.rocket.pos[1]\") \n"
                  )
client_socket.send( b"trick.var_unpause()\n" )

# 4.0 Repeatedly read and process the responses from the variable server.
while(True):
    line = insock.readline()
    if line == '':
        break

    fields = line.split("\t")

    print(line)

    x,y = float(fields[1]), float(fields[2])
    cx,cy = (x*SCALE+X), (HEIGHT-y*SCALE-Y)
    canvas.coords(rocket,cx-rocketRadius,cy-rocketRadius,cx+rocketRadius,cy+rocketRadius)

    tk.update()

tk.mainloop()