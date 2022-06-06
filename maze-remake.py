#!/usr/bin/env python3

import string
#import keyboard
import curses
from curses import wrapper
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

stdscr.timeout(1)

cuLine = 0
maxLives = 5

def clear():
    stdscr.clear()
    global cuLine
    cuLine = 0

def cuPrint(x):
    global cuLine
    stdscr.addstr(cuLine+1, 2, x)
    cuLine += 1
    return

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

    return input

def goSmiley(direction, mazeChars, smileyCoord):
    # Interpret the input.
    ch = [0, 0]
    try:
        if direction == 100 or direction == 261: #d
            ch = [0, 1]
        elif direction == 97 or direction == 260: #a
            ch = [0, -1]
        elif direction == 115 or direction == 258: #s
            ch = [1, 0]
        elif direction == 119 or direction == 259: #w
            ch = [-1, 0]
    except(IndexError):
        return [0]

    if(ch[0] + ch[1] == 0):
        return [0]
    new = [smileyCoord[0] + ch[0], smileyCoord[1] + ch[1]]
    if (mazeChars[new[0]][new[1]] == "█"): # This is a mess.
        return [1]

    #print("smileyCoord was: {}".format(smileyCoord))
    mazeChars[smileyCoord[0]][smileyCoord[1]] = " "
    mazeChars[new[0]][new[1]] = "U"

    # Print the maze again, and reinitialize the coordinates of the character.
    smileyCoord = findInMaze(mazeChars, "U")
    if smileyCoord == [-1, -1]:
        raise Exception("U went out of bounds")
    return [smileyCoord, mazeChars]

def updateGameScreen(mazeChars, isVisible, timer = 0, score = 0, lives = 3):
    clear()

    # Print lives & score
    # For ease of copying, here are the hearts: ♥ ♡
    hearts = ""
    for i in range(maxLives):
        if i > lives:
            hearts += "♡"
        else: hearts += "♥"
    cuPrint(f"{hearts}  SC:{score}  ⧗{round(timer)}")

    # Print maze, or don't. This code's a mess, but it's fine
    dots = False
    for dex,i in enumerate(mazeChars):
        line = ""
        dots = False
        for ind,j in enumerate(i):
            if j == " " and dots:
                line += "."
            elif j == "█":
                dots = True
                if isVisible:
                    line += "█"
                else: line += "."
            elif isVisible or j == "U" or j == "░":
                line += j
            else:
                line += "." if dots else " "

            if j == "U":
                returner = [dex, ind]
        cuPrint(line)

def game(input):
    # Initialize variables
    mazeChars = input[2]
    smileyCoord = findInMaze(mazeChars, "U")
    goalCoord = findInMaze(mazeChars, "░")
    isVisible = True
    
    # These should be changed later on. Maybe also made global.
    score = 42
    lives = 1

    timeStart = time()
    timeEnd = time() + input[0]

    result = [0, 0]

    updateGameScreen(mazeChars, isVisible, timeEnd - time(), score, lives)
    while True:
        # Get player input
        chara = stdscr.getch()

        # Update maze according to input
        result = goSmiley(chara, mazeChars, smileyCoord)

        if(result[0] != 0):
            if(result[0] != 1):
                smileyCoord = result[0]
                mazeChars = result[1]
                isVisible = False
            else:
                timeEnd -= 3
        # There are technically less global variables with this approach,
        # but this code might be absolutely terrible.

        # This should run every loop...
        updateGameScreen(mazeChars, isVisible, timeEnd - time(), score, lives)
        stdscr.refresh()

        # Check for winstate and failstate
        if smileyCoord[0] == goalCoord[0] and smileyCoord[1] == goalCoord[1]:
            updateGameScreen(mazeChars, isVisible, timeEnd - time(), score, lives)
            keepGoing = False
            return timeEnd - time()
        elif time() >= timeEnd:
            return 0
        
        sleep(0.03) # 30fps, let's not overload the computer.

def main(stdscr):
    if game(loadMazeFile("test-maze.txt")) == 0:
        print("U died in the maze.")
    else:
        print("U got to the end!")
    sleep(2)

wrapper(main)
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()