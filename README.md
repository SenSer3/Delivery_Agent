# Autonomous Delivery Agent in 2D Grid City

## Overview
This project implements an autonomous agent that delivers packages in a 2D grid city. The agent navigates terrain with varying movement costs, static and dynamic obstacles, and uses multiple planning algorithms (BFS, Uniform-cost, A*, local search replanning).

## Features
- Environment modeling: grid, terrain costs, static/dynamic obstacles
- Rational agent: maximizes delivery efficiency (time, fuel)
- Planners: BFS, Uniform-cost, A*, local search (hill-climbing/simulated annealing)
- Dynamic replanning for moving obstacles
- CLI to run planners and select maps
- Experimental comparison and analysis

## Setup
1. Python 3.8+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run planners via CLI (instructions below)

## Folder Structure
- `delivery_agent/` - Source code
- `maps/` - Grid map files
- `tests/` - Unit tests
- `.github/` - Copilot instructions

## Running
Example:
```bash
python delivery_agent/main.py --planner a_star --map maps/medium.txt
```

## Interactive Simulation
You can run an interactive simulation using:
```bash
python delivery_agent/interactive.py
```
This script allows you to:
- Select a map (small, medium, large, dynamic) by entering a number (1-4).
- Choose whether to enable dynamic obstacles (y/n).
- Enter the initial fuel amount (integer).
The agent will plan a path and simulate movement step-by-step, showing the map, agent position, fuel, and replanning if blocked by dynamic obstacles.

## Reproducibility
- All planners and maps are included.
- Tests provided for core functions.

## License
MIT
# Delivery_Agent
# Autonomous Delivery Agent in 2D Grid City

## Overview
This project implements an autonomous agent that delivers packages in a 2D grid city. The agent navigates terrain with varying movement costs, static and dynamic obstacles, and uses multiple planning algorithms (BFS, Uniform-cost, A*, local search replanning).

## Features
- Environment modeling: grid, terrain costs, static/dynamic obstacles
- Rational agent: maximizes delivery efficiency (time, fuel)
- Planners: BFS, Uniform-cost, A*, local search (hill-climbing/simulated annealing)
- Dynamic replanning for moving obstacles
- CLI to run planners and select maps
- Experimental comparison and analysis

## Setup
1. Python 3.8+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run planners via CLI (instructions below)

## Folder Structure
- `delivery_agent/` - Source code
- `maps/` - Grid map files
- `tests/` - Unit tests
- `.github/` - Copilot instructions

## Running
Example:
```bash
python delivery_agent/main.py --planner a_star --map maps/medium.txt
```

## Interactive Simulation
You can run an interactive simulation using:
```bash
python delivery_agent/interactive.py
```
This script allows you to:
- Select a map (small, medium, large, dynamic) by entering a number (1-4).
- Choose whether to enable dynamic obstacles (y/n).
- Enter the initial fuel amount (integer).
The agent will plan a path and simulate movement step-by-step, showing the map, agent position, fuel, and replanning if blocked by dynamic obstacles.

## Reproducibility
- All planners and maps are included.
- Tests provided for core functions.

## License
MIT
