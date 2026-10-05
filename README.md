# Dual Degree Project 2026

A Python-based implementation of the core mechanics of the board game Catan. This project models the hexagonal board, resource generation, player turn flow, initial placement, road-building, settlements, and city upgrades in a lightweight simulation environment suitable for experimentation and further extension.

## Overview

This repository focuses on the underlying game logic rather than a full graphical interface. It includes:

- A procedural Catan-style board generation system
- Player resource tracking
- Dice-based resource collection
- Initial settlement and road placement
- Building roads, settlements, and upgraded industries
- Turn management and winner detection
- A simple environment wrapper for simulation-style interaction

## Project Structure

- `app.py` — example script that walks through a full game flow and prints the resulting state
- `board.py` — board topology, tile layout, placement validation, and rendering helpers
- `game.py` — game rules, turn logic, winner checks, and building actions
- `player.py` — player state, resources, and victory points
- `env.py` — environment wrapper for step-based game interaction

## Features

- 2–4 player support
- Randomized board setup using resource tiles and number tokens
- Settlement placement rules with adjacency checks
- Road placement connected to owned settlements or roads
- Industry upgrades from settlements to higher-value structures
- Resource distribution based on dice roll values
- End-of-turn progression and game-over detection
- Minimal environment API for automation or AI experiments

## Requirements

- Python 3
- `numpy`
- `matplotlib`

Install dependencies:

```bash
pip install numpy matplotlib
```

## Running the Project

From the repository root:

```bash
python3 app.py
```

This script demonstrates a valid gameplay sequence:

1. Initial settlement placement
2. Initial road placement
3. Dice roll
4. Resource generation check
5. Road building
6. End-turn transition

The current run was verified successfully and produced output showing the initial placement, successful dice roll, build action, and turn progression.

## Example Usage

```python
from env import CatanEnv

env = CatanEnv(n_players=4)
state = env.reset()

state, reward, done, info = env.step({
    "type": "roll"
})
```

The environment exposes a simple step-based interface that returns:

- the updated game state
- a reward value
- a completion flag
- an action success message

## Gameplay Logic

The game follows the standard Catan flow:

- Players place their initial settlement and road
- Dice are rolled during the main phase
- Resources are awarded to players whose settlements or industries are connected to rolled tiles
- Players can build roads, settlements, and industries if they have enough resources
- The game ends when a player reaches the victory point threshold




