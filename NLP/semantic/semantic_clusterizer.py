import networkx as nx
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class SemanticGraphClusterizer:
    def __init__(self, graph_data):
        self.graph_data = graph_data
        self.graph = nx.DiGraph()
        self.df = None

    def build_semantic_graph(self):
        for node in self.graph_data["nodes"]:
            self.graph.add_node(node["id"])

        for link in self.graph_data["links"]:
            source = link["source"]
            target = link["target"]
            self.graph.add_edge(source, target, type=link["type"], explanation=link["explanation"], weight=link["weight"])

    def choose_optimal_clusters(self, max_clusters=10):
        adjacency_matrix = nx.to_numpy_array(self.graph)
        distortions = []

        for num_clusters in range(1, max_clusters + 1):
            kmeans = KMeans(n_clusters=num_clusters, random_state=42)
            kmeans.fit(adjacency_matrix)
            distortions.append(kmeans.inertia_)

        # Plot the elbow method graph
        plt.plot(range(1, max_clusters + 1), distortions, marker='o')
        plt.title('Elbow Method')
        plt.xlabel('Number of Clusters')
        plt.ylabel('Distortion')
        plt.show()

    def clusterize_graph(self, num_clusters):
        adjacency_matrix = nx.to_numpy_array(self.graph)
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        labels = kmeans.fit_predict(adjacency_matrix)

        for i, node in enumerate(self.graph.nodes()):
            self.graph.nodes[node]["cluster"] = int(labels[i])

        self.df = pd.DataFrame({"Node": list(self.graph.nodes()), "Cluster": labels})
    
    def save_clusterized_graph_to_csv(self, filename="clustering_results.csv"):
        self.df.to_csv(filename, index=False)

    def visualize_clusterized_graph(self):
        pos = nx.spring_layout(self.graph)
        colors = [self.graph.nodes[node]["cluster"] for node in self.graph.nodes()]
        nx.draw(self.graph, pos, with_labels=True, font_weight='bold', node_size=700, node_color=colors, cmap=plt.cm.RdYlBu)
        plt.show()

if __name__ == "__main__":
    graph_data = {
        "directed": True,
        "multigraph": False,
        "graph": {},
        "nodes": [
            {"id": "процесс"},
            {"id": "Маркетинг"},
            {"id": "включает"}
        ],
        "links": [
            {"type": "nsubj", "explanation": "nominal subject", "weight": 0.5, "source": "Маркетинг", "target": "процесс"},
            {"type": "nsubj", "explanation": "nominal subject", "weight": 0.5, "source": "Маркетинг", "target": "включает"}
        ]
    }

    clusterizer = SemanticGraphClusterizer(graph_data)
    clusterizer.build_semantic_graph()
    clusterizer.choose_optimal_clusters(max_clusters=3)  # Choose a reasonable maximum number of clusters
    num_clusters = int(input("Enter the optimal number of clusters: "))
    clusterizer.clusterize_graph(num_clusters)
    clusterizer.visualize_clusterized_graph()
