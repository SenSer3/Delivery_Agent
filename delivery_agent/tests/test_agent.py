import unittest
from environment import GridEnvironment
from agent import DeliveryAgent

class TestDeliveryAgent(unittest.TestCase):
    def setUp(self):
        self.env = GridEnvironment(5, 5)
        self.env.set_static_obstacle(1, 1)
        self.env.set_static_obstacle(2, 3)
        self.agent = DeliveryAgent(self.env, (0, 0), (4, 4))

    def test_bfs_static(self):
        path = self.agent.bfs(dynamic=False)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (4, 4))

    def test_uniform_cost_static(self):
        path = self.agent.uniform_cost_search(dynamic=False)
        self.assertIsNotNone(path)

    def test_a_star_static(self):
        path = self.agent.a_star(dynamic=False)
        self.assertIsNotNone(path)

    def test_local_search_static(self):
        path = self.agent.local_search_replan(dynamic=False)
        self.assertIsNotNone(path)

    def test_no_path(self):
        # Block all paths
        env = GridEnvironment(3, 3)
        for r in range(3):
            for c in range(3):
                if (r, c) != (0, 0) and (r, c) != (2, 2):
                    env.set_static_obstacle(r, c)
        agent = DeliveryAgent(env, (0, 0), (2, 2))
        path = agent.a_star(dynamic=False)
        self.assertIsNone(path)

    def test_fuel_depletion(self):
        # Test fuel in simulation
        from simulate import EnhancedDeliveryAgent
        env = GridEnvironment(5, 5)
        env.set_terrain_cost(0, 1, 2)  # Set cost to 2
        agent = EnhancedDeliveryAgent(env, (0, 0), (4, 4), fuel=1)  # Low fuel
        self.assertFalse(agent.can_move((0, 1)))  # Cost 2 > fuel 1

if __name__ == '__main__':
    unittest.main()
