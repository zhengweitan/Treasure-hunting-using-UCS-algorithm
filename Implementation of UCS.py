class Node:
    def __init__(self, state=None, parent=None, cost=0):
        self.state = state
        self.parent = parent
        self.children = []
        self.cost = cost

    def addChildren(self, children):
        self.children.extend(children)

def expandAndReturnChildren(state_space, node, obstacles):
    children = []
    for (m, n, c, effect, item) in state_space:
        if (m == node.state or n == node.state) and m not in obstacles and n not in obstacles:
            if m == node.state:
                cost = apply_effect(c, effect)
                children.append(Node(n, node.state, node.cost + cost))
            else:
                cost = apply_effect(c, effect)
                children.append(Node(m, node.state, node.cost + cost))
    return children

def apply_effect(cost, effect):
    if effect == '⊖':
        return cost * 2
    elif effect == '⊞':
        return cost / 2
    return cost

def print_world(solution, size, obstacles, traps, rewards, treasures):
    for step in solution:
        for i in range(size):
            for j in range(size):
                if (i, j) == step:
                    print("X", end=" ")
                elif (i, j) in obstacles:
                    print("O", end=" ")
                elif (i, j) in traps:
                    print("T", end=" ")
                elif (i, j) in rewards:
                    print("R", end=" ")
                elif (i, j) in treasures:
                    print("C", end=" ")
                else:
                    print("_", end=" ")
            print()
        print("\n")

def ucs(state_space, initial_state, goal_state, obstacles, size, traps, rewards, treasures):
    frontier = []
    explored = []
    found_goal = False
    goalie = Node()
    solution = []
    frontier.append(Node(initial_state, None))
    
    while not found_goal and frontier:
        if frontier[0].state == goal_state:
            found_goal = True
            goalie = frontier[0]
            break
        children = expandAndReturnChildren(state_space, frontier[0], obstacles)
        frontier[0].addChildren(children)
        explored.append(frontier[0])
        del frontier[0]
        for child in children:
            if not (child.state in [e.state for e in explored]):        
                frontier.append(child)
    
    if found_goal:
        solution = [goalie.state]
        path_cost = goalie.cost
        while goalie.parent is not None:
            solution.insert(0, goalie.parent)
            for e in explored:
                if e.state == goalie.parent:
                    goalie = e
                    break
        print_world(solution, size, obstacles, traps, rewards, treasures)
        return solution, path_cost
    else:
        return None, float('inf')

if __name__ == "__main__":
    # Define the state space with coordinates, traps, rewards, and obstacles
    state_space = [
        [(0, 0), (0, 1), 1, None, None], [(0, 1), (0, 2), 1, None, None], [(0, 2), (1, 2), 1, '⊖', None],
        [(1, 2), (1, 3), 1, None, None], [(1, 3), (2, 3), 1, '⊞', None], [(2, 3), (3, 3), 1, None, None],
        [(3, 3), (3, 2), 1, None, None], [(3, 2), (3, 1), 1, None, None], [(3, 1), (3, 0), 1, None, 'T']
    ]

    initial_state = (0, 0) #Entry
    goal_state = (2, 3)
    treasures = [(3, 0)]
    obstacles = [(2, 2), (3, 1)]
    traps = [(0, 2), (1, 3)]
    rewards = [(1, 3)]


    size = 4

    solution, cost = ucs(state_space, initial_state, goal_state, obstacles, size, traps, rewards, treasures)
    if solution:
        print("Solution:", solution)
        print("Path Cost:", cost)