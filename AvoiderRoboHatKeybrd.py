# BETA Avoider code with Keyboard control for Initio 4WD Robot with RoboHat Board
# Uses Left & Right obstacle sensors to avoid objects 
# 
# Speed can be controlled using "," & "." keys
# Direction can be controlled with Cursor keys - the robot *should* avoid objects if you try to crash it - maybe... You've been warned.
# Marc Voller (VollTec) Aug 2018


import robohat, time

#======================================================================
# Reading single character by forcing stdin to raw mode
import sys
import tty
import termios

def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ch == '0x03':
        raise KeyboardInterrupt
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)  # 16=Up, 17=Down, 18=Right, 19=Left arrows

# End of single character reading
#======================================================================

speed = 30

print "Avoider Code Test with Keyboard Control - Uses left & right ir obstacle sensors to avoid objects"
print "Use , or < to slow down"
print "Use . or > to speed up"
print "Up Arrow - Forward"
print "Down Arrow - Backward"
print "Left Arrow - Rotate Left"
print "Right Arrow - Rotate Right"
print "Press Ctrl-C to end"
print

robohat.init()

# main loop
try:
    while True:
        keyp = readkey()
        if robohat.irLeft():
			robohat.reverse(speed)
			time.sleep(1)
			robohat.spinRight(speed)
			time.sleep(0.5)
			robohat.forward(speed)
			time.sleep(1)
			print 'I detected something on the left, course adjusted'
			print 'My current speed is', speed
        elif robohat.irRight():
			robohat.reverse(speed)
			time.sleep(1)
			robohat.spinLeft(speed)
			time.sleep(0.5)
			robohat.forward(speed)
			time.sleep(1)
			print 'I detected something on the right, course adjusted'
			print 'My current speed is', speed
			if keyp == 'w' or ord(keyp) == 16:
            robohat.forward(speed)
            print 'Forward', speed
        elif keyp == 'z' or ord(keyp) == 17:
            robohat.reverse(speed)
            print 'Reverse', speed
        elif keyp == 's' or ord(keyp) == 18:
            robohat.spinRight(speed)
            print 'Spin Right', speed
        elif keyp == 'a' or ord(keyp) == 19:
            robohat.spinLeft(speed)
            print 'Spin Left', speed
        elif keyp == '.' or keyp == '>':
            speed = min(100, speed+5)
            print 'Speed+', speed
        elif keyp == ',' or keyp == '<':
            speed = max (0, speed-5)
            print 'Speed-', speed
        elif keyp == ' ':
            robohat.stop()
            print 'Stop'
        elif ord(keyp) == 3:
            break

except KeyboardInterrupt:
    print

finally:
    robohat.cleanup()
    
