import os
import json
from NLP.semantic.semantic_builder import SemanticGraphBuilder

def process_json_directory(input_directory, output_directory):
    for filename in os.listdir(input_directory):
        if filename.endswith(".json"):
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, filename)
            
            with open(input_path, 'r', encoding='utf-8') as file:
                semantic_data = json.load(file)

            graph_builder = SemanticGraphBuilder(semantic_data)
            graph_builder.build_semantic_graph()
            graph_builder.weight_graph_edges()  # Возможно, вы захотите взвесить ребра

            # Сохраняем взвешенный граф в JSON
            graph_builder.save_graph_to_json(filename=output_path)

if __name__ == "__main__":
    input_directory = "NLP/examples/ssp_jsons"
    output_directory = "NLP/examples/sgw_jsons"

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    process_json_directory(input_directory, output_directory)
