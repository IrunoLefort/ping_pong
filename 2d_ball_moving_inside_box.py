from vpython import *
import serial
import time
import os

room_x = 20
room_y = 5
room_z = 1.2
wall_thick = 0.2
wall_color = vector(1, 1, 1)
wall_opacity = 0.8
front_opacity = 0.2
ball_radius = 0.5
ball_color = vector(0, 0, 1)

my_floor = box(size=vector(room_x, wall_thick, room_z),
            pos=vector(0, -room_y/2, 0),
            color=wall_color, opacity=wall_opacity)
my_ceiling = box(size=vector(room_x, wall_thick, room_z),
               pos=vector(0, room_y/2, 0),
               color=wall_color, opacity=wall_opacity)
left_wall = box(size=vector(wall_thick, room_y, room_z),
               pos=vector(-room_x/2, 0, 0),
               color=wall_color, opacity=wall_opacity)
right_wall = box(size=vector(wall_thick, room_y, room_z),
               pos=vector(room_x/2, 0, 0),
               color=wall_color, opacity=wall_opacity)
back_wall = box(size=vector(room_x, room_y, wall_thick),
               pos=vector(0, 0, -room_z/2),
               color=wall_color, opacity=wall_opacity)
front_wall = box(size=vector(room_x, room_y, wall_thick),
               pos=vector(0, 0, room_z/2),
               color=wall_color, opacity=front_opacity)

my_ball = sphere(color=ball_color, radius=ball_radius)

paddle_x = 4
paddle_y = wall_thick
paddle_z = 0.85*room_z
paddle_x_position = 0
paddle_y_position = -room_y/2+wall_thick/2
paddle_axis = vector(0, 0, 0)
paddle_color = vector(100, 100, 0)
paddle_opacity = 0.8
my_paddle = box(size=vector(paddle_x, paddle_y, paddle_z),
                pos=vector(paddle_x_position, paddle_y_position, 0),
                color=paddle_color, opacity=paddle_opacity)

ball_x_position = 0
ball_y_position = 0
delta_x = 0.1
delta_y = 0.1


arduino_data = serial.Serial('com5', baudrate=9600)

while(True):
    while(arduino_data.inWaiting()==0):
        pass
    data = arduino_data.readline()
    data = str(data, "utf-8")
    data = data.strip("\r\n")
    x = float(data)
    paddle_x_position = (room_x/1023.0)*x - room_x/2
    
    # to avoid that the paddle gets out the box
    if(paddle_x_position >= room_x/2-paddle_x/2):
        paddle_x_position = room_x/2-paddle_x/2
    if(paddle_x_position <= -room_x/2+paddle_x/2):
        paddle_x_position = -room_x/2+paddle_x/2
         
    ball_x_position = ball_x_position + delta_x
    x_test1 =  ball_x_position+ball_radius>room_x/2-wall_thick/2
    x_test2 = ball_x_position-ball_radius<-room_x/2+wall_thick/2

    if x_test1 or x_test2:
        delta_x = delta_x*(-1)
   
    ball_y_position = ball_y_position + delta_y
    y_test1 =  ball_y_position+ball_radius>room_y/2-wall_thick/2
    y_test2 = ball_y_position-ball_radius<-room_y/2+wall_thick/2
    if y_test1:
        delta_y = delta_y*(-1)
    
    test_paddle_x = paddle_x_position-paddle_x/2<ball_x_position and ball_x_position<paddle_x_position+paddle_x/2
    
    if y_test2:
        if test_paddle_x:
            delta_y = delta_y*(-1)
        else:
            lab = label(text="GAME OVER!", color=color.red)
            time.sleep(3)
            os._exit()
    
    my_ball.pos = vector(ball_x_position, ball_y_position, 0)
    my_paddle.pos = vector(paddle_x_position, paddle_y_position, 0)