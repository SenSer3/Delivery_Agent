"""
Main CLI entry point for running delivery agent planners.
"""
import argparse
from environment import GridEnvironment, DynamicObstacle
from agent import DeliveryAgent
import time

def load_map(file_path: str) -> GridEnvironment:
    with open(file_path, 'r') as f:
        lines = [line.strip().split() for line in f.readlines() if line.strip()]
    rows = len(lines)
    cols = len(lines[0])
    env = GridEnvironment(rows, cols)
    for r, row in enumerate(lines):
        for c, ch in enumerate(row):
            if ch == '#':
                env.set_static_obstacle(r, c)
            elif ch.isdigit():
                env.set_terrain_cost(r, c, int(ch))
            else:
                env.set_terrain_cost(r, c, 1)
    return env

def main():
    parser = argparse.ArgumentParser(description="Autonomous Delivery Agent CLI")
    parser.add_argument('--planner', type=str, choices=['bfs', 'uniform_cost', 'a_star', 'local_search'], required=True, help='Planner to use')
    parser.add_argument('--map', type=str, required=True, help='Path to map file')
    parser.add_argument('--start', type=str, default='0,0', help='Start position row,col')
    parser.add_argument('--goal', type=str, default=None, help='Goal position row,col')
    parser.add_argument('--dynamic', action='store_true', help='Enable dynamic obstacles handling')
    args = parser.parse_args()

    env = load_map(args.map)
    dynamic = args.dynamic or 'dynamic' in args.map
    if dynamic:
        # Add a dynamic obstacle: moves right on row 2, cols 1 to 5, at times 2,3,4,5
        obs = DynamicObstacle([(2,1),(2,2),(2,3),(2,4),(2,5)], [2,3,4,5])
        env.add_dynamic_obstacle(obs)

    start = tuple(map(int, args.start.split(',')))
    goal = tuple(map(int, args.goal.split(','))) if args.goal else (env.rows - 1, env.cols - 1)

    agent = DeliveryAgent(env, start, goal)

    print(f"Running planner {args.planner} from {start} to {goal} on map {args.map} with dynamic={dynamic}")
    result = agent.run_planner(args.planner, dynamic=dynamic)

    if result['success']:
        print(f"Path found with cost {result['cost']}, length {result['length']}, time {result['time']:.4f} seconds")
        print("Path:", result['path'])
    else:
        print("No path found.")

if __name__ == '__main__':
    main()
