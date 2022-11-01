import osmnx as ox
import heapq
import random
from haversine import haversine, Unit

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return not self.elements
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

class Graph():
    def __init__(self, graph):
        self.graph = graph
        # Default speeds in km/h in case the maxspeed property is missing
        self.defaults = {
            "motorway": 130,
            "trunk": 110,
            "primary": 90,
            "secondary": 80,
            "tertiary": 70,
            "unclassified": 50,
            "residential": 50,
            "motorway_link": 60,
            "trunk_link": 50,
            "primary_link": 40,
            "secondary_link": 40,
            "tertiary_link": 40,
            "living_street": 20,
            "service": 20,
            "pedestrian": 20,
            "track": 20,
            "road": 50
        }
    
    def heuristic(self, current, to_find):
        current_to_end = haversine((current['y'], current['x']),(to_find['y'], to_find['x']),unit=Unit.METERS)
        # make sure it is an underestimate
        # time at max speed
        return (current_to_end / self.to_ms(130))
    
    def get_speed(self, node):
        # Get the speed of the road of which a vertex is part of
        
        # Check if the maxspeed property exists
        if node.get("maxspeed"):
            road_speed = ""
            # if the road has more than 1 max speed, pick the first
            if isinstance(node["maxspeed"], list):
                road_speed = node["maxspeed"][0]
            else:
                road_speed = node["maxspeed"]
            return road_speed
        # check if the road type is specified
        elif node.get("highway"):
            road_type = ""
            # if the road has more than 1 road type, pick the first
            if isinstance(node["highway"], list):
                road_type = node["highway"][0]
            else:
                road_type = node["highway"]
            road_speed = self.defaults.get(road_type)
            return str(road_speed)
        # Otherwise return a default speed
        else:
            return str(50)
    
    def is_mph(self, speed):
        # Check if the speed is in mph (if part of the string says mph)
        try:
            int(speed)
            return False
        except:
            return True
    
    def to_ms(self, speed):
        # Convert the speed to m/s
        if self.is_mph(speed):
            converted = int(speed[:-4]) / 2.237
        else:
            converted = int(speed) / 3.6
        # Return the speed rounded to 2 decimal places
        return round(converted, 2)
        
    def astar(self, start, to_find):
        to_visit = PriorityQueue()
        to_visit.put(start, 0)
        from_v = {}
        cost_to_vertex= {}
        from_v[start] = None 
        cost_to_vertex[start] = 0
        vertices_explored = 0
        edges_explored = 0

        while not to_visit.empty():
            current = to_visit.get()
            vertices_explored += 1
            if current == to_find:
                path = []
                while current != start:
                    path.append(current)
                    current = from_v[current]
                path.append(start)
                path.reverse()
                return path, vertices_explored, edges_explored, cost_to_vertex[to_find]
            
            for neighbor in list(self.graph.neighbors(current)):
                # The weight of the nodes is the time to get there (distance/speed)
                speed = self.to_ms(self.get_speed(self.graph[current][neighbor][0]))
                distance = self.graph[current][neighbor][0]["length"]
                new_cost = cost_to_vertex[current] + distance/speed
                edges_explored += 1
                if neighbor not in cost_to_vertex or new_cost < cost_to_vertex[neighbor]:
                    cost_to_vertex[neighbor] = new_cost
                    priority = new_cost + self.heuristic(self.graph.nodes[neighbor], self.graph.nodes[to_find])
                    to_visit.put(neighbor, priority)
                    from_v[neighbor] = current
        return

ox.config(use_cache=True)

p1 = ox.geocode("Cupertino, CA")
p2 = ox.geocode("Mountain View, CA")

north, east, south, west = 0, 0, 0, 0
if p1[0] >= p2[0]:
    north, south = p1[0], p2[0]
else:
    north, south = p2[0], p1[0]
if p1[1] >= p2[1]:
    east, west = p1[1], p2[1]
else:
    east, west = p2[1], p1[1]

G = ox.graph_from_bbox(north + 0.01, south - 0.01, east + 0.01, west - 0.01, network_type="drive", simplify=True)

orig = ox.get_nearest_node(G, p1)
dest = ox.get_nearest_node(G, p2)

my_G = Graph(G)
path, vertices_explored, edges_explored, cost = my_G.astar(orig, dest)
print("A* (Time): Explored " + str(vertices_explored) + " vertices and " + str(edges_explored) + " edges. The destination is " + str(cost) + " seconds away")

fig, ax = ox.plot_graph_route(G, path, route_linewidth=2, node_size=0, route_color="#ff0000")