"""
Interactive interface for delivery agent simulation.
Allows user to choose fuel, map, dynamic obstacles, and shows map progress.
"""
from environment import GridEnvironment, DynamicObstacle
from agent import DeliveryAgent

class InteractiveDeliveryAgent(DeliveryAgent):
    def __init__(self, env, start, goal, fuel=100):
        super().__init__(env, start, goal)
        self.fuel = fuel

    def can_move(self, pos):
        cost = self.env.get_cost(*pos)
        return self.fuel >= cost

    def move(self, pos):
        cost = self.env.get_cost(*pos)
        if self.fuel >= cost:
            self.fuel -= cost
            return True
        return False

def print_map(env, agent_pos, t, agent):
    print(f"\nMap at time {t}:")
    for r in range(env.rows):
        row = ""
        for c in range(env.cols):
            if (r, c) == agent_pos:
                row += "A-"  # Agent
            elif env.grid[r][c].is_obstacle:
                row += "#-"  # Static obstacle
            elif any(pos == (r, c) and s == t for obs in env.dynamic_obstacles for pos, s in zip(obs.path, obs.schedule)):
                row += "O-"  # Dynamic obstacle at this time
            else:
                cost = env.grid[r][c].cost
                row += f"{cost}-"
        print(row.rstrip('-'))  # Remove trailing -
    print(f"Agent fuel: {agent.fuel}")

def load_map(file_path: str) -> GridEnvironment:
    with open(file_path, 'r') as f:
        lines = [line.strip().split('-') for line in f.readlines() if line.strip()]
    rows = len(lines)
    cols = max(len(row) for row in lines) if lines else 0
    env = GridEnvironment(rows, cols)
    for r, row in enumerate(lines):
        for c in range(cols):
            ch = row[c] if c < len(row) else '1'
            if ch == '#':
                env.set_static_obstacle(r, c)
            elif ch.isdigit():
                env.set_terrain_cost(r, c, int(ch))
            else:
                env.set_terrain_cost(r, c, 1)
    return env

def main():
    print("=== Interactive Delivery Agent Simulation ===")

    # Choose map
    maps = {
        '1': ('maps/small.txt', 'Small map'),
        '2': ('maps/medium.txt', 'Medium map'),
        '3': ('maps/large.txt', 'Large map'),
        '4': ('maps/dynamic.txt', 'Dynamic map')
    }
    print("Choose map:")
    for k, v in maps.items():
        print(f"{k}. {v[1]}")
    map_choice = input("Enter choice (1-4): ").strip()
    if map_choice not in maps:
        print("Invalid choice.")
        return
    map_file, _ = maps[map_choice]
    env = load_map(map_file)

    # Dynamic obstacles
    dynamic = input("Enable dynamic obstacles? (y/n): ").strip().lower() == 'y'
    if dynamic:
        # Add multiple dynamic obstacles, adjusted for map size
        max_col = env.cols - 1
        obs1 = DynamicObstacle([(2,1),(2,2),(2,3),(2,4),(2,min(4,max_col))], [2,3,4,5])  # Moves right on row 2
        env.add_dynamic_obstacle(obs1)
        obs2 = DynamicObstacle([(1,3),(2,3),(3,3),(min(4,env.rows-1),3)], [3,4,5,6])  # Moves down on col 3
        env.add_dynamic_obstacle(obs2)
        obs3 = DynamicObstacle([(3,1),(3,2),(3,min(3,max_col))], [4,5,6])  # Moves right on row 3
        env.add_dynamic_obstacle(obs3)
        print("Dynamic obstacles added:")
        print(f"  Obstacle 1: Moves right on row 2 from col 1 to {min(4,max_col)} at times 2-5")
        print(f"  Obstacle 2: Moves down on col 3 from row 1 to {min(4,env.rows-1)} at times 3-6")
        print(f"  Obstacle 3: Moves right on row 3 from col 1 to {min(3,max_col)} at times 4-6")

    # Fuel
    fuel = int(input("Enter initial fuel (e.g., 50): ").strip())

    start = (0, 0)
    goal = (env.rows - 1, env.cols - 1)
    agent = InteractiveDeliveryAgent(env, start, goal, fuel)

    print(f"Start: {start}, Goal: {goal}, Fuel: {fuel}, Dynamic: {dynamic}")

    # Plan initial path using A*
    print("\nPlanning initial path using A*...")
    result = agent.run_planner('a_star', dynamic=dynamic)
    if not result['success']:
        print("No initial path found.")
        return
    path = result['path']
    print(f"Initial path: {path}")

    # Simulate movement
    current_pos = start
    t = 0
    total_cost = 0
    print_map(env, current_pos, t, agent)

    while current_pos != goal:
        # Check if next move is blocked
        next_pos = path[path.index(current_pos) + 1] if path.index(current_pos) + 1 < len(path) else goal
        move_cost = env.get_cost(*next_pos)

        if env.is_occupied(next_pos[0], next_pos[1], t + 1):
            print(f"Obstacle detected at {next_pos} at time {t+1}, replanning...")
            # Replan using local search
            temp_agent = InteractiveDeliveryAgent(env, current_pos, goal, agent.fuel)
            new_result = temp_agent.run_planner('local_search', dynamic=dynamic)
            if new_result['success']:
                new_path = new_result['path']
                print(f"New path: {new_path}")
                path = [current_pos] + new_path
                next_pos = path[1]
                move_cost = env.get_cost(*next_pos)
            else:
                print("Replanning failed. Agent stuck.")
                break

        if not agent.can_move(next_pos):
            print(f"Insufficient fuel to move to {next_pos} (need {move_cost}, have {agent.fuel}). Agent stuck.")
            break

        # Move
        if agent.move(next_pos):
            total_cost += move_cost
            current_pos = next_pos
            t += 1
            print_map(env, current_pos, t, agent)
        else:
            print("Move failed due to fuel.")
            break

        if current_pos == goal:
            print(f"Reached goal at time {t}, total cost: {total_cost}, remaining fuel: {agent.fuel}")
            break

    if current_pos != goal:
        print("Simulation ended without reaching goal.")

if __name__ == '__main__':
    main()
