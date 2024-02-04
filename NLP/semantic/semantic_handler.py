from langchain.chat_models.gigachat import GigaChat
from langchain.schema import HumanMessage, SystemMessage
from NLP.semantic.semantic_builder import SemanticGraphBuilder

class SemanticGraphHandler:
    def __init__(self, semantic_data, credentials):
        self.builder = SemanticGraphBuilder(semantic_data)
        self.chat = GigaChat(credentials=credentials, verify_ssl_certs=False)

    def build_and_visualize_graph(self):
        self.builder.build_semantic_graph()
        self.builder.visualize_graph()

    def generate_answer(self, message):
        system_message = SystemMessage(content="Ты - модель, которая должна помочь превратить сырые данные семантическго графа в текст.")
        human_message = HumanMessage(content=message)
        messages = [system_message, human_message]
        response = self.chat(messages)
        return response.content
