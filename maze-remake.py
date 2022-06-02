#!/usr/bin/env python3

import string
#import keyboard
import curses
#import libxmplite
from time import *
import threading

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

def findInMaze(maze, char):
    for ind,i in enumerate(maze):
        for dex,j in enumerate(i):
            if j == char:
                return [ind, dex]
    return [-1, -1]

# Returns an array: [Time limit, Name, Maze data]
def loadMazeFile(filename):
    input = [0, 1, 2] # init with 3 values
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

    return mazeInfo

def goSmiley(direction, mazeChars, smileyCoord):
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
        return smileyCoord

    if(ch[0] + ch[1] == 0):
        return smileyCoord
    new = [smileyCoord[0] + ch[0], smileyCoord[1] + ch[1]]
    if (mazeChars[new[0]][new[1]] == "█"): # This is a mess.
        return smileyCoord

    #cuPrint("smileyCoord was: {}".format(smileyCoord))
    mazeChars[smileyCoord[0]][smileyCoord[1]] = " "
    mazeChars[new[0]][new[1]] = "U"

    # Print the maze again, and reinitialize the coordinates of the character.
    smileyCoord = findInMaze(mazeChars, "U")
    if smileyCoord == [-1, -1]:
        raise Exception("U went out of bounds")
    return [smileyCoord, mazeChars]

timer = 0
keepGoing = True
def countdown():
    global timer

    global keepGoing
    keepGoing = True

    while timer != 0 and keepGoing:
        sleep(1)
        timer -= 1
    return timer

def game(input):
    mazeChars = input[2]
    smileyCoord = findInMaze(mazeChars, "U")

    goalCoord = findInMaze(mazeChars, "░")
    
    global keepGoing
    keepGoing = True

    global timer
    timer = input[0]
    timeThread = threading.Thread(target=countdown)
    timeThread.start()

    global stdscr
    while True:
        chara = stdscr.getch()
        if smileyCoord[0] == goalCoord[0] and smileyCoord[1] == goalCoord[1]:
            keepGoing = False
            return timer
        if timer <= 0:
            return 