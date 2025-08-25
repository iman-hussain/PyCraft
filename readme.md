
# PyCraft 🧱

A simple and fun voxel-based sandbox game built with Python and the Ursina engine. Create, build, and save your 3D creations in a colorful block world!

![Ui Image](https://raw.githubusercontent.com/iman-hussain/PyCraft/refs/heads/main/PyCraft%20UI.png)

## Features

* **First-Person 3D World:** Explore a flat, open canvas.
* **Block Placement & Destruction:** Build and destroy with a simple click.
* **8 Vibrant Colors:** Choose from a wide palette of colors for your blocks.
* **Intuitive UI:** An easy-to-use toolbar shows your selected block.
* **Save & Load System:** Save your creations as `.pycraft` files and load them later using your system's file explorer.

## Installation Guide

To get PyCraft running on your system, follow these simple steps.

### 1. Install Python

PyCraft is built with Python. If you don't have Python installed, you'll need to download it first.

* Go to the official Python website: [python.org/downloads](https://www.python.org/downloads/ "null")
* Download the latest version for your operating system (Windows, macOS, or Linux).
* Run the installer. **Important:** On Windows, make sure to check the box that says **"Add Python to PATH"** during installation.

### 2. Install Ursina

This project depends on the Ursina game engine. You can install it using `pip`, Python's package manager.

* Open your terminal or command prompt.
* Run the following command:

```
pip install ursina

```

## How to Run the Game

1. Save the game's code as a Python file (e.g., `pycraft.py`).
2. Open your terminal or command prompt.
3. Navigate to the directory where you saved the file.
4. Run the game with the following command:

```
python pycraft.py

```

The game window should now appear!

## How to Play

### Controls

| **Key / Action** | **Description**                       |
| ---------------------- | ------------------------------------------- |
| **W, A, S, D**   | Move the player forward, left, back, right. |
| **Mouse**        | Look around.                                |
| **Space Bar**    | Jump.                                       |
| **Left Mouse**   | Destroy a block.                            |
| **Right Mouse**  | Place a block.                              |
| **Mouse Wheel**  | Cycle through the block colors.             |
| **Keys 1-8**     | Select a specific block color.              |
| **Escape (Esc)** | Open or close the Pause Menu.               |

### Menus

#### Title Screen

When you first launch the game, you will see the main title screen with two options:

* **New Canvas:** Starts a brand new, empty world for you to build in.
* **Load Canvas:** Opens your system's file explorer, allowing you to select and load a previously saved `.pycraft` file.

#### Pause Menu

Pressing the `Escape` key at any time during gameplay will pause the game and bring up this menu.

* **Return:** Closes the menu and resumes your game.
* **Save Canvas:** Opens your system's file explorer, allowing you to save your current creation as a `.pycraft` file.
* **Load Canvas:** Discards your current session and lets you load a different
