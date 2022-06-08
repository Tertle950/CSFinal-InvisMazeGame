#!/usr/bin/env python3

import string
#import keyboard
import curses
from curses import wrapper
#import libxmplite
from time import *
from os.path import exists
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

def updateGameScreen(mazeChars, name, isVisible, timer = 0, score = 0, lives = 3):
    clear()

    # Print lives & score
    # For ease of copying, here are the hearts: ♥ ♡
    hearts = ""
    for i in range(maxLives):
        if i+1 > lives:
            hearts += "♡"
        else: hearts += "♥"
    cuPrint(f"{hearts}  S:{score}  ⧗{round(timer)}")

    # print maze name
    cuPrint(f" -= {name} =-")

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
    
    stdscr.refresh()

def game(input, score = 0, lives = 1):
    # Initialize variables
    mazeName = input[1]
    mazeChars = input[2]
    smileyCoord = findInMaze(mazeChars, "U")
    goalCoord = findInMaze(mazeChars, "░")
    isVisible = True

    timeStart = time()
    timeEnd = time() + input[0]

    result = [0, 0]

    updateGameScreen(mazeChars, mazeName, isVisible, timeEnd - time(), score, lives)
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
        
        # Check for winstate and failstate.
        # Also, update the screen.
        sleep(0.03)
        if smileyCoord[0] == goalCoord[0] and smileyCoord[1] == goalCoord[1]:
            yes = int(timeEnd - time())
            updateGameScreen(mazeChars, mazeName, True, yes, score, lives)
            return yes
        elif time() >= timeEnd:
            updateGameScreen(mazeChars, mazeName, True, 0, score, lives)
            return 0
        else:
            updateGameScreen(mazeChars, mazeName, isVisible, timeEnd - time(), score, lives)

def main(stdscr):
    lives = 3
    score = 0
    exLife = 2
    level = 1
    while(lives != 0):
        if(not exists(f"mazes/{level}.txt")):
            level = 1
        gameResult = game(loadMazeFile(f"mazes/{level}.txt"), score, lives)
        if(gameResult == 0):
            lives -= 1
        else:
            score += gameResult
            if (score / 100) > exLife:
                exLife += 2
                lives += 1
        level += 1
        sleep(2)
    clear()
    cuPrint(f"U got a score of {score}. Game over!")
    sleep(5)

wrapper(main)
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
# trailing newline baby
