import networkx as nx
import spacy
import matplotlib.pyplot as plt
import random

class SemanticGraph:
    def __init__(self):
        """
        Инициализация объекта семантического графа.
        """
        self.graph = nx.DiGraph()
        self.nlp = spacy.load("ru_core_news_sm")
        self.subgraph_nodes = set()
        self.subgraph_color_mapping = {}  # Словарь для отображения подграфов в цвета

    def add_node(self, node_name: str, subgraph: int = None):
        """
        Добавляет узел в граф.

        :param node_name: Название узла.
        :param subgraph: Идентификатор подграфа, к которому принадлежит узел (по умолчанию None).
        """
        self.graph.add_node(node_name, subgraph=subgraph)

    def add_edge(self, source_node: str, target_node: str, verb: str, weight: float = 1.0):
        """
        Добавляет дугу (ребро) между двумя узлами с указанными атрибутами.

        :param source_node: Начальный узел дуги.
        :param target_node: Конечный узел дуги.
        :param verb: Глагол, связанный с дугой.
        :param weight: Вес дуги (по умолчанию 1.0).
        """
        self.graph.add_edge(source_node, target_node, verb=verb, weight=weight)

    def shortest_path(self, source: str, target: str):
        """
        Вычисляет кратчайший путь между двумя узлами в графе.

        :param source: Начальный узел пути.
        :param target: Конечный узел пути.
        :return: Список узлов, образующих кратчайший путь.
        """
        return nx.shortest_path(self.graph, source=source, target=target)

    def analyze_sentence(self, sentence: str):
        """
        Анализирует предложение и извлекает субъекты, глаголы и объекты.

        :param sentence: Предложение для анализа.
        :return: Список субъектов, глаголов и объектов в предложении.
        """
        doc = self.nlp(sentence)
        subjects = []
        verbs = []
        objects = []

        for token in doc:
            if "nsubj" in token.dep_:
                subjects.append(token.text)
            if "ROOT" in token.dep_:
                verbs.append(token.lemma_)
            if "obj" in token.dep_:
                objects.append(token.text)

        return subjects, verbs, objects

    def create_graph_from_text(self, text: str):
        """
        Создает семантический граф из текста, разделяя его на предложения.

        :param text: Текст для создания графа.
        """
        sentences = text.split(".")
        subgraph_id = 0  # Идентификатор подграфа
        for sentence in sentences:
            subgraph_id += 1  # Увеличиваем идентификатор подграфа для нового предложения
            subjects, verbs, objects = self.analyze_sentence(sentence)
            for subject in subjects:
                if subject not in self.subgraph_nodes:
                    self.add_node(subject, subgraph=subgraph_id)
                    self.subgraph_nodes.add(subject)
                    self.subgraph_color_mapping[subgraph_id] = (random.random(), random.random(), random.random())  # Генерация случайного цвета
            for verb in verbs:
                for subject in subjects:
                    for obj in objects:
                        self.add_node(obj, subgraph=subgraph_id)
                        self.add_edge(subject, obj, verb)

    def visualize_graph(self):
        """
        Визуализирует семантический граф с разными цветами для узлов разных подграфов.
        """
        pos = nx.spring_layout(self.graph, seed=42)
        edge_labels = {(source, target): data["verb"] for source, target, data in self.graph.edges(data=True)}
        node_colors = [self.subgraph_color_mapping[self.graph.nodes[node]["subgraph"]] for node in self.graph.nodes()]

        nx.draw(self.graph, pos, with_labels=True, node_size=1000, font_size=10, node_color=node_colors)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_size=10)
        plt.show()

# Создание объекта семантического графа
semantic_graph = SemanticGraph()

# Анализ текста на русском языке и создание графа
text = """
В век технологического прогресса и информационного бума мы оказываемся в удивительном мире возможностей. 
Однако с развитием технологий возникают и новые вызовы. Кибербезопасность становится все более актуальной проблемой, требующей внимания и инновационных решений. В современном мире защита личной информации и киберпространства становится неотъемлемой частью нашей повседневной жизни. Это вызывает необходимость постоянного совершенствования методов обеспечения безопасности в цифровой эпохе.
Спорт, как важная часть культуры и общества, также претерпевает изменения под воздействием новых технологий. Виртуальные соревнования, киберспорт, и использование технологий в тренировочном процессе открывают новые возможности для спортсменов и болельщиков.
В заключение, наше общество находится на стыке двух эпох – традиционного и цифрового мира. Это время вызовов, но и огромных возможностей. Мы стоим на пороге новой эры, где технологии будут формировать нашу реальность и вносить вклад в каждый аспект нашей жизни. Важно сохранять баланс между развитием и сохранением ценностей, чтобы создать гармоничное общество для будущих поколений.
"""
semantic_graph.create_graph_from_text(text)

# Визуализация графа
semantic_graph.visualize_graph()
