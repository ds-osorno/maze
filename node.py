class Node():
    def __init__(self, state, parent, action):
        self.distance = parent.distance+1 if parent is not None else 0
        self.state = state
        self.parent = parent
        self.action = action
