def GRAPH_SEARCH(start_node, is_goal, get_children):
    """
    GRAPH_SEARCH algorithm implementation.

    :param start_node: The initial node to start the search.
    :param is_goal: Function to check if a node is the goal.
    :param get_children: Function to get the children of a node.
    :return: Path to the goal node if found, else 'failed'.
    """
    frontier = [start_node]  # Initialize the frontier with the start node.
    expanded = set()         # Set to keep track of expanded nodes.
    path = {start_node: [start_node]}  # Dictionary to store paths.

    while frontier:
        # Remove the last node from the frontier (LIFO - stack behavior).
        node = frontier.pop()
        
        # Check if the current node is the goal.
        if is_goal(node):
            return path[node]  # Return the path to the goal node.
        
        # If the node has not been expanded, process it.
        if node not in expanded:
            expanded.add(node)  # Mark the node as expanded.
            
            # Iterate over the children of the current node.
            for child in get_children(node):
                if child not in expanded and child not in frontier:
                    frontier.append(child)  # Add the child to the frontier.
                    path[child] = path[node] + [child]  # Update the path.
    
    # If the loop completes without finding the goal, return 'failed'.
    return "failed"
