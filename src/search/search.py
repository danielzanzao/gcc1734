# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """ DFS para encontrar um caminho até o objetivo."""
    
    from util import Stack

    frontier = Stack()
    frontier.push((problem.getStartState(), []))  

    visited = set()  

    while not frontier.isEmpty():
        current_state, actions = frontier.pop()

        if problem.isGoalState(current_state):
            return actions

        if current_state not in visited:
            visited.add(current_state)

            for successor, action, cost in problem.expand(current_state):
                if successor not in visited:
                    frontier.push((successor, actions + [action]))

    return []


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    from util import Queue  # Usa a fila para gerenciar a fronteira

    # Inicializa a fronteira com o estado inicial e o caminho vazio
    frontier = Queue()
    frontier.push((problem.getStartState(), []))  # (estado, ações para chegar ao estado)

    visited = set()  # Conjunto para rastrear estados visitados

    while not frontier.isEmpty():
        current_state, actions = frontier.pop()

        # Verifica se o estado atual é o objetivo
        if problem.isGoalState(current_state):
            return actions

        # Se ainda não visitado, expande o estado
        if current_state not in visited:
            visited.add(current_state)

            # Use expand para obter os sucessores
            for successor, action, cost in problem.expand(current_state):
                if successor not in visited:
                    frontier.push((successor, actions + [action]))

    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    from util import PriorityQueue  # Usa fila de prioridade para gerenciar a fronteira

    # Inicializa a fronteira com o estado inicial, caminho vazio, e custo acumulado
    frontier = PriorityQueue()
    start_state = problem.getStartState()
    frontier.push((start_state, [], 0), heuristic(start_state, problem))

    visited = {}  # Dicionário para rastrear estados visitados e o menor custo

    while not frontier.isEmpty():
        current_state, actions, g_cost = frontier.pop()

        # Verifica se é o estado objetivo
        if problem.isGoalState(current_state):
            return actions

        # Checa se o estado já foi expandido com menor custo
        if current_state not in visited or g_cost < visited[current_state]:
            visited[current_state] = g_cost

            # Expande os sucessores do estado atual
            for successor, action, step_cost in problem.expand(current_state):
                new_cost = g_cost + step_cost
                total_cost = new_cost + heuristic(successor, problem)
                frontier.push((successor, actions + [action], new_cost), total_cost)

    return []
def iterativeDeepeningSearch(problem):
    """
    Perform Iterative Deepening Depth-First Search (IDS).

    :param problem: The search problem instance to solve.
    :return: A list of actions to reach the goal state.
    """
    def dls(node, depth, visited):
        """
        Perform Depth-Limited Search (DLS).
        
        :param node: Current node in the search tree.
        :param depth: The current depth limit.
        :param visited: Set of visited nodes.
        :return: A tuple (found, actions). If found, actions is the path to the goal.
        """
        if problem.isGoalState(node[0]):
            return True, node[1]  # Return the path if goal is found

        if depth == 0:
            return False, None

        visited.add(node[0])
        for child, action, _ in problem.expand(node[0]):
            if child not in visited:
                found, path = dls((child, node[1] + [action]), depth - 1, visited)
                if found:
                    return True, path
        visited.remove(node[0])
        return False, None

    depth = 0
    while True:
        visited = set()
        start_state = problem.getStartState()
        found, path = dls((start_state, []), depth, visited)
        if found:
            return path
        depth += 1


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ids = iterativeDeepeningSearch
