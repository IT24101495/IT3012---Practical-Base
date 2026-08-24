
# agent.py
class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)
    
class SimpleReflexAgent:
    def sense_and_act(self, percept):

        # IF food is here THEN stay
        if percept['food_here']:
            return 'Stay'

        # IF wall is ahead THEN turn left
        if percept['wall_ahead']:
            return 'TurnLeft'

        # ELSE move forward
        return 'Forward'
    
class ModelBasedAgent:

    def __init__(self):
        self.visited_cells = set()
        self.position = (0, 0)
        self.facing = 'Up'
        self.last_action = None
        self.last_percept = None

    def sense_and_act(self, percept):

        # Update internal memory
        self.last_percept = percept
        self.visited_cells.add(self.position)

        # ------------------------------------------------
        # IF-THEN RULES
        # ------------------------------------------------

        # IF food is here THEN stay
        if percept['food_here']:
            action = 'Stay'

        # IF wall ahead AND left is visited THEN turn right
        elif percept['wall_ahead'] and self.is_left_visited():
            action = 'TurnRight'

        # IF wall ahead AND left is a wall THEN turn right
        elif percept['wall_ahead'] and self.is_left_wall(percept):
            action = 'TurnRight'

        # IF ahead is visited AND left is visited/wall
        # THEN turn right
        elif (
            self.is_ahead_visited()
            and (
                self.is_left_visited()
                or self.is_left_wall(percept)
            )
        ):
            action = 'TurnRight'

        # IF ahead is visited AND right is not a wall
        # AND right is not visited THEN turn right
        elif (
            self.is_ahead_visited()
            and not self.is_right_wall(percept)
            and not self.is_right_visited()
        ):
            action = 'TurnRight'

        # IF ahead is visited AND left is available
        # THEN turn left
        elif (
            self.is_ahead_visited()
            and not self.is_left_wall(percept)
            and not self.is_left_visited()
        ):
            action = 'TurnLeft'

        # IF ahead is visited AND both left/right are blocked
        # THEN turn around
        elif (
            self.is_ahead_visited()
            and (
                self.is_left_wall(percept)
                or self.is_left_visited()
            )
            and (
                self.is_right_wall(percept)
                or self.is_right_visited()
            )
        ):
            action = 'TurnRight'

        # IF wall ahead THEN turn left
        elif percept['wall_ahead']:
            action = 'TurnLeft'

        # ELSE move forward
        else:
            action = 'Forward'

        # Update internal model
        self.update_state(action, percept)

        # Remember last action
        self.last_action = action

        return action

    # ------------------------------------------------
    # CHECK WHETHER LEFT CELL HAS BEEN VISITED
    # ------------------------------------------------

    def is_left_visited(self):

        x, y = self.position

        if self.facing == 'Up':
            left_position = (x - 1, y)

        elif self.facing == 'Left':
            left_position = (x, y - 1)

        elif self.facing == 'Down':
            left_position = (x + 1, y)

        else:  # Right
            left_position = (x, y + 1)

        return left_position in self.visited_cells

    # ------------------------------------------------
    # CHECK WHETHER RIGHT CELL HAS BEEN VISITED
    # ------------------------------------------------

    def is_right_visited(self):

        x, y = self.position

        if self.facing == 'Up':
            right_position = (x + 1, y)

        elif self.facing == 'Right':
            right_position = (x, y - 1)

        elif self.facing == 'Down':
            right_position = (x - 1, y)

        else:  # Left
            right_position = (x, y + 1)

        return right_position in self.visited_cells

    # ------------------------------------------------
    # CHECK WHETHER LEFT IS A WALL
    # ------------------------------------------------

    def is_left_wall(self, percept):

        if self.facing == 'Up':
            return percept['wall_left']

        elif self.facing == 'Left':
            return percept['wall_down']

        elif self.facing == 'Down':
            return percept['wall_right']

        else:  # Right
            return percept['wall_up']

    # ------------------------------------------------
    # CHECK WHETHER RIGHT IS A WALL
    # ------------------------------------------------

    def is_right_wall(self, percept):

        if self.facing == 'Up':
            return percept['wall_right']

        elif self.facing == 'Right':
            return percept['wall_down']

        elif self.facing == 'Down':
            return percept['wall_left']

        else:  # Left
            return percept['wall_up']

    # ------------------------------------------------
    # CHECK WHETHER AHEAD HAS BEEN VISITED
    # ------------------------------------------------

    def is_ahead_visited(self):

        x, y = self.position

        if self.facing == 'Up':
            ahead = (x, y + 1)

        elif self.facing == 'Down':
            ahead = (x, y - 1)

        elif self.facing == 'Left':
            ahead = (x - 1, y)

        else:  # Right
            ahead = (x + 1, y)

        return ahead in self.visited_cells

    # ------------------------------------------------
    # UPDATE INTERNAL STATE
    # ------------------------------------------------

    def update_state(self, action, percept):

        # Turn left
        if action == 'TurnLeft':

            if self.facing == 'Up':
                self.facing = 'Left'

            elif self.facing == 'Left':
                self.facing = 'Down'

            elif self.facing == 'Down':
                self.facing = 'Right'

            elif self.facing == 'Right':
                self.facing = 'Up'

        # Turn right
        elif action == 'TurnRight':

            if self.facing == 'Up':
                self.facing = 'Right'

            elif self.facing == 'Right':
                self.facing = 'Down'

            elif self.facing == 'Down':
                self.facing = 'Left'

            elif self.facing == 'Left':
                self.facing = 'Up'

        # Move forward
        elif action == 'Forward':

            # Do not update internal position if wall is ahead
            if percept['wall_ahead']:
                return

            x, y = self.position

            if self.facing == 'Up':
                self.position = (x, y + 1)

            elif self.facing == 'Down':
                self.position = (x, y - 1)

            elif self.facing == 'Left':
                self.position = (x - 1, y)

            elif self.facing == 'Right':
                self.position = (x + 1, y)
                

from collections import deque
import heapq

class SearchAgent:

    def __init__(self, algorithm="BFS"):
        self.algorithm = algorithm  # Default algorithm
        self.last_action = None

    # --------------------------------------------------
    # BFS - Breadth First Search
    # FIFO Queue
    # --------------------------------------------------

    def bfs_search(self, start, goal, walls, grid_size):

        queue = deque()
        queue.append((start, []))

        reached = {start}

        while queue:

            current, path = queue.popleft()

            if current == goal:
                return path

            for action, neighbor in self.get_neighbors(
                current, walls, grid_size
            ):

                if neighbor not in reached:
                    reached.add(neighbor)

                    queue.append(
                        (neighbor, path + [action])
                    )

        return None

    # --------------------------------------------------
    # DFS - Depth First Search
    # LIFO Stack
    # --------------------------------------------------

    def dfs_search(self, start, goal, walls, grid_size):

        stack = []
        stack.append((start, []))

        reached = {start}

        while stack:

            current, path = stack.pop()

            if current == goal:
                return path

            for action, neighbor in self.get_neighbors(
                current, walls, grid_size
            ):

                if neighbor not in reached:
                    reached.add(neighbor)

                    stack.append(
                        (neighbor, path + [action])
                    )

        return None

    # --------------------------------------------------
    # UCS - Uniform Cost Search
    # Priority Queue
    # --------------------------------------------------

    def ucs_search(self, start, goal, walls, grid_size):

        priority_queue = []

        # (total_cost, current_position, path)
        heapq.heappush(
            priority_queue,
            (0, start, [])
        )

        reached = set()
        reached.add(start)

        while priority_queue:

            cost, current, path = heapq.heappop(priority_queue)

            if current == goal:
                return path

            for action, neighbor in self.get_neighbors(
                current, walls, grid_size
            ):

                if neighbor not in reached:

                    reached.add(neighbor)

                    new_cost = cost + 1

                    heapq.heappush(
                        priority_queue,
                        (
                            new_cost,
                            neighbor,
                            path + [action]
                        )
                    )

        return None

    def sense_and_act(self, percept):

        start = percept['agent_pos']

        if not percept['all_food']:
            return 'Stay'

        goal = percept['all_food'][0]

        if self.algorithm == "BFS":
            path = self.bfs_search(
                start,
                goal,
                percept['walls'],
                percept['grid_size']
            )

        elif self.algorithm == "DFS":
            path = self.dfs_search(
                start,
                goal,
                percept['walls'],
                percept['grid_size']
            )

        elif self.algorithm == "UCS":
            path = self.ucs_search(
                start,
                goal,
                percept['walls'],
                percept['grid_size']
            )

        else:
            return 'Stay'
        
        if path:
            action = path[0]
            self.last_action = action
            return action

        return 'Stay'

    # --------------------------------------------------
    # Generate valid neighboring states
    # --------------------------------------------------

    def get_neighbors(self, position, walls, grid_size):

        x, y = position

        width, height = grid_size

        neighbors = []

        possible_moves = [
            ('Up', (x, y + 1)),
            ('Down', (x, y - 1)),
            ('Left', (x - 1, y)),
            ('Right', (x + 1, y))
        ]

        for action, (nx, ny) in possible_moves:

            # Check boundaries
            if nx < 0 or nx >= width:
                continue

            if ny < 0 or ny >= height:
                continue

            # Check walls
            if (nx, ny) in walls:
                continue

            neighbors.append(
                (action, (nx, ny))
            )

        return neighbors
