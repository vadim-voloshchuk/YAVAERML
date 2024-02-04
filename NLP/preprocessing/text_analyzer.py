from NLP.preprocessing.text_processor import TextPreprocessor

class TextAnalyzer:
    def __init__(self, preprocessor):
        """
        Constructor for initializing the TextAnalyzer with a TextPreprocessor instance.
        
        Args:
            preprocessor: TextPreprocessor - An instance of the TextPreprocessor class.
        """
        self.preprocessor = preprocessor

    def analyze_sentiment(self, text):
        """
        Analyze the sentiment of the input text after preprocessing.

        Args:
            text (str): The input text to analyze.

        Returns:
            str: The sentiment analysis result.
        """
        # Пример анализа настроения (просто для иллюстрации)
        processed_tokens = self.preprocessor.preprocess(text)
        positive_words = ["happy", "good", "positive"]
        negative_words = ["sad", "bad", "negative"]

        positive_count = sum(1 for token in processed_tokens if token in positive_words)
        negative_count = sum(1 for token in processed_tokens if token in negative_words)

        if positive_count > negative_count:
            return "Positive sentiment"
        elif negative_count > positive_count:
            return "Negative sentiment"
        else:
            return "Neutral sentiment"

if __name__ == "__main__":
    # Пример использования TextAnalyzer с TextPreprocessor
    text = "This is a very good and positive example for NLP preprocessing."
    
    # Создаем экземпляр TextPreprocessor
    preprocessor = TextPreprocessor()
    
    # Создаем экземпляр TextAnalyzer, передавая TextPreprocessor
    analyzer = TextAnalyzer(preprocessor)
    
    # Анализ настроения текста после предобработки
    sentiment_result = analyzer.analyze_sentiment(text)
    
    # Вывод результата
    print(sentiment_result)
