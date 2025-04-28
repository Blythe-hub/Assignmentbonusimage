from heap import BinaryHeap

def max_probability(n, edges, succ_prob, start, end):
    """
    Find the path with the maximum probability of success from start to end.
    
    Args:
        n: Number of vertices in the graph (0-indexed)
        edges: List of edges, where edges[i] = [a, b] represents an edge between a and b
        succ_prob: List of probabilities, where succ_prob[i] is the probability of success for edges[i]
        start: Starting vertex
        end: Ending vertex
        
    Returns:
        The maximum probability of success to go from start to end
    """
    # If start and end are the same, return 1.0 (100% probability)
    if start == end:
        return 1.0
    
    # Build the adjacency list representation of the graph
    graph = [[] for _ in range(n)]
    for i, (a, b) in enumerate(edges):
        # Undirected edge from a to b
        graph[a].append((b, succ_prob[i]))
        # Undirected edge from b to a
        graph[b].append((a, succ_prob[i]))
    
    # Create a max heap for Dijkstra's algorithm
    # Since we're using a min heap, we'll negate the probabilities to simulate a max heap
    heap = BinaryHeap()
    
    # Probability to reach each vertex from the start
    # Initialize with 0 probability for all vertices except start
    probs = [0.0] * n
    probs[start] = 1.0
    
    # Visited set to keep track of processed vertices
    visited = set()
    
    # Add the start vertex to the heap with probability 1.0
    # We negate the probability since we're using a min heap but want max probability
    heap.insert((-1.0, start))
    
    while not heap.is_empty():
        # Get vertex with the highest probability so far
        neg_prob, vertex = heap.delete()
        prob = -neg_prob  # Convert back to actual probability
        
        # If we've reached the end vertex, return the probability
        if vertex == end:
            return prob
        
        # Skip if we've already processed this vertex
        if vertex in visited:
            continue
        
        # Mark vertex as visited
        visited.add(vertex)
        
        # Process all neighbors of the current vertex
        for neighbor, edge_prob in graph[vertex]:
            # If the neighbor has already been processed, skip
            if neighbor in visited:
                continue
            
            # Calculate new probability to reach the neighbor
            new_prob = prob * edge_prob
            
            # If we found a better path, update the probability
            if new_prob > probs[neighbor]:
                probs[neighbor] = new_prob
                # Add to heap with negated probability (for max heap behavior)
                heap.insert((-new_prob, neighbor))
    
    # If we've explored all reachable vertices and haven't found end, return 0
    return 0.0
