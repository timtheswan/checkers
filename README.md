#Checkers AI Using Minimax Lookahead Algorithm

Given `Checkers.py`, which facilitates a series of fair checkers games between `P1.py` and `P2.py`, I designed a player (`P2.py`) which reliably beats standard heursitic AIs by using a heavily optimized recursive lookahead.

This project was initially a project for Intro to Computational Problem Solving (COS 120), though the additional step of a recursive lookahead and all optimizations was a personal project.

##Constraints
- Player turn limited to 1 second, otherwise they lose the round
- Players have no control over the board API, they may only submit a valid move command.
- Moves limited to valid checkers moves given the current board state
