# ai-minimax-agent
Python agent that plays the board game [Reversi/Othello](https://en.wikipedia.org/wiki/Reversi) using a [minimax strategy](https://en.wikipedia.org/wiki/Minimax) with [alpha-beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning).

Uses Python 2.7.

## Files
File|Description
:-:|---
*board.py*|Othello board class (not written by me). 
*ksx2101.py*|My game-playing minimax agent.
*q2_ksx2101.txt*|Experiments analyzing number of nodes generated/duplicated, average branching factor of the search tree, and algorithm runtime for different tree depths.
*readme_ksx2101.txt*|Original README file (reproduced in below sections).


## Overview
* Sources used: http://dhconnelly.com/paip-python/docs/paip/othello.html
* I wrote my code for minimax/alpha-beta based off the lecture slides.
* My agent will never run out of time. If the total time allotted is 30 seconds, it will use about 20-25 seconds. If the total time allotted is 60+ seconds, it will use about 40 seconds. This is explained below.

## My Heuristic
* My evaluation function is based off a 2D array that assigns a weighted value to each square on the 8x8 board (got weighted values from source).
* The function calculates the value of the board by summing up the weighted values of the squares where you have pieces, and then subtracting the sum of the weighted values of the squares where your opponent has pieces.
* The corner squares are worth the most (120) because they are the most important squares in the game. They cannot be flipped once placed. If you own two adjacent corners, you probably will own the connecting side.
* The squares immediately adjacent (including diagonally) to the corner squares are worth a lot of negative points (-20, -40) because they help your opponent take the corner squares.
* The squares two spaces away from the corners are worth a good amount of points (20, 15) because they help you obtain the corner squares.
* For the rest of the board, generally, squares close to the center are worth a few points and those a little farther away are worth a few negative points. This is based off basic Othello strategy.


## Effectiveness vs. Time Remaining
* The get_move() function uses the minimax algorithm if alpha_beta is false and uses minimax with alpha-beta pruning if alpha_beta is true.
* If time_remaining > 12 seconds, then get_move() will use minimax or alpha-beta with a ply of 4. This is because a deep ply will likely lead towards the best possible outcome.
* If time_remaining > 1 second, then get_move() will use minimax/alpha-beta with a ply of 3. This might lead to a less optimal outcome, but is much faster than a ply of 4.
* If you have less than 1 second remaining, get_move() will just pick random moves. This level will almost never be reached, but this ensures that you will never run out of time because random moves are essentially instantaneous.
