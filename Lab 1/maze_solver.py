#!/usr/bin/env python3
from fringe import Fringe
from state import State


def heuristic(room, goal):
    """
    Returns heuristic value between a room and the goal room
    :param room: current room
    :param goal: goal room
    :return: int
    """

    room_coords = room.get_coords()
    goal_coords = goal.get_coords()
    return abs(room_coords[0] - goal_coords[0]) + abs(room_coords[1] - goal_coords[1])


def depth_limited(fr, visited, depth_limit):
    while not fr.is_empty() and depth_limit >= 0:
        cost, state = fr.pop()
        room = state.get_room()

        if room.is_goal():
            return state  # When the goal is reached, return the state

        visited.append(room)

        for d in room.get_connections():
            new_room, cost = room.make_move(d, state.get_cost())
            if new_room not in visited:
                new_state = State(new_room, state, cost)
                fr.push(new_state)
    
    return None  # No solution found


def ids(maze):
    """
    Performs iterative deepening search in a maze
    :param maze: maze which is used for IDS
    """

    depth = 0
    while True:
        fr = Fringe("STACK")
        room = maze.get_room(*maze.get_start())
        state = State(room, None)
        fr.push(state)
        visited = []
        
        solution = depth_limited(fr, visited, depth)
        if solution is not None:
            return solution
        depth += 1


def solve_maze_general(maze, algorithm):
    """
    Finds a path in a given maze with the given algorithm
    :param maze: The maze to solve
    :param algorithm: The desired algorithm to use
    :return: True if solution is found, False otherwise
    """
    # select the right fringe for each algorithm
    if algorithm == "BFS":
        fr = Fringe("FIFO")
    elif algorithm == "DFS":
        fr = Fringe("STACK")
    elif algorithm == "UCS" or "GREEDY" or "ASTAR":
        fr = Fringe("PRIORITY")
    else:
        print("Algorithm not found/implemented, exit")
        return

    # get the start room, create state with start room and None as parent and put it in fringe
    start_room = maze.get_room(*maze.get_start())

    if algorithm == "BFS" or "DFS" or "UCS":
        state = State(start_room, None)

    elif algorithm == "GREEDY" or "ASTAR":
        goal_room = maze.get_room(*maze.get_goal())
        start_priority = heuristic(start_room, goal_room)
        state = State(start_room, None, priority=start_priority)
    
    elif algorithm == "IDS":
        solution = ids(maze)
        if solution:
            print("solved")
            fr.print_stats()
            state.print_path()
            state.print_actions()
            print()  # print newline
            maze.print_maze_with_path(state)
            return True
        else:
            print("not solved")     # fringe is empty and goal is not found, so maze is not solved
            fr.print_stats()        # print the statistics of the fringe
            return False


    fr.push(state)
    visited = []

    while not fr.is_empty():

        # get item from fringe and get the room from that state
        cost, state = fr.pop()
        room = state.get_room()

        if room.is_goal():
            # if room is the goal, print that with the statistics and the path and return
            print("solved")
            fr.print_stats()
            state.print_path()
            state.print_actions()
            print()  # print newline
            maze.print_maze_with_path(state)
            return True

        visited.append(room)

        for d in room.get_connections():
            # loop through every possible move
            new_room, cost = room.make_move(d, state.get_cost())    # Get new room after move and cost to get there
            if new_room not in visited:
                new_state = State(new_room, state, cost)            # Create new state with new room and old room
                if algorithm == "UCS":
                    fr.push(new_state, cost)                        # Push state as a tuple (cost, state), which adds priority into the heapq
                elif algorithm == "GREEDY":
                    heuristic_cost = heuristic(new_room, goal_room)
                    new_state = State(new_room, state, state.get_cost() + cost, heuristic_cost)
                    fr.push(new_state)
                elif algorithm == "ASTAR":
                    total_cost = state.get_cost() + cost
                    new_priority = total_cost + heuristic(new_room, goal_room)
                    new_state = State(new_room, state, total_cost, new_priority)
                    fr.push(new_state)
                else:
                    fr.push(new_state)                              # push the new state


    print("not solved")     # fringe is empty and goal is not found, so maze is not solved
    fr.print_stats()        # print the statistics of the fringe
    return False


