import search
import random
from random import randint
import util

# Module Classes

class TwoJarsState:
    """
    This class represents a configuration of the two jars.
    """

    def __init__(self, volumes):
        """
          Constructs a new configuration.

        The configuration of the two jars is stored in a dict. 
         - The first position stores the amount of water in the first jar (with capacity 4l).
         - The second position stores the amount of water in the second jar (with capacity 3l).
        """
        self.jars = {"J4": volumes[0], "J3": volumes[1]}
        assert (self.jars["J4"] >= 0 and self.jars["J4"] <= 4)
        assert (self.jars["J3"] >= 0 and self.jars["J3"] <= 3)

    def isGoal(self):
        """
        Checks to see if the pair of jars is in its goal state.

        The goal is to have 2 liters in the 4-liter jar.

        >>> TwoJarsState((2, 1)).isGoal()
        True

        >>> TwoJarsState((2, 0)).isGoal()
        True

        >>> TwoJarsState((1, 0)).isGoal()
        False
        """
        return self.jars["J4"] == 2

    def legalMoves(self):
        """
        Returns a list of legal actions from the current state.

        Actions consist of the following:
        - fillJ3 (fill 3-liter jar)
        - fillJ4 (fill 4-liter jar)
        - pourJ3intoJ4 (pour from 3-liter jar into 4-liter jar)
        - pourJ4intoJ3 (pour from 4-liter jar into 3-liter jar)
        - emptyJ3 (empty 3-liter jar)
        - emptyJ4 (empty 4-liter jar)
        
        These are encoded as strings: 'fillJ3', 'fillJ4', 
        'pourJ3intoJ4', 'pourJ4intoJ3', 'emptyJ3', 'emptyJ4'.

        >>> TwoJarsState((1, 3)).legalMoves()
        ['fillJ4', 'pourJ3intoJ4', 'emptyJ3', 'emptyJ4']
        """
        moves = []

        if self.jars["J4"] < 4:  # Can fill J4
            moves.append("fillJ4")
        if self.jars["J3"] < 3:  # Can fill J3
            moves.append("fillJ3")
        if self.jars["J3"] > 0:  # Can pour J3 into J4
            moves.append("pourJ3intoJ4")
        if self.jars["J4"] > 0:  # Can pour J4 into J3
            moves.append("pourJ4intoJ3")
        if self.jars["J3"] > 0:  # Can empty J3
            moves.append("emptyJ3")
        if self.jars["J4"] > 0:  # Can empty J4
            moves.append("emptyJ4")

        return moves

    def result(self, move):
        """
        Returns an object TwoJarsState with the current state based on the provided move.

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception, which may be an array bounds
        exception.

        NOTE: This function *does not* change the current object. Instead,
        it returns a new object.
        """
        new_state = TwoJarsState((self.jars["J4"], self.jars["J3"]))

        if move == "fillJ4":
            new_state.jars["J4"] = 4
        elif move == "fillJ3":
            new_state.jars["J3"] = 3
        elif move == "emptyJ4":
            new_state.jars["J4"] = 0
        elif move == "emptyJ3":
            new_state.jars["J3"] = 0
        elif move == "pourJ3intoJ4":
            transfer = min(new_state.jars["J3"], 4 - new_state.jars["J4"])
            new_state.jars["J3"] -= transfer
            new_state.jars["J4"] += transfer
        elif move == "pourJ4intoJ3":
            transfer = min(new_state.jars["J4"], 3 - new_state.jars["J3"])
            new_state.jars["J4"] -= transfer
            new_state.jars["J3"] += transfer
        else:
            raise ValueError(f"Illegal move: {move}")

        return new_state

    def __eq__(self, other):
        """
        Overloads '==' such that two pairs of jars with the same volume of water
        are equal.

        >>> TwoJarsState((0, 1)) == TwoJarsState((1, 0)).result('pourJ4intoJ3')
        True
        """
        return self.jars == other.jars

    def __hash__(self):
        return hash((self.jars["J4"], self.jars["J3"]))

    def __getAsciiString(self):
        """
        Returns a display string for the jars
        """
        return f"J4: {self.jars['J4']} | J3: {self.jars['J3']}"

    def __str__(self):
        return self.__getAsciiString()


class TwoJarsSearchProblem(search.SearchProblem):
    """
      Implementation of a SearchProblem for the Two Jars domain

      Each state is represented by an instance of an TwoJarsState.
    """
    def __init__(self, start_state):
        "Creates a new TwoJarsSearchProblem which stores search information."
        self.start_state = start_state

    def getStartState(self):
        return self.start_state

    def isGoalState(self,state):
        return state.isGoal()

    def expand(self,state):
        """
          Returns list of (child, action, stepCost) pairs where
          each child is either left, right, up, or down
          from the original state and the cost is 1.0 for each
        """
        child = []
        for a in self.getActions(state):
            next_state = self.getNextState(state, a)
            child.append((next_state, a, self.getActionCost(state, a, next_state)))
        return child

    def getActions(self, state):
        return state.legalMoves()

    def getActionCost(self, state, action, next_state):
        assert next_state == state.result(action), (
            "getActionCost() called on incorrect next state.")
        return 1

    def getNextState(self, state, action):
        assert action in state.legalMoves(), (
            "getNextState() called on incorrect action")
        return state.result(action)

    def getCostOfActionSequence(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)

def createRandomTwoJarsState(moves=10):
    """
      moves: number of random moves to apply

      Creates a random state by applying a series 
      of 'moves' random moves to a solved state.
    """
    volume_of_J3 = randint(0, 3)
    a_state = TwoJarsState((2,volume_of_J3))
    for i in range(moves):
        # Execute a random legal move
        a_state = a_state.result(random.sample(a_state.legalMoves(), 1)[0])
    return a_state

if __name__ == '__main__':
    start_state = createRandomTwoJarsState(8)
    print('A random initial state:')
    print(start_state)

    problem = TwoJarsSearchProblem(start_state)
    path = search.breadthFirstSearch(problem)
    print('BFS found a path of %d moves: %s' % (len(path), str(path)))
    curr = start_state
    i = 1
    for a in path:
        curr = curr.result(a)
        print('After %d move%s: %s' % (i, ("", "s")[i>1], a))
        print(curr)

        input("Press return for the next state...")   # wait for key stroke
        i += 1
