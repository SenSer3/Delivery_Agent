"""
Run experiments to compare planners.
"""
import time
from environment import GridEnvironment, DynamicObstacle
from agent import DeliveryAgent

def run_experiments():
    maps = ['maps/small.txt', 'maps/medium.txt', 'maps/large.txt', 'maps/dynamic.txt']
    planners = ['bfs', 'uniform_cost', 'a_star', 'local_search']
    results = {}

    for map_file in maps:
        print(f"Testing map: {map_file}")
        env = load_map(map_file)
        dynamic = 'dynamic' in map_file
        if dynamic:
            obs = DynamicObstacle([(2,1),(2,2),(2,3),(2,4),(2,5)], [2,3,4,5])
            env.add_dynamic_obstacle(obs)
        start = (0, 0)
        goal = (env.rows - 1, env.cols - 1)
        agent = DeliveryAgent(env, start, goal)

        for planner in planners:
            print(f"  Planner: {planner}")
            result = agent.run_planner(planner, dynamic=dynamic)
            key = (map_file, planner)
            results[key] = result
            if result['success']:
                print(f"    Cost: {result['cost']}, Length: {result['length']}, Time: {result['time']:.4f}")
            else:
                print("    No path found")

    return results

def load_map(file_path: str):
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

if __name__ == '__main__':
    results = run_experiments()
    # Print summary
    for key, res in results.items():
        if res['success']:
            print(f"{key}: cost={res['cost']}, time={res['time']:.4f}")
