"""
Simulate agent movement and replanning with dynamic obstacles, fuel, and time tracking.
"""
from environment import GridEnvironment, DynamicObstacle
from agent import DeliveryAgent

class EnhancedDeliveryAgent(DeliveryAgent):
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

def simulate_replanning():
    env = GridEnvironment(5, 5)
    env.set_static_obstacle(1, 1)
    # env.set_static_obstacle(2, 3)  # Removed to allow path through (3,3)
    # Dynamic obstacle: blocks (3,3) at t=6, simulating a vehicle appearing
    obs = DynamicObstacle([(3, 3)], [6])
    env.add_dynamic_obstacle(obs)

    start = (0, 0)
    goal = (4, 4)
    agent = EnhancedDeliveryAgent(env, start, goal, fuel=50)  # Limited fuel

    print("=== Simulation: Agent Movement with Dynamic Obstacles, Fuel, and Time ===")
    print(f"Start: {start}, Goal: {goal}, Initial Fuel: {agent.fuel}")
    print("Static obstacles: (1,1), (2,3)")
    print("Dynamic obstacle path: [(2,1) at t=3, (2,2) at t=4, (2,3) at t=5]")
    print()

    # Plan initial path using A*
    print("Planning initial path using A*...")
    result = agent.run_planner('a_star', dynamic=True)
    if not result['success']:
        print("No initial path found.")
        return
    path = result['path']
    print(f"Initial path (A*): {path}")
    print(f"Path cost: {result['cost']}, Length: {result['length']}")
    print()

    # Simulate movement
    current_pos = start
    t = 0
    total_cost = 0
    while current_pos != goal:
        print(f"Time {t}: At {current_pos}, Fuel: {agent.fuel}")
        # Show dynamic obstacles at current time
        obstacles_at_t = [(obs.path[i], obs.schedule[i]) for obs in env.dynamic_obstacles for i in range(len(obs.path)) if obs.schedule[i] == t]
        if obstacles_at_t:
            print(f"  Dynamic obstacles at t={t}: {obstacles_at_t}")

        # Check if next move is blocked
        next_pos = path[path.index(current_pos) + 1] if path.index(current_pos) + 1 < len(path) else goal
        move_cost = env.get_cost(*next_pos)
        print(f"  Next move to {next_pos}, cost: {move_cost}")

        if env.is_occupied(next_pos[0], next_pos[1], t + 1):
            print(f"  Obstacle detected at {next_pos} at time {t+1}, replanning...")
            # Replan using local search (hill-climbing with restarts)
            print("  Replanning using Local Search (hill-climbing with random restarts)...")
            temp_agent = EnhancedDeliveryAgent(env, current_pos, goal, agent.fuel)
            new_result = temp_agent.run_planner('local_search', dynamic=True)
            if new_result['success']:
                new_path = new_result['path']
                print(f"  New path (Local Search): {new_path}")
                print(f"  New path cost: {new_result['cost']}, Length: {new_result['length']}")
                path = [current_pos] + new_path  # Update path
                next_pos = path[1]
                move_cost = env.get_cost(*next_pos)
            else:
                print("  Replanning failed. Agent stuck.")
                break

        if not agent.can_move(next_pos):
            print(f"  Insufficient fuel to move to {next_pos} (need {move_cost}, have {agent.fuel}). Agent stuck.")
            break

        # Move
        if agent.move(next_pos):
            total_cost += move_cost
            current_pos = next_pos
            t += 1
            print(f"  Moved to {current_pos}, fuel now: {agent.fuel}")
        else:
            print("  Move failed due to fuel.")
            break

        if current_pos == goal:
            print(f"Reached goal at time {t}, total cost: {total_cost}, remaining fuel: {agent.fuel}")
            break
        print()

    if current_pos != goal:
        print("Simulation ended without reaching goal.")

if __name__ == '__main__':
    simulate_replanning()
