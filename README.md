# 🐍 SNAKEGAME

A classic retro **Snake** game with a unique twist! Instead of simply eating apples, every apple you eat becomes a **permanent obstacle**, making the map progressively more challenging. As your snake grows, so does the difficulty.

To make things even more interesting, some apples are **poisonous**, causing you to lose both size and score.

<img width="797" height="798" alt="image" src="https://github.com/user-attachments/assets/39557411-8e4a-4758-8794-6ef5b3be5ca0" />


---

#  Features

-  Classic Snake gameplay with a unique obstacle mechanic
-  Every eaten apple becomes a permanent wall
-  Poison apples reduce your snake's length and score
-  Increasing difficulty as the game progresses
-  Multiple visual themes
-  High score tracking

---

#  Controls

## Start Screen

| Key | Action |
|-----|--------|
| **Space** | Start the game |
| **T** | Change theme |

---

## During the Game

| Key | Action |
|-----|--------|
| **Arrow Keys / WASD** | Move the snake |

### Apples

-  **Normal Apple**
  - +1 Length
  - +1 Score
  - Leaves behind a permanent obstacle

-  **Poison Apple**
  - -1 Length
  - Reduces score

---

## Game Over

| Key | Action |
|-----|--------|
| **Space** | Restart |
| **T** | Change theme |
| **Escape** | Exit the game |

Your **Final Score** will be displayed at the end of each run.

---



#  About the Idea

This project was inspired by a bug I noticed in a video where apples remained on the map after being eaten.

Instead of fixing the bug, I thought:

> "What if that was actually the game mechanic?"

That idea became the core of the game. Every apple turns into a permanent obstacle, forcing the player to constantly adapt as the available space shrinks.

Building this project helped me learn more about:

- Arrays
- `Vector2` logic
- Collision detection
- Game state management with Pygame

I plan to continue expanding the game with new mechanics and features.

<img width="804" height="829" alt="image" src="https://github.com/user-attachments/assets/f3ab1f7c-6b6d-4ed5-95b8-3652b2ab2acc" />


---

# Installation

## 1. Download the project

Click the green **`<> Code`** button at the top of this repository and select **Download ZIP**.

Extract the ZIP file to your computer.

---

## 2. Install Pygame

Open a terminal inside the project folder and run:

```bash
pip install pygame
```

---

## 3. Run the game

<img width="798" height="822" alt="image" src="https://github.com/user-attachments/assets/ebccf03a-4d12-4ab4-84ab-8729bf39049f" />


```bash
python main.py
```

---

#  Built With

- Python
- Pygame

---

#  Gameplay

*(Add screenshots or GIFs here)*

Example:

```
/screenshots/gameplay.png
```

---

# Future Plans

- More obstacle types
- Additional game modes
- Sound effects and music
- Power-ups
- Better animations
- Online leaderboard
- More themes

---

# ❤️ Author

Made with ❤️ by **Rosario Alexandros Morabito**

<img width="798" height="800" alt="image" src="https://github.com/user-attachments/assets/ec2fa6a6-b8b4-4ccf-af3b-c68ca273704d" />

