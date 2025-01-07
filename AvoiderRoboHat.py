# Beta Avoider code for Initio 4WD Robot with RoboHat Board
# Uses Left & Right obstacle sensors to avoid objects 
# 
# Speed can be controlled using "," & "." keys
#
# Marc Voller (VollTec) Jan 2025


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

print "Basic Avoider Code Test - Uses left & right ir obstacle sensors to avoid objects"
print "Use , or < to slow down"
print "Use . or > to speed up"
print ""
print "Press Ctrl-C to end"
print

robohat.init()
print 'Robot initialised'

# main loop
try:
    while True:
        keyp = readkey()
	print 'Key pressed:', keyp
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
    
