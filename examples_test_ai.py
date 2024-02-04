from NLP.semantic.semantic_handler import SemanticGraphHandler
from NLP.preprocessing.text_parser import TextParser
from NLP.preprocessing.text_analyzer import TextAnalyzer
from NLP.preprocessing.text_processor import TextPreprocessor
from common.pereferences import GIGACHAT_API

text = "Моряк - это человек, который посвятил свою жизнь морским путешествиям и работе на кораблях. Он должен обладать рядом важных качеств: выносливостью, терпением, умением работать в команде, а также знаниями и опытом работы с морем и судами.Моряки проводят много времени на открытом море, поэтому они должны быть готовы к различным погодным условиям и возможным экстремальным ситуациям. Они также должны быть способны быстро реагировать и принимать решения в сложных и неожиданных обстоятельствах.В своей работе моряк выполняет множество задач: управляет судном, следит за его техническим состоянием, участвует в грузовых операциях, обеспечивает безопасность экипажа и пассажиров.Жизнь моряка - это не только работа, но и приключения. Он видит мир, путешествует по разным странам, сталкивается с новыми людьми и культурами. Но вместе с этим он часто сталкивается и с трудностями, испытаниями и рисками, связанными с морской профессией."
    
preprocessor = TextPreprocessor()
    
analyzer = TextAnalyzer(preprocessor)
    
parser = TextParser(preprocessor, analyzer)
    
subject_predicate_pairs = parser.extract_subject_predicate_pairs(text)

credentials = GIGACHAT_API
handler = SemanticGraphHandler(subject_predicate_pairs, credentials)
handler.build_and_visualize_graph()
response = handler.generate_answer("What is the meaning of life?")
print(response)
