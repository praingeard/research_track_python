from __future__ import print_function
import time
from sr.robot import *
import math

"""
run with:
	$ python2 run.py assignment_generalized.py
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
    """
    Function for setting an angular velocity via an angle
    Works well for speeds between 15 and 25

    Args: speed (int): the speed of the wheels
          angle (int): the angle of rotation in degrees (between -180 and 180)
    """
    if angle > 0:
        turn(speed, angle/54.*20./speed)
    else:
        turn(-speed, -angle/54.*20./speed)


def detect_marker_angle(type, angle, tolerance, limit):
    """
    Function for detecting any markers of a certain type at a certain angle with a certain maximum distance

    Args: type (str): the type of token to be detected (either "silver" or "gold")
          angle (int): the angle of the desired detection in degrees (between -180 and 180)
          tolerance(int): bounds of the detection from the angle (between 0 and 180)
          limit(float): maximum distance to be considered for detection
    """
    #getting marker types
    if type == "silver":
        marker_type = MARKER_TOKEN_SILVER
    elif type == "gold":
        marker_type = MARKER_TOKEN_GOLD
    else:
        return -1, -1

    #getting closest marker in respect of desired angle and tolerance
    dist = limit
    for token in R.see():
        if token.dist < dist and token.rot_y > angle-tolerance and token.rot_y < angle+tolerance and token.info.marker_type == marker_type:
            dist = token.dist
            rot_y = token.rot_y
    if dist == limit:
        return -1, -1
    else:
        return dist, rot_y

def straight_drive(lin_speed, rot_speed, last_turn):
    """
    Function for driving in the center of a corridor

    Args: lin_speed (int): desired linear speed of robot
          rot_speed (int): desired rotation speed of robot
          last_turn(str): last direction the robot has turned (either "front", "right" or "left"), avoids wall collision

    Returns the new last direction the robot has turned
    """

    #tolerance of distance between walls
    tolerance = side_wall_dist_tol

    #detecting golden markers right and left
    dist_right, roty_right = detect_marker_angle("gold", 90, side_angle_tol, max_detect_side_dist)
    dist_left, roty_left = detect_marker_angle("gold", -90, side_angle_tol, max_detect_side_dist)

    #if we are not in a corridor we drive straight
    if dist_right == -1 or dist_left == 1:
        print("dist far")
        drive(lin_speed, 1)
        return

    #if a wall is closer to the other, we turn a bit and drive to the furthest wall
    if dist_right > dist_left + tolerance:
        #we can't do to right turns or two left turns successively to avoid wall collision
        if last_turn != "right":
            print("dist right over dist left")
            turn_angle(rot_speed, straight_drive_angle_turn)
            drive(lin_speed, straight_drive_time_step)
            last_turn = "right"
        else:
            drive(lin_speed, straight_drive_time_step/2) #drive straight if the turn is not possible
    elif dist_right < dist_left - tolerance:
        #we can't do to right turns or two left turns successively to avoid wall collision
        if last_turn != "left":
            print("dist left over dist right")
            turn_angle(rot_speed, -straight_drive_angle_turn)
            drive(lin_speed, straight_drive_time_step)
            last_turn = "left"
        else:
            drive(lin_speed, straight_drive_time_step/2) #drive straight if the turn is not possible
    else:
        print("everything ok")
        drive(lin_speed, straight_drive_time_step) #drive straight if in the middle of corridor
    return last_turn


def detect_wall_and_turn(tolerance_front, rot_speed, lin_speed, last_turn):
    """
    Function for detecting a front wall and turning in the right direction

    Args: tolerance_front (float): distance from the front wall at which the robot will turn 
          lin_speed (int): desired linear speed of robot
          rot_speed (int): desired rotation speed of robot
          last_turn(str): last direction the robot has turned (either "front", "right" or "left"), avoids wall collision

    Returns the new last direction the robot has turned (will reset it to "front" after the turn)
    """
    dist_front, rotfront = detect_marker_angle("gold", 0, front_angle_tol, 100) #detecting closest wall in front of robot
    if dist_front < tolerance_front and dist_front != -1: #if wall close enough

        #detect distance to left and right walls
        dist_right, roty_right = detect_marker_angle("gold", 90, 15, 100)
        dist_left, roty_left = detect_marker_angle("gold", -90, 15, 100)

        #turn the opposite way of the closest side wall
        if dist_right >= dist_left:
            if abs(rotfront) <= front_wall_detect_angle:
                turn_angle(rot_speed, 80) #turn in the corner
                drive(lin_speed, drive_after_turn_time)
                last_turn = "front" #reset last turn variable
            else :
                drive(-lin_speed, 0.5)
                turn_angle(rot_speed, failsafe_angle_turn) #turn slightly to avoid collision
                last_turn = "right"
            
        else:
            if abs(rotfront) <= front_wall_detect_angle:
                turn_angle(rot_speed, -80) #turn in the corner
                drive(lin_speed, drive_after_turn_time)
                last_turn = "front" #reset last turn variable
            else :
                drive(-lin_speed, 0.5)
                turn_angle(rot_speed, -failsafe_angle_turn) #turn slightly to avoid collision
                last_turn = "left"

    return last_turn


def move_towards(type, angle, tolerance, limit):
    """
    Function for moving towards a targeted token

    Args: type (str): the type of token to be detected (either "silver" or "gold")
          angle (int): the angle of the desired detection in degrees (between -180 and 180)
          tolerance(int): bounds of the detection from the angle (between 0 and 180)
          limit(float): maximum distance to be considered for detection

    Returns True if the token was caught within 40 tries, else returns False
    """
    retries = 0
    while 1:
        retries += 1
        if retries > 40:
            return False
        # dist, rot_y = m.dist, m.rot_y  # we look for markers
        dist, rot_y = detect_marker_angle(type, angle, tolerance, limit)
        print("token is at " + str(dist) + " " + str(rot_y))
        if dist == -1:
            print("I don't see any token!!")
            exit()  # if no markers are detected, the program ends
        elif dist < d_th:
            print("Found it!")
            R.grab()  # if we are close to the token, we grab it.
            print("Gotcha!")
            break
        elif -a_th <= rot_y <= a_th:  # if the robot is well aligned with the token, we go forward
            print("Ah, here we are!.")
            drive(lin_speed, 0.5)
        elif rot_y < -a_th:  # if the robot is not well aligned with the token, we move it on the left or on the right
            print("Left a bit...")
            turn(-2, 0.5)
        elif rot_y > a_th:
            print("Right a bit...")
            turn(+2, 0.5)
    return True


def put_marker():
    """
    Function for moving a grabed marker and putting it behind the robot
          
    """
    turn_angle(rot_speed, 175)
    R.release()
    turn_angle(rot_speed, -175)
    drive(lin_speed, after_grab_time)


def get_marker(type, angle, tolerance, last_turn, limit):
    """
    Function for catching the closest marker of a certain type and put it behind the robot

    Args: type (str): the type of token to be detected (either "silver" or "gold")
          angle (int): the angle of the desired detection in degrees (between -180 and 180)
          tolerance(int): bounds of the detection from the angle (between 0 and 180)
          last_turn(str): last direction the robot has turned (either "front", "right" or "left"), avoids wall collision
          limit(float): maximum distance to be considered for detection

    Returns the new last direction the robot has turned (will reset it to "front" after the action)
    """
    dist, rot_y = detect_marker_angle(type, angle, tolerance, limit) #detect closest marker of desired type
    if (dist, rot_y) != (-1, -1):
        print("found" + type + " at " + str(dist) + " " + str(rot_y))
        if (move_towards(type, angle, tolerance, limit)): #move towards marker
            put_marker() #put marker behind robot
            last_turn = "front" #reset last turn variable
    return last_turn


def main():
    limit = silver_marker_detect_dist #limit distance for silver token detection
    last_turn = "front" #last turn taken by the robot
    while(1):
        dist_front, roty_front = detect_marker_angle("gold", 0, 10, 100) #detect front wall
        if dist_front > front_wall_turn_dist*1.5 or dist_front == -1: #if far from front wall
            last_turn = straight_drive(lin_speed, rot_speed, last_turn) #drive in the center of corrifdor
        else:
            drive(lin_speed, 0.2)
            detect_wall_and_turn(front_wall_turn_dist, lin_speed, rot_speed, last_turn) #turn if wall is close enough
        last_turn = get_marker("silver", 0, silver_marker_tolerance, last_turn, limit) #get a detected silver marker if one is close to the robot


#parameters

#speeds of robot
lin_speed = 20
rot_speed = 20

#max detection distance of silver markers and angle tolerance on detection
silver_marker_detect_dist = 2
silver_marker_tolerance = 24
after_grab_time = 1 #time driving straight after getting a silver marker

#front detection params
front_wall_turn_dist = 1.2 #max distance to the front wall from which the robot is in a corner
front_angle_tol = 30 #tolerance for front detections 
drive_after_turn_time = 4 #time of driving straight after turning at a corner

#failsafe params
front_wall_detect_angle = 15 #angle from which a wall is considered a side wall to avoid
failsafe_angle_turn = 10 #angle to turn robot in case it's too close to a side wall

#side detections params
side_wall_dist_tol = 0.08 #minimal distance difference betweens walls for the robot to turn
side_angle_tol = 25 #angle tolerance for side detection
max_detect_side_dist = 100 #max distance detected for side detection

#straight drive params
straight_drive_time_step = 0.5 #straight drive time step
straight_drive_angle_turn = 5 #angle to turn in degrees to drive straight

main()
