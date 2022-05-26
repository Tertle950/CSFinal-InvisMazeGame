#!/usr/bin/env python3

import string
import libxmplite

# Problem: My kids need a distraction, but all I have is a Linux terminal and a Python interpreter!

# import only system from os
from os import system, name
  
# import sleep to show output for some time period
from time import sleep

def printMaze(maze):
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
    "████████████",
    "█☺ █       █",
    "█    █     █",
    "█   ███    █",
    "███    █   █",
    "█       █  █",
    "██  █     ██",
    "█  █ █   █  ",
    "█     █ █ ██",
    "█  █      ░█",
    "████████████"] # It's a lot easier to write it this way.

# ...but here's what I'm REALLY gonna use!
mazeChars = []
for i in mazeStrings:
    mCpart = []
    for j in i:
        mCpart.append(j)
    mazeChars.append(mCpart)

smileyCoord = printMaze(mazeChars)

goalCoord = None
for idex,i in enumerate(mazeChars):
    if(goalCoord != None): break
    for jdex,j in enumerate(i):
        if(j == "░"):
            goalCoord = []


while True:
    # Ask for input from the player. UDLR accepted.
    print("☺  { WASD to move. )")
    direction = input("> ").lower()

    # Interpret the input.
    ch = [0, 0]
    try:
        if direction[0] == "r":
            ch = [0, 1]
        if direction[0] == "l":
            ch = [0, -1]
        if direction[0] == "d":
            ch = [1, 0]
        if direction[0] == "u":
            ch = [-1, 0]
    except(IndexError):
        print("☺  { Please type a direction for me to go. )")
        continue

    #print("ch is: {}".format(ch))

    if(ch[0] + ch[1] == 0):
        print("☺  { Please type a direction for me to go. )")
        continue
    new = [smileyCoord[0] + ch[0], smileyCoord[1] + ch[1]]
    if (mazeChars[new[0]][new[1]] == "█"): # This is a mess.
        print("☺  { Please type a direction for me to go. )")
        continue

    #print("smileyCoord was: {}".format(smileyCoord))
    mazeChars[smileyCoord[0]][smileyCoord[1]] = " "
    mazeChars[new[0]][new[1]] = "☺"

    # Print the maze again, and reinitialize the coordinates of the character.
    smileyCoord = dontPrintMaze(mazeChars)
    if smileyCoord == [-1, -1]:
        raise Exception("Smiley's gone?")
    #print("smileyCoord is: {}".format(smileyCoord))
    #print("smileyCoord is: {}".format(goalCoord))


    # Check for victory.
    if smileyCoord[0] == goalCoord[0] and smileyCoord[1] == goalCoord[1]:
        break

print("Congratulations! You won!")