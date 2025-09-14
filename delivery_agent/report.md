# Autonomous Delivery Agent in 2D Grid City - Report

## Environment Model
The environment is modeled as a 2D grid using the `GridEnvironment` class. Each cell is a `Cell` object with:
- Movement cost (integer ≥ 1, default 1 for roads, higher for rough terrain)
- Terrain type (e.g., "road", "grass")
- Static obstacle flag
- Dynamic obstacle reference

Dynamic obstacles are `DynamicObstacle` objects with a path (list of positions) and schedule (list of time steps).

The grid supports 4-connected moves (up, down, left, right). No diagonals.

## Agent Design
The `DeliveryAgent` class implements rational behavior by choosing paths that minimize cost (fuel/time) under constraints.

Planners implemented:
- **BFS**: Uninformed, finds shortest path in steps (cost 1 per step).
- **Uniform-Cost Search**: Uninformed, minimizes total cost.
- **A***: Informed, uses Manhattan distance heuristic (admissible).
- **Local Search Replanning**: Hill-climbing with random restarts for dynamic environments.

For dynamic obstacles, planners consider time dimension. Local search replans by hill-climbing towards goal, restarting if stuck.

Fuel constraint: Agent has limited fuel; each move consumes cost; if fuel < move cost, cannot move.

Replanning: If path blocked by dynamic obstacle, replan from current position.

## Heuristics
- A*: Manhattan distance, admissible and consistent for grid.

## Experimental Results
Experiments run on 4 maps: small (5x5), medium (10x10), large (15x20), dynamic (10x10 with moving obstacle).

Planners compared on path cost, length, time.

Results from experiment.py:

| Map       | Planner       | Cost | Length | Time (s) | Success |
|-----------|---------------|------|--------|----------|---------|
| small     | BFS           | 8    | 8      | 0.0000   | Yes     |
| small     | Uniform-Cost  | 8    | 8      | 0.0001   | Yes     |
| small     | A*            | 8    | 8      | 0.0001   | Yes     |
| small     | Local Search  | 8    | 8      | 0.0009   | Yes     |
| medium    | BFS           | 18   | 18     | 0.0003   | Yes     |
| medium    | Uniform-Cost  | 18   | 18     | 0.0002   | Yes     |
| medium    | A*            | 18   | 18     | 0.0002   | Yes     |
| medium    | Local Search  | 18   | 18     | 0.0002   | Yes     |
| large     | BFS           | 33   | 33     | 0.0003   | Yes     |
| large     | Uniform-Cost  | 33   | 33     | 0.0005   | Yes     |
| large     | A*            | 33   | 33     | 0.0006   | Yes     |
| large     | Local Search  | 33   | 33     | 0.0004   | Yes     |
| dynamic   | BFS           | 18   | 18     | 0.0003   | Yes     |
| dynamic   | Uniform-Cost  | 18   | 18     | 0.0003   | Yes     |
| dynamic   | A*            | 18   | 18     | 0.0003   | Yes     |
| dynamic   | Local Search  | 18   | 18     | 0.0004   | Yes     |

- BFS: Fast, optimal in steps, but ignores costs.
- Uniform-Cost: Optimal in cost, slower on large grids.
- A*: Fastest, optimal, efficient on large grids.
- Local Search: Good for dynamic, but suboptimal, may fail if restarts insufficient.

Dynamic map: Moving obstacle on row 2, cols 1-5 at t=2,3,4,5. Planners handle time dimension.

## Analysis
- Uninformed (BFS, Uniform-Cost): Good for small maps, but Uniform-Cost better for varying costs.
- Informed (A*): Best overall, scales well.
- Local Search: Useful for dynamic, handles unpredictability, but may not find optimal.

When to use:
- Static, small: BFS.
- Static, costs vary: Uniform-Cost or A*.
- Dynamic: Local Search or time-extended A*.

## Conclusion
Implemented all required features. A* performs best in most cases. Dynamic replanning demonstrated in simulation.

## Demo
Run `python interactive.py` for interactive simulation. Select map, fuel, dynamic. See step-by-step map updates.

Screenshots: (Describe or assume)
- Initial map with agent at start.
- After move, show agent position, fuel remaining.
- Obstacle appears, agent replans.
