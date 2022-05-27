#!/usr/bin/env python3

import string
#import keyboard
import curses
import libxmplite
#https://stackoverflow.com/questions/3523174/raw-input-without-pressing-enter

# Problem: My kids need a distraction, but all I have is a Linux terminal and a Python interpreter!

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
stdscr.clear()
stdscr.refresh()
curses.start_color()

line = 0

def clear():
    stdscr.clear()
    line = 0

def printMaze(maze):
    clear()
    returner = [-1, -1]
    for dex,i in enumerate(maze):
        line = ""
        for ind,j in enumerate(i):
            line += j
            if j == "☺":
                returner = [dex, ind]
        print(line)
    return returner

def dontPrintMaze(maze):
    clear()
    returner = [-1, -1]
    for dex,i in enumerate(maze):
        line = ""
        for ind,j in enumerate(i):
            if j == "☺" or j == "░":
                if j == "☺": returner = [dex, ind]
                line += j
            else:
                line += " "
        print(line)
    return returner

# def

# The maze itself is a constant.
mazeStrings = [
    "█████████████",
    "█☺█         █",
    "█     █     █",
    "█    ███    █",
    "███     █   █",
    "█        █  █",
    "██  █      ██",
    "█  █ █    █  ",
    "█     █  █ ██",
    "█  █       ░█",
    "█████████████"] # It's a lot easier to write it this way.

# ...but here's what I'm REALLY gonna use!
mazeChars = []
for i in mazeStrings:
    mCpart = []
    for j in i:
        mCpart.append(j)
    mazeChars.append(mCpart)

smileyCoord = printMaze(mazeChars)

goalCoord = 0
for dex,i in enumerate(mazeChars):
    if(goalCoord != 0): break
    for ind,j in enumerate(i):
        if(j == "░"):
            goalCoord = [dex, ind]
            break

def game(mazeChars):
    while True:
        char = stdscr.getch()
        if goSmiley(char) and smileyCoord[0] == goalCoord[0] and smileyCoord[1] == goalCoord[1]:
            return

def goSmiley(direction):
    # Interpret the input.
    ch = [0, 0]
    try:
        if direction == 'd':
            ch = [0, 1]
        if direction == 'a':
            ch = [0, -1]
        if direction == 's':
            ch = [1, 0]
        if direction == 'w':
            ch = [-1, 0]
    except(IndexError):
        #print("☺  { Please type a direction for me to go. )")
        return False

    #print("ch is: {}".format(ch))

    if(ch[0] + ch[1] == 0):
        #print("☺  { Please type a direction for me to go. )")
        return False
    new = [smileyCoord[0] + ch[0], smileyCoord[1] + ch[1]]
    if (mazeChars[new[0]][new[1]] == "█"): # This is a mess.
        #print("☺  { Please type a direction for me to go. )")
        return False

    #print("smileyCoord was: {}".format(smileyCoord))
    mazeChars[smileyCoord[0]][smileyCoord[1]] = " "
    mazeChars[new[0]][new[1]] = "☺"

    # Print the maze again, and reinitialize the coordinates of the character.
    smileyCoord = dontPrintMaze(mazeChars)
    if smileyCoord == [-1, -1]:
        raise Exception("Smiley's gone?")
    #print("smileyCoord is: {}".format(smileyCoord))
    #print("smileyCoord is: {}".format(goalCoord))
    return True

game(mazeChars)

curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
print("Congratulations! You won!")