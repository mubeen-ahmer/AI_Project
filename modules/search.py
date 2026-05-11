from collections import deque   # for BFS queue
import heapq                     # for UCS and A* priority queue
from data.city_graph import UNWEIGHTED_CITY_GRAPH, WEIGHTED_CITY_GRAPH
HEURISTIC = {
    "Police_HQ"            : 10,
    "Traffic_Control_Center": 9,
    "North_Station"         : 7,
    "River_Bridge"          : 8,
    "Stadium"               : 5,
    "Airport_Road"          : 6,
    "South_Residential"     : 3,
    "City_Hospital"         : 0,
    "East_Market"           : 2,
    "Central_Junction"      : 4,
    "West_Terminal"         : 6,
    "Fire_Station"          : 7,
    "Industrial_Zone"       : 8,
}

def bfs(start, destination):
    queue = deque()
    visited = set()
    queue.append([start])
    visited.add(start)

    while queue:
        path = queue.popleft()
        current = path[-1]

        if current == destination:
            return path, len(path) - 1  # path and number of hops

        for neighbor in UNWEIGHTED_CITY_GRAPH[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    return None, -1

def ucs(start, destination):
    """
    Uniform Cost Search on weighted graph.
    Expands lowest cost node first.
    Returns (path, total_cost) or (None, -1) if no path found.
    """
    heap = []
    heapq.heappush(heap, (0, [start]))  # (cost, path)
    visited = set()

    while heap:
        cost, path = heapq.heappop(heap)
        current = path[-1]

        if current in visited:
            continue
        visited.add(current)

        if current == destination:
            return path, cost

        for neighbor, weight in WEIGHTED_CITY_GRAPH[current].items():
            if neighbor not in visited:
                heapq.heappush(heap, (cost + weight, path + [neighbor]))

    return None, -1

def astar(start, destination):
    """
    A* Search on weighted graph using manual heuristic table.
    Priority = actual cost + heuristic estimate to destination.
    Returns (path, total_cost) or (None, -1) if no path found.
    """
    heap = []
    heapq.heappush(heap, (HEURISTIC[start], 0, [start]))  # (priority, cost, path)
    visited = set()

    while heap:
        priority, cost, path = heapq.heappop(heap)
        current = path[-1]

        if current in visited:
            continue
        visited.add(current)

        if current == destination:
            return path, cost

        for neighbor, weight in WEIGHTED_CITY_GRAPH[current].items():
            if neighbor not in visited:
                new_cost     = cost + weight
                new_priority = new_cost + HEURISTIC[neighbor]
                heapq.heappush(heap, (new_priority, new_cost, path + [neighbor]))

    return None, -1

def find_route(start, destination, algorithm="bfs"):
    """
    Master search function. Selects algorithm based on parameter.
    Returns (path, cost).
    """
    print(f"[Search] Running {algorithm.upper()} from {start} to {destination}")
    
    if algorithm == "bfs":
        return bfs(start, destination)
    elif algorithm == "ucs":
        return ucs(start, destination)
    elif algorithm == "astar":
        return astar(start, destination)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")