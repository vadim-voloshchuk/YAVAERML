import json
import spacy
from NLP.preprocessing.text_analyzer import TextAnalyzer
from NLP.preprocessing.text_processor import TextPreprocessor

class TextParser:
    def __init__(self, preprocessor, analyzer):
        self.preprocessor = preprocessor
        self.analyzer = analyzer
        self.pairs = []

    def extract_subject_predicate_pairs(self, text):
        # Если удалить пунктуацию, то логика зависимостей в предложениях изменится
        # processed_text = self.preprocessor.remove_punctuation(text)
        
        # Загрузка модели spaCy для русского языка
        nlp = spacy.load("ru_core_news_sm")
        
        # Обработка текста с использованием spaCy
        doc = nlp(text)
        
        # Извлечение пар подлежащее-сказуемое
        subject_predicate_pairs = []
        for sent in doc.sents:
            for token in sent:
                if 'ROOT' in token.dep_:
                    print(token)
                    current_subject = token.text
                    current_predicate = None
                    for child in token.children:
                        if 'nsubj' in child.dep_:
                            current_predicate = child.text
                            # Добавляем тип зависимости и его объяснение
                            dep_type = child.dep_
                            dep_explanation = spacy.explain(dep_type)
                            subject_predicate_pairs.append({
                                'subject': current_subject,
                                'predicate': current_predicate,
                                'dependency_type': dep_type,
                                'dependency_explanation': dep_explanation
                            })
                            break
                
        return subject_predicate_pairs

    def save_to_json(self, filename='subject_predicate_pairs.json'):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.pairs, file,ensure_ascii=False, indent=2)
        print(f'Subject-Predicate pairs saved to {filename}')

if __name__ == "__main__":
    text = "Моряк - это человек, который посвятил свою жизнь морским путешествиям и работе на кораблях. Он должен обладать рядом важных качеств: выносливостью, терпением, умением работать в команде, а также знаниями и опытом работы с морем и судами.Моряки проводят много времени на открытом море, поэтому они должны быть готовы к различным погодным условиям и возможным экстремальным ситуациям. Они также должны быть способны быстро реагировать и принимать решения в сложных и неожиданных обстоятельствах.В своей работе моряк выполняет множество задач: управляет судном, следит за его техническим состоянием, участвует в грузовых операциях, обеспечивает безопасность экипажа и пассажиров.Жизнь моряка - это не только работа, но и приключения. Он видит мир, путешествует по разным странам, сталкивается с новыми людьми и культурами. Но вместе с этим он часто сталкивается и с трудностями, испытаниями и рисками, связанными с морской профессией."
    
    # Создаем экземпляр TextPreprocessor
    preprocessor = TextPreprocessor()
    
    # Создаем экземпляр TextAnalyzer, передавая TextPreprocessor
    analyzer = TextAnalyzer(preprocessor)
    
    # Создаем экземпляр TextParser, передавая TextPreprocessor и TextAnalyzer
    parser = TextParser(preprocessor, analyzer)
    
    # Извлекаем пары подлежащее-сказуемое
    subject_predicate_pairs = parser.extract_subject_predicate_pairs(text)
    parser.pairs = subject_predicate_pairs
    
    # Сохраняем пары в JSON
    parser.save_to_json()
