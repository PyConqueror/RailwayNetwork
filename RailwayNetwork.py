from models import Node, Edge, Train, Package, Move


class RailwayNetwork:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.trains = []
        self.packages = []
        self.moves = []

    def add_node(self, name):
        if name not in self.nodes: #if the node is not in the nodes list, add it
            self.nodes[name] = Node(name)

    def add_edge(self, edge_name, n1, n2, time_min):
        self.add_node(n1)
        self.add_node(n2)
        edge = Edge(edge_name, n1, n2, time_min)
        self.edges.append(edge)
        self.nodes[n1].neighbors[n2] = edge
        self.nodes[n2].neighbors[n1] = edge

    def add_train(self, name, capacity, start_node):
        self.trains.append(Train(name, capacity, start_node))


    def add_package(self, name, weight, start, dest):
        self.packages.append(Package(name, weight, start, dest))

    def find_edge(self, n1, n2):
        return self.nodes[n1].neighbors.get(n2)
    
    def find_path(self, start, end, path=None, visited=None):
        if path is None:
            path = [start]
        if visited is None:
            visited = set()

        if start == end:
            return path

        visited.add(start)

        for neighbor in self.nodes[start].neighbors:
            if neighbor not in visited:
                new_path = self.find_path(neighbor, end, path + [neighbor], visited.copy())
                if new_path:
                    return new_path

        return None    
        
    def simulate(self):
        time = 0

        for pkg in self.packages:
            for train in self.trains:
                if pkg.weight > train.capacity:
                    continue

                path_to_pkg = self.find_path(train.current_node, pkg.current_node)
                path_to_dest = self.find_path(pkg.current_node, pkg.dest_node)

                if not path_to_pkg or not path_to_dest:
                    continue  # no path found

                # move train to package
                for next_node in path_to_pkg[1:]:  # skip current_node
                    edge = self.find_edge(train.current_node, next_node)
                    travel_time = edge.journey_time_min
                    self.moves.append(Move(time, train.name, train.current_node, [], next_node, []))
                    time += travel_time
                    train.current_node = next_node

                # pick up package
                train.carrying.append(pkg)
                pkg.current_node = train.current_node

                # move train to destination
                for next_node in path_to_dest[1:]:
                    edge = self.find_edge(train.current_node, next_node)
                    travel_time = edge.journey_time_min
                    self.moves.append(Move(time, train.name, train.current_node, [pkg.name], next_node, []))
                    time += travel_time
                    train.current_node = next_node

                # drop off package
                self.moves.append(Move(time, train.name, train.current_node, [], train.current_node, [pkg.name]))
                pkg.delivered = True
                break  # stop after assigning one train per package


        #todo:
        #1. find the suitable train for the package
        #2. find the path for the train to pick up the package
        #3. find the path for the train to drop off the package
        #4. add the move to the moves list
        #5. update the train's current station
        #6. update the package's current station
        #7. update the package's delivered status

    def print_moves(self):
        for move in self.moves:
            print(move)


test_network = RailwayNetwork()

test_network.add_edge("E1", "A", "B", 30)
test_network.add_edge("E2", "B", "C", 10)
test_network.add_package("K1", 5, "A", "C")
test_network.add_train("Q1", 5, "B")

test_network.simulate()
test_network.print_moves()

#print(test_network.edges)
#print(test_network.trains)
#print(test_network.packages)


