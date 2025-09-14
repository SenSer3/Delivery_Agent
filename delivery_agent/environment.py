"""
Environment model for autonomous delivery agent.
Models grid, terrain costs, static and dynamic obstacles.
"""
import numpy as np
from typing import List, Tuple, Dict, Optional

class Cell:
    def __init__(self, cost: int = 1, terrain: str = "road", is_obstacle: bool = False):
        self.cost = cost
        self.terrain = terrain
        self.is_obstacle = is_obstacle
        self.dynamic_obstacle = None  # Can be set to a DynamicObstacle

class DynamicObstacle:
    def __init__(self, path: List[Tuple[int, int]], schedule: List[int]):
        """
        path: list of (row, col) positions
        schedule: list of time steps when obstacle occupies each position
        """
        self.path = path
        self.schedule = schedule

class GridEnvironment:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.dynamic_obstacles: List[DynamicObstacle] = []

    def set_static_obstacle(self, row: int, col: int):
        self.grid[row][col].is_obstacle = True

    def set_terrain_cost(self, row: int, col: int, cost: int, terrain: str = "road"):
        self.grid[row][col].cost = cost
        self.grid[row][col].terrain = terrain

    def add_dynamic_obstacle(self, obstacle: DynamicObstacle):
        self.dynamic_obstacles.append(obstacle)

    def is_occupied(self, row: int, col: int, time: int) -> bool:
        if self.grid[row][col].is_obstacle:
            return True
        for obs in self.dynamic_obstacles:
            for pos, t in zip(obs.path, obs.schedule):
                if pos == (row, col) and t == time:
                    return True
        return False

    def get_cost(self, row: int, col: int) -> int:
        return self.grid[row][col].cost

    def neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        moves = [(-1,0), (1,0), (0,-1), (0,1)] # up, down, left, right
        result = []
        for dr, dc in moves:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                result.append((nr, nc))
        return result
