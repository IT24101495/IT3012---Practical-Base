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
        
        self.path = []  # To keep track of the path taken

    def sense_and_act(self, percept):

        self.last_percept = percept

        # Remember current cell
        if self.position not in self.visited_cells:
            self.visited_cells.add(self.position)
            self.path.append(self.position)

        # If food is here, collect it
        if percept['food_here']:
            action = 'Stay'

        else:
            # Find valid unvisited neighboring cells
            candidates = self.get_unvisited_neighbors(percept)

            if candidates:
                # Choose the first unexplored direction
                direction = candidates[0]
                action = self.turn_towards(direction)

            else:
                # No unexplored cells nearby.
                # Backtrack to the previous cell in the path
                action = self.backtrack(percept)

        self.update_state(action, percept)

        self.last_action = action

        return action
    
    def backtrack(self, percept):

    # If there is nowhere to backtrack to,
    # rotate to search for another direction.
        if len(self.path) <= 1:
            return 'TurnRight'

    # Previous position in the exploration path
        previous_position = self.path[-2]

        x, y = self.position
        px, py = previous_position

    # Determine which direction leads back
        if px == x and py == y + 1:
            direction = 'Up'

        elif px == x and py == y - 1:
            direction = 'Down'

        elif px == x - 1 and py == y:
            direction = 'Left'

        elif px == x + 1 and py == y:
            direction = 'Right'

        else:
            return 'TurnRight'

        return self.turn_towards(direction)

    def get_unvisited_neighbors(self, percept):

        x, y = self.position

        neighbors = []

        # Prefer directions based on current orientation
        if self.facing == 'Up':
            directions = [
                ('Left',  (x - 1, y), percept['wall_left']),
                ('Up',    (x, y + 1), percept['wall_up']),
                ('Right', (x + 1, y), percept['wall_right']),
                ('Down',  (x, y - 1), percept['wall_down'])
            ]

        elif self.facing == 'Right':
            directions = [
                ('Up',    (x, y + 1), percept['wall_up']),
                ('Right', (x + 1, y), percept['wall_right']),
                ('Down',  (x, y - 1), percept['wall_down']),
                ('Left',  (x - 1, y), percept['wall_left'])
            ]

        elif self.facing == 'Down':
            directions = [
                ('Right', (x + 1, y), percept['wall_right']),
                ('Down',  (x, y - 1), percept['wall_down']),
                ('Left',  (x - 1, y), percept['wall_left']),
                ('Up',    (x, y + 1), percept['wall_up'])
            ]

        else:  # Left
            directions = [
                ('Down',  (x, y - 1), percept['wall_down']),
                ('Left',  (x - 1, y), percept['wall_left']),
                ('Up',    (x, y + 1), percept['wall_up']),
                ('Right', (x + 1, y), percept['wall_right'])
            ]

        for direction, position, blocked in directions:

            # Ignore walls
            if blocked:
                continue

            # Ignore already visited cells
            if position in self.visited_cells:
                continue

            neighbors.append(direction)

        return neighbors

    def turn_towards(self, direction):

        if direction == self.facing:
            return 'Forward'

        if self.facing == 'Up':

            if direction == 'Left':
                return 'TurnLeft'

            if direction == 'Right':
                return 'TurnRight'

            if direction == 'Down':
                return 'TurnRight'

        elif self.facing == 'Right':

            if direction == 'Up':
                return 'TurnLeft'

            if direction == 'Down':
                return 'TurnRight'

            if direction == 'Left':
                return 'TurnRight'

        elif self.facing == 'Down':

            if direction == 'Right':
                return 'TurnLeft'

            if direction == 'Left':
                return 'TurnRight'

            if direction == 'Up':
                return 'TurnRight'

        elif self.facing == 'Left':

            if direction == 'Down':
                return 'TurnLeft'

            if direction == 'Up':
                return 'TurnRight'

            if direction == 'Right':
                return 'TurnRight'

        return 'TurnRight'

    def update_state(self, action, percept):

        if action == 'TurnLeft':

            if self.facing == 'Up':
                self.facing = 'Left'

            elif self.facing == 'Left':
                self.facing = 'Down'

            elif self.facing == 'Down':
                self.facing = 'Right'

            elif self.facing == 'Right':
                self.facing = 'Up'

        elif action == 'TurnRight':

            if self.facing == 'Up':
                self.facing = 'Right'

            elif self.facing == 'Right':
                self.facing = 'Down'

            elif self.facing == 'Down':
                self.facing = 'Left'

            elif self.facing == 'Left':
                self.facing = 'Up'

        elif action == 'Forward':

            # Do not update internal position if there is a wall
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
