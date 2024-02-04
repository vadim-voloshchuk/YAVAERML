import networkx as nx
import matplotlib.pyplot as plt
import json

class SemanticGraphBuilder:
    def __init__(self, semantic_data):
        self.semantic_data = semantic_data
        self.graph = nx.DiGraph()

    def build_semantic_graph(self):
        for relation in self.semantic_data:
            subject = relation["subject"]
            predicate = relation["predicate"]
            dependency_type = relation["dependency_type"]
            dependency_explanation = relation["dependency_explanation"]

            # Add nodes and edges to the graph
            self.graph.add_node(subject)
            self.graph.add_node(predicate)
            self.graph.add_edge(predicate, subject, type=dependency_type, explanation=dependency_explanation)

    def visualize_graph(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8, connectionstyle='arc3,rad=0.1')
        edge_labels = nx.get_edge_attributes(self.graph, 'type')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
        plt.show()

    def save_graph_to_json(self, filename='semantic_graph.json'):
        graph_data = nx.node_link_data(self.graph)
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(graph_data, file, ensure_ascii=False, indent=2)
        print(f'Semantic graph saved to {filename}')
    
    def weight_graph_edges(self):
        edge_type_count = {}
        
        for edge in self.graph.edges(data=True):
            dependency_type = edge[2]['type']
            edge_type_count[dependency_type] = edge_type_count.get(dependency_type, 0) + 1

        for edge in self.graph.edges(data=True):
            dependency_type = edge[2]['type']
            edge[2]['weight'] = 1.0 / edge_type_count[dependency_type]


if __name__ == "__main__":
    semantic_data = [
        {"subject": "человек", "predicate": "работает", "dependency_type": "nsubj", "dependency_explanation": "nominal subject"},
        {"subject": "должен", "predicate": "Он", "dependency_type": "nsubj", "dependency_explanation": "nominal subject"},
        {"subject": "работает", "predicate": "Он", "dependency_type": "nsubj", "dependency_explanation": "nominal subject"},
    ]

    graph_builder = SemanticGraphBuilder(semantic_data)
    graph_builder.build_semantic_graph()
    graph_builder.weight_graph_edges()
    graph_builder.visualize_graph()
    graph_builder.save_graph_to_json()
