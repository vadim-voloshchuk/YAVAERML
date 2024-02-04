import os
import json
import csv
from NLP.semantic.semantic_clusterizer import SemanticGraphClusterizer

def process_json_directory(input_directory, output_directory):
    for filename in os.listdir(input_directory):
        if filename.endswith(".json"):
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, os.path.splitext(filename)[0] + "_clustered.csv")
            
            with open(input_path, 'r', encoding='utf-8') as file:
                graph_data = json.load(file)

            clusterizer = SemanticGraphClusterizer(graph_data)
            clusterizer.build_semantic_graph()
            clusterizer.choose_optimal_clusters(max_clusters=3)  # You can adjust the maximum number of clusters
            num_clusters = int(input("Enter the optimal number of clusters: "))
            clusterizer.clusterize_graph(num_clusters)

            # Save clusterized graph to CSV
            clusterizer.save_clusterized_graph_to_csv(filename=output_path)

if __name__ == "__main__":
    input_directory = "NLP/examples/sgw_jsons"
    output_directory = "NLP/examples/clustered_csvs"

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    process_json_directory(input_directory, output_directory)
