
Tetri Flip Game
===============

Short Description
-----------------
A fast-paced arcade game where the player must switch shapes to match incoming rows.
The goal is to survive as long as possible without hitting the rows.

Installation
------------
1. Make sure Python (3.7 or higher) is installed.
2. Install the required library using pip:
   pip install pygame
3. Run the game using the main file:
   python main.py

How to Play
-----------
- Use WASD keys to move.
- Use keys '[' and ']' to change the player's shape.
- player start with 3 lives
- Match your shape to the approaching row's shape.
- Stand in the correct position to complete the row and gain 100 points.
- Hitting the a row makes the player lose a life and makes the row gray and not completeable.
- The game ends when player lose all lives.
- Press ESC to pause the game.
- Press M to mute game.

Folder Structure
----------------
project-root/
├── main.py          -> Main file that runs the game
├── player.py        -> Handles player logic and behavior
├── row.py           -> Manages rows and collisions
├── /assets/         -> Folder for image and sound assets
│   ├── Trow.png
│   ├── Irow.png
│   ├── LLrow.png
│   └── LRrow.png
└── README.txt       -> This description file

Dependencies
------------
- pygame: 2D game development library

TODO – Future Improvements
--------------------------
- Add powerups
- Multiplayer / co-op mode
- Shop and coin system
- Additional difficulty levels
- improve visuals

Credits
-------
- Noam Abutbul and Yosif stolovitzki
- all sounds made by us except background music
- Inspired by Tetris (background music and shapes)
