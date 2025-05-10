class Node:  # station
    def __init__(self, name):
        self.name = name
        self.neighbors = {}  # dict of neighbors and the edge between them


class Edge:
    def __init__(self, name, node1, node2, journey_time_min):
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.journey_time_min = journey_time_min


class Train:
    def __init__(self, name, capacity, start_node):
        self.name = name
        self.capacity = capacity
        self.current_node = start_node
        self.carrying = []


class Package:
    def __init__(self, name, weight, start_node, dest_node):
        self.name = name
        self.weight = weight
        self.current_node = start_node
        self.dest_node = dest_node
        self.delivered = False


class Move:
    def __init__(self, time, train_name, from_node, picked, to_node, dropped):
        self.time = time
        self.train_name = train_name
        self.from_node = from_node
        self.picked = picked
        self.to_node = to_node
        self.dropped = dropped

    def __repr__(self):
        return f"W={self.time}, T={self.train_name}, N1={self.from_node}, P1={self.picked}, N2={self.to_node}, P2={self.dropped}" 