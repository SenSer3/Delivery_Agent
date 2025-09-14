"""
Delivery Agent implementation with various planners.
"""
import heapq
import time
from typing import List, Tuple, Optional, Callable
from environment import GridEnvironment

class DeliveryAgent:
    def __init__(self, env: GridEnvironment, start: Tuple[int, int], goal: Tuple[int, int]):
        self.env = env
        self.start = start
        self.goal = goal

    def bfs(self, dynamic: bool = False) -> Optional[List[Tuple[int, int]]]:
        """
        Breadth-First Search. For dynamic, uses time but cost 1 per step.
        """
        if dynamic:
            return self._uniform_cost_search(dynamic=True, cost_func=lambda r,c: 1)
        # Static BFS
        from collections import deque
        queue = deque([(self.start, 0)])  # (position, steps)
        visited = set([self.start])
        parent = {self.start: None}

        while queue:
            current, steps = queue.popleft()
            if current == self.goal:
                return self._reconstruct_path(parent, current)
            for nr, nc in self.env.neighbors(*current):
                if (nr, nc) not in visited and not self.env.is_occupied(nr, nc, 0):
                    visited.add((nr, nc))
                    queue.append(((nr, nc), steps + 1))
                    parent[(nr, nc)] = current
        return None

    def uniform_cost_search(self, dynamic: bool = False) -> Optional[List[Tuple[int, int]]]:
        """
        Uniform-Cost Search.
        """
        return self._uniform_cost_search(dynamic=dynamic, cost_func=self.env.get_cost)

    def _uniform_cost_search(self, dynamic: bool, cost_func: Callable[[int, int], int]) -> Optional[List[Tuple[int, int]]]:
        """
        Helper for uniform cost and BFS.
        """
        pq = [(0, self.start, 0)]  # (cost, position, time)
        visited = set()
        parent = {}
        cost_so_far = {self.start: 0}

        while pq:
            current_cost, current, t = heapq.heappop(pq)
            if current == self.goal:
                return self._reconstruct_path(parent, current)
            state = (current, t) if dynamic else current
            if state in visited:
                continue
            visited.add(state)
            for nr, nc in self.env.neighbors(*current):
                move_cost = cost_func(nr, nc)
                new_cost = current_cost + move_cost
                new_t = t + 1 if dynamic else 0
                new_state = ((nr, nc), new_t) if dynamic else (nr, nc)
                if new_state not in visited and not self.env.is_occupied(nr, nc, new_t):
                    if (nr, nc) not in cost_so_far or new_cost < cost_so_far[(nr, nc)]:
                        cost_so_far[(nr, nc)] = new_cost
                        heapq.heappush(pq, (new_cost, (nr, nc), new_t))
                        parent[(nr, nc)] = current
        return None

    def a_star(self, dynamic: bool = False) -> Optional[List[Tuple[int, int]]]:
        """
        A* Search with Manhattan heuristic.
        """
        def heuristic(pos):
            return abs(pos[0] - self.goal[0]) + abs(pos[1] - self.goal[1])

        pq = [(0, self.start, 0)]  # (f, position, time)
        visited = set()
        parent = {}
        g_cost = {self.start: 0}

        while pq:
            f, current, t = heapq.heappop(pq)
            if current == self.goal:
                return self._reconstruct_path(parent, current)
            state = (current, t) if dynamic else current
            if state in visited:
                continue
            visited.add(state)
            for nr, nc in self.env.neighbors(*current):
                move_cost = self.env.get_cost(nr, nc)
                new_g = g_cost[current] + move_cost
                new_t = t + 1 if dynamic else 0
                new_state = ((nr, nc), new_t) if dynamic else (nr, nc)
                if new_state not in visited and not self.env.is_occupied(nr, nc, new_t):
                    if (nr, nc) not in g_cost or new_g < g_cost[(nr, nc)]:
                        g_cost[(nr, nc)] = new_g
                        f_new = new_g + heuristic((nr, nc))
                        heapq.heappush(pq, (f_new, (nr, nc), new_t))
                        parent[(nr, nc)] = current
        return None

    def local_search_replan(self, dynamic: bool = False, max_iter: int = 1000) -> Optional[List[Tuple[int, int]]]:
        """
        Local search replanning using hill-climbing with random restarts.
        For simplicity, start from start, try to move towards goal, if blocked, random restart.
        """
        import random
        best_path = None
        best_cost = float('inf')
        for restart in range(10):  # random restarts
            current = self.start
            path = [current]
            cost = 0
            t = 0
            for _ in range(max_iter):
                if current == self.goal:
                    if cost < best_cost:
                        best_cost = cost
                        best_path = path[:]
                    break
                neighbors = [(nr, nc) for nr, nc in self.env.neighbors(*current) if not self.env.is_occupied(nr, nc, t)]
                if not neighbors:
                    break  # stuck
                # Hill-climbing: choose neighbor closest to goal
                def dist(pos):
                    return abs(pos[0] - self.goal[0]) + abs(pos[1] - self.goal[1])
                neighbors.sort(key=dist)
                next_pos = neighbors[0]
                path.append(next_pos)
                cost += self.env.get_cost(*next_pos)
                current = next_pos
                t += 1 if dynamic else 0
            # If not reached, random restart by choosing random start neighbor or something, but simple
        return best_path

    def _reconstruct_path(self, parent: dict, current: Tuple[int, int]) -> List[Tuple[int, int]]:
        path = []
        while current is not None:
            path.append(current)
            current = parent.get(current)
        path.reverse()
        return path

    def run_planner(self, planner_name: str, dynamic: bool = False) -> dict:
        """
        Run a planner and return results.
        """
        planners = {
            'bfs': self.bfs,
            'uniform_cost': self.uniform_cost_search,
            'a_star': self.a_star,
            'local_search': self.local_search_replan
        }
        if planner_name not in planners:
            raise ValueError(f"Unknown planner: {planner_name}")
        start_time = time.time()
        path = planners[planner_name](dynamic)
        end_time = time.time()
        if path:
            cost = sum(self.env.get_cost(r, c) for r, c in path[1:])  # exclude start
            return {
                'path': path,
                'cost': cost,
                'length': len(path) - 1,
                'time': end_time - start_time,
                'success': True
            }
        else:
            return {
                'path': None,
                'cost': None,
                'length': None,
                'time': end_time - start_time,
                'success': False
            }
