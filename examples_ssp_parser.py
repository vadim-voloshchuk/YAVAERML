import os
from NLP.preprocessing.text_parser import TextParser
from NLP.preprocessing.text_analyzer import TextAnalyzer
from NLP.preprocessing.text_processor import TextPreprocessor

def process_directory(input_directory, output_directory):
    preprocessor = TextPreprocessor()
    analyzer = TextAnalyzer(preprocessor)
    parser = TextParser(preprocessor, analyzer)

    for filename in os.listdir(input_directory):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_directory, filename)
            output_filename = f"{os.path.splitext(filename)[0]}.json"
            output_path = os.path.join(output_directory, output_filename)
            
            with open(input_path, 'r', encoding='utf-8') as file:
                text = file.read()

            subject_predicate_pairs = parser.extract_subject_predicate_pairs(text)
            parser.pairs = subject_predicate_pairs

            parser.save_to_json(filename=output_path)

if __name__ == "__main__":
    input_directory = "NLP/examples/texts"
    output_directory = "NLP/examples/ssp_jsons"

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    process_directory(input_directory, output_directory)
