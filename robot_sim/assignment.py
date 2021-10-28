from __future__ import print_function
import time
from sr.robot import *
import math

"""
Exercise 1 python script

Put the main code after the definition of the functions. The code should drive the robot around the environment
Steps to be performed:
1- give a linear velocity (speed 50, time 2)
2- give an angular velocity (speed 20, time 2)
3- move the robot in circle -> hint: you should create a new function setting the velocities so as to have a linear velocity + an angular velocity (speed 30, time 5)

When done, run with:
	$ python run.py exercise1.py
"""
a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""
R = Robot()
""" instance of the class Robot"""


def drive(speed, seconds):
    """
    Function for setting a linear velocity

    Args: speed (int): the speed of the wheels
          seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def turn(speed, seconds):
    """
    Function for setting an angular velocity

    Args: speed (int): the speed of the wheels
          seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def turn_angle(speed, angle):
    if angle > 0:
        turn(speed, angle/54.*20./speed)
    else:
        turn(-speed, -angle/54.*20./speed)


def detect_marker_angle(type, angle, tolerance):
    if type == "silver":
        marker_type = MARKER_TOKEN_SILVER
    elif type == "gold":
        marker_type = MARKER_TOKEN_GOLD
    else:
        return -1, -1
    dist = 2000
    for token in R.see():
        if token.dist < dist and token.rot_y > angle-tolerance and token.rot_y < angle+tolerance and token.info.marker_type == marker_type:
            dist = token.dist
        rot_y = token.rot_y
    if dist == 2000:
        return -1, -1
    else:
        return dist, rot_y

def detect_closest_marker_angle(type, angle, tolerance):
    if type == "silver":
        marker_type = MARKER_TOKEN_SILVER
    elif type == "gold":
        marker_type = MARKER_TOKEN_GOLD
    dist=2
    for token in R.see():
        if token.dist < dist and token.info.marker_type == marker_type and token.rot_y > angle-tolerance and token.rot_y < angle+tolerance:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==2:
        return -1, -1
    else:
        return dist, rot_y


def straight_drive(lin_speed,rot_speed, last_turn):
    tolerance = 0.08
    dist_right, roty_right = detect_marker_angle("gold",90, 25)
    dist_left, roty_left = detect_marker_angle("gold",-90, 25)
    if dist_right == -1 or dist_left == 1:
        print("dist far")
        drive(lin_speed,1)
        return
    if dist_right > dist_left + tolerance :
        if last_turn != "right":
            print("dist right over dist left")
            turn_angle(rot_speed,5)
            drive(lin_speed,0.8)
            last_turn = "right"
        else : 
             drive(lin_speed,0.5)
    elif dist_right < dist_left - tolerance:
        if last_turn != "left":
            print("dist left over dist right")
            turn_angle(rot_speed,-5)
            drive(lin_speed,0.8)
            last_turn = "left"
        else : 
             drive(lin_speed,0.5)
    else:
        print("everything ok")
        drive(lin_speed,0.8)
    return last_turn


def detect_wall_and_turn(tolerance_front, rot_speed, lin_speed, last_turn):
    dist_front, rotfront = detect_marker_angle("gold",0, 15)
    if dist_front < tolerance_front and dist_front!= -1:
        dist_right, roty_right = detect_marker_angle("gold",90, 15)
        dist_left, roty_left = detect_marker_angle("gold",-90, 15)
        if dist_right >= dist_left:
            turn_angle(rot_speed,80)
            drive(lin_speed,5)
            last_turn = "front"
        else:
            turn_angle(rot_speed,-80)
            drive(lin_speed,5)
            last_turn = "front"
    return last_turn

def move_towards(type, angle, tolerance):
    retries = 0
    while 1:
        retries += 1
        if retries > 40 :
            return False
        # dist, rot_y = m.dist, m.rot_y  # we look for markers
        dist, rot_y = detect_closest_marker_angle(type, angle, tolerance)
        print("token is at " + str(dist) + " " + str(rot_y))
        if dist==-1:
            print("I don't see any token!!")
            exit()# if no markers are detected, the program ends
        elif dist <d_th: 
            print("Found it!")
            R.grab() # if we are close to the token, we grab it.
            print("Gotcha!") 
            break
        elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
            print("Ah, here we are!.")
            drive(20, 0.5)
        elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
            print("Left a bit...")
            turn(-2, 0.5)
        elif rot_y > a_th:
            print("Right a bit...")
            turn(+2, 0.5)
    return True

def put_marker():
        turn_angle(20,180)
        R.release()
        turn_angle(20,-180)
        drive(20,1)

def get_marker(type, angle, tolerance, last_turn):
    dist, rot_y = detect_closest_marker_angle(type,angle, tolerance)
    if (dist, rot_y) != (-1, -1):
        print("found" + type + " at " + str(dist) + " " + str(rot_y))
        if (move_towards(type, angle, tolerance)):
            put_marker()
            last_turn = "front"
    return last_turn


def main():
    last_turn = "front"
    turn_wait = 30
    drive(20,5)
    while(1):
        dist_front, roty_front = detect_marker_angle("gold",0, 10)
        if dist_front > 2. or dist_front == -1:
            last_turn =straight_drive(20,20, last_turn)
        else:
            drive(20,0.2)
        # for token in R.see():
        #     print(token.dist, token.rot_y)
        # dist_right, roty_right = detect_marker_angle("gold",90, 15)
        # dist_left, roty_left = detect_marker_angle("gold",-90, 15)
        # print(" dist right" + str(dist_right))
        # print("dist left" + str(dist_left))
            # if turn_wait >= 30:
            detect_wall_and_turn(1.2, 20, 20, last_turn)
            #     turn_wait = 0
            # turn_wait+= 1
        last_turn = get_marker("silver", 0, 23, last_turn)


main()

# here goes the code
