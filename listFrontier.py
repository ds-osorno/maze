from node import Node
from stackfrontier import StackFrontier


class ListFrontier(StackFrontier):
    def remove(self, node):
        self.frontier.remove(node)

    def all(self):
        return self.frontier
