#!/usr/bin/env python3

import string
#import keyboard
import curses
#import libxmplite
from time import *
import threading
#https://stackoverflow.com/questions/3523174/raw-input-without-pressing-enter

# Problem: My kids need a distraction, but all I have is a Linux terminal and a Python interpreter!
# ...and libxmplite, I guess?

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
stdscr.clear()
stdscr.refresh()
curses.start_color()

cuLine = 0

def clear():
    stdscr.clear()
    global cuLine
    cuLine = 0

    global timer
    stdscr.addstr(1, 1, str(timer)+"   ")

def cuPrint(x):
    global cuLine
    stdscr.addstr(cuLine+2, 1+2, x)
    cuLine += 1
    return

def printMaze(maze):
    clear()
    returner = [-1, -1]
    for dex,i in enumerate(maze):
        line = ""
        dots = False
        for ind,j in enumerate(i):
            if j == " " and dots:
                line += "."
            elif j == "█":
                dots = True
                line += "█"
            else: line += j
            if j == "U":
                returner = [dex, ind]
        cuPrint(line)
    return returner

def dontPrintMaze(maze):
    clear()
    returner = [-1, -1]
    for dex,i in enumerate(maze):
        line = ""
        dots = False
        for ind,j in enumerate(i):
            if j == "U" or j == "░":
                if j == "U": returner = [dex, ind]
                line += j
            elif j == "█":
                dots = True
                line += "."
            elif dots:
                line += "."
            else: line += " "
        cuPrint(line)
    return returner

# Function for opening a maze.
def loadMaze(filename):
    input = [0, 1, 2]
    mazeStrings = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            mazeStrings.append(line)

    info = mazeStrings[0]
    info = info.split('/')
    input[0] = int(info[0])
    input[1] = info[1][:-1] #the [:-1] is to kill the newline at the end

    mazeChars = []
    for i in range(len(mazeStrings) - 1):
        mCpart = []
        for j in mazeStrings[i+1]:
            mCpart.append(j)
        mazeChars.append(mCpart)

    input[2] = mazeChars

    #print(input)
    #sleep(3)

    return input

goalCoord = 0


smileyCoord = 0

# To Do: https://stackoverflow.com/q/34822346
# + https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
timer = 0
keepGoing = True
def countdown():
    global timer
    stdscr.addstr(1, 1, str(timer)+"   ")

    global keepGoing
    keepGoing = True
    while timer != 0 and keepGoing:
        sleep(1)
        timer -= 1
        stdscr.addstr(1, 1, str(timer)+"   ")
    return timer
    


def game(input):
    mazeChars = input[2]
    global smileyCoord
    smileyCoord = printMaze(mazeChars)

    global goalCoord
    goalCoord = 0
    for dex,i in enumerate(mazeChars):
        if(goalCoord != 0): break
        for ind,j in enumerate(i):
            if(j == "░"):
                goalCoord = [dex, ind]
                break
    
    global keepGoing
    keepGoing = True

    global timer
    timer = input[0]
    timeThread = threading.Thread(target=countdown)
    timeThread.start()

    global stdscr
    while True:
        chara = stdscr.getch()
        if goSmiley(chara, mazeChars) and smileyCoord[0] == goalCoord[0] and smileyCoord[1] == goalCoord[1]:
            keepGoing = False
            return timer
        if timer <= 0:
            return 

def goSmiley(direction, mazeChars):
    global smileyCoord
    # Interpret the input.
    ch = [0, 0]
    try:
        if direction == 100 or direction == 261: #d
            ch = [0, 1]
        if direction == 97 or direction == 260: #a
            ch = [0, -1]
        if direction == 115 or direction == 258: #s
            ch = [1, 0]
        if direction == 119 or direction == 259: #w
            ch = [-1, 0]
    except(IndexError):
        #cuPrint("U  { Please type a direction for me to go. )")
        return False

    #cuPrint("ch is: {}".format(ch))

    if(ch[0] + ch[1] == 0):
        #cuPrint("U  { Please type a direction for me to go. )")
        return False
    new = [smileyCoord[0] + ch[0], smileyCoord[1] + ch[1]]
    if (mazeChars[new[0]][new[1]] == "█"): # This is a mess.
        #cuPrint("U  { Please type a direction for me to go. )")
        return False

    #cuPrint("smileyCoord was: {}".format(smileyCoord))
    mazeChars[smileyCoord[0]][smileyCoord[1]] = " "
    mazeChars[new[0]][new[1]] = "U"

    # Print the maze again, and reinitialize the coordinates of the character.
    smileyCoord = dontPrintMaze(mazeChars)
    if smileyCoord == [-1, -1]:
        raise Exception("U went out of bounds")
    #cuPrint("smileyCoord is: {}".format(smileyCoord))
    #cuPrint("smileyCoord is: {}".format(goalCoord))
    return True

game(loadMaze('test-maze.txt'))
game(loadMaze('test-maze-2.txt'))

curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
print("U got to the end!")