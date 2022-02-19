##############################################################################################
# 0/1 Knapsack Problem
# Using the Best-First-Search (BFS) with Branch-and-Bound Algorithm to Solve it.
# -------------------------------------------------------------------------------
# Mark Barros
# CS3310 - Design and Analysis of Algorithms
# Cal Poly Pomona: Spring 2021
##############################################################################################


# These are the global variables used in this module. ----------------------------------------
BB_solution = None
BB_stack = []
BB_tree = []

# This is the structure used to represent a binary tree node. --------------------------------
class BTreeNode():
    def __init__(self):
        self.ParentNode = None
        self.Relaxation = 0
        self.Objective = 0
        self.ObjectID = -1
        self.Taken = None
        self.Room = None

    def __str__(self):
        return str(self.ObjectID) + "[" + str(self.Taken) + "]:" \
            + str(self.Objective) +  ", " + str(self.Room) + ", " + str(self.Relaxation)

# This solves the 0/1 Knapsack problem using the Branch and Bound method. --------------------
def BB_solver(capacity, weights, values):

    # This is an array for indicating whether an element has been taken or not.
    global BB_tree, BB_stack

    items = len(values)     # Get number of items
    taken = [0] * items     # Allocate memory for taken

    # This creates a list containing: (index, value/weight)
    value_per_weight = \
        [(elem[0][0], elem[0][1]/elem[1]) \
        for elem in zip(enumerate(values), weights)]

    # This sorts the list in descending order.
    value_per_weight.sort(key=lambda pair:pair[1], reverse=True)

    # This reorders the values and weights.
    weights = [weights[element[0]] for element in value_per_weight]
    values = [values[element[0]] for element in value_per_weight]

    # This creates a root node.
    Root = BTreeNode()
    Root.Room = capacity
    Root.Objective = 0
    Root.ObjectID = -1
    Root.Relaxation = getBound(items - 1, Root.ObjectID, Root.Room, Root.Objective, \
                      weights, values, value_per_weight)

    # This adds a root node to the tree.
    BB_tree.append(Root)
    BB_stack.append(Root)

    # This branches while the stack isn't empty.
    while BB_stack:
        Branch(items - 1, values, weights, value_per_weight)

    # This retraces which items were taken and which were ignored.
    Node = BB_solution

    while Node.ParentNode:
        taken[value_per_weight[Node.ObjectID][0]] = Node.Taken
        Node = Node.ParentNode

    return (BB_solution.Objective, taken)


# This handles all the branching logic and functionality. ------------------------------------
def Branch(items, values, weights, value_per_weight):

    global BB_solution, BB_tree, BB_stack

    if not BB_stack:
        return
    else:
        Root = BB_stack.pop()

    if BB_solution and Root.Relaxation < BB_solution.Objective:
        return
    elif Root.ObjectID == items:
        return

    Node = BTreeNode()
    Node.ObjectID = Root.ObjectID + 1
    Node.Room = Root.Room

    if Node.Room >= 0:
        Node.Objective = Root.Objective 
        Node.Taken = 0
        Node.Relaxation = \
            getBound(items, Node.ObjectID, Node.Room, \
            Node.Objective, weights, values, value_per_weight)
        Node.ParentNode = Root
        BB_stack.append(Node)

        if Node.Objective == Node.Relaxation:
            if BB_solution and Node.Objective > BB_solution.Objective:
                BB_solution = Node
            elif BB_solution is None:
                BB_solution = Node

    BB_tree.append(Node)

    Node = BTreeNode()
    Node.ObjectID = Root.ObjectID + 1
    Node.Room = Root.Room - weights[Node.ObjectID]
    
    if Node.Room >= 0:
        Node.Objective = Root.Objective + values[Node.ObjectID]
        Node.Taken = 1
        Node.Relaxation = \
            getBound(items, Node.ObjectID, Node.Room, \
            Node.Objective, weights, values, value_per_weight)
        Node.ParentNode = Root
        BB_stack.append(Node)

        if Node.Objective == Node.Relaxation:
            if BB_solution and Node.Objective > BB_solution.Objective:
                BB_solution = Node
            elif BB_solution is None:
                BB_solution = Node
    
    BB_tree.append(Node)

# This gets the bounds. ----------------------------------------------------------------------
def getBound(items, rootid, root_room, root_objective, weights, values, value_per_weight):
    while rootid < items and root_room - weights[rootid + 1] >= 0:
        root_objective = root_objective + values[rootid + 1]
        root_room = root_room - weights[rootid + 1]
        rootid = rootid + 1

    if rootid < items and root_room > 0:
        root_objective = root_objective + min(root_room, weights[rootid + 1]) \
                         * value_per_weight[rootid + 1][1]

    return root_objective


def solveIt(inputData):
    # This parses the first line's input.
    lines = inputData.split('\n')
    firstLine = lines[0].split()
    # The first value of the first line is the number of items.
    items = int(firstLine[0])
    # The second value of the first line is the Knapsack capacity.
    capacity = int(firstLine[1])

    # This is the output header.
    print("--------------------------------------------------------------------------")
    print("Solution to the 0/1 Knapsack problem using the Branch and Bound method")
    print("By Mark Barros")

    # This outputs the capacity of the napsack.
    print("--------------------------------------------------------------------------")
    print("Knapsack capacity: ", capacity)
    
    # This outputs the number of types of items there are.
    print("Number of types of items: ", items)

    # These are the lists for holding the values and weights.
    values = []
    weights = []

    # This places the input's values and weight in their respective lists.
    for i in range(1, items+1):
        # This parses the second line through the last lines' values.
        line = lines[i]
        parts = line.split()
        # This places the first value of each line in the values list.
        values.append(int(parts[0]))
        # This places the second value of each line in the weights list.
        weights.append(int(parts[1]))

    # This prints the respective values of the items in the list.
    print("Respective values of the items: ", *values[:])

    # This prints the respective weights of the items in the list.
    print("Respective weights of the items: ", *weights[:])

    # Branch and Bound is called.
    value, taken = BB_solver(capacity, weights, values)

    # The respective number of taken of each item:
    print("Respective number taken of each item: ", *taken)

    # This outputs the final profit.
    print("--------------------------------------------------------------------------")
    print("Final profit: ", value)

if __name__ == '__main__':
    
    # This opens the input file and accepts the input.
    inputDataFile = open("input.txt", 'r')
    inputData = ''.join(inputDataFile.readlines())
    inputDataFile.close()
    solveIt(inputData)
    print("--------------------------------------------------------------------------")

# End of Script. -----------------------------------------------------------------------------