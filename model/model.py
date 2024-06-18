import copy

import networkx as nx
from geopy.distance import distance
from database.DAO import DAO


class Model:
    def __init__(self):
        self.best_sol = None
        self.cities = DAO.get_all_cities()
        self.graph = None

    def build_graph(self, city):
        self.graph = nx.Graph()
        nodes = DAO.get_nodes(city)
        self.graph.add_nodes_from(nodes)
        for c1 in self.graph.nodes:
            for c2 in self.graph.nodes:
                if c1 != c2:
                    peso = distance((c1.latitude, c1.longitude), (c2.latitude, c2.longitude)).km
                    self.graph.add_edge(c1, c2, weight=peso)

    def get_graph_details(self):
        return len(self.graph.nodes), len(self.graph.edges)

    def get_farthest_node(self, business):
        farthest_node = None
        dist = 0
        for neighbor in self.graph.neighbors(business):
            distanza = distance((business.latitude, business.longitude), (neighbor.latitude, neighbor.longitude)).km
            if distanza > dist:
                dist = distanza
                farthest_node = neighbor
        return farthest_node, dist

    def get_percorso(self, b1, b2, soglia):
        self.best_sol = []
        parziale = [b1]
        self.ricorsione(parziale, b2, soglia)
        distanza_percorsa = self.get_distanza_percorsa(self.best_sol)
        return self.best_sol, distanza_percorsa

    def ricorsione(self, parziale, b2, soglia):
        if parziale[-1] == b2 and len(parziale) > len(self.best_sol):
            self.best_sol = copy.deepcopy(parziale)
            print(parziale)
        possibili = [n for n in self.graph.neighbors(parziale[-1]) if n.stars > soglia]
        for neighbor in possibili:
            if neighbor not in parziale:
                parziale.append(neighbor)
                self.ricorsione(parziale, b2, soglia)
                parziale.pop()
    
    def get_distanza_percorsa(self, nodes_list):
        d = 0
        for i in range(len(nodes_list)-1):
            d += distance((nodes_list[i].latitude, nodes_list[i].longitude), 
                          (nodes_list[i+1].latitude, nodes_list[i+1].longitude)).km
        return d
    