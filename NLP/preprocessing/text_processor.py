import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk import pos_tag
import re

class TextPreprocessor:
    def __init__(self):
        """
        Constructor for initializing the class with necessary NLTK downloads and setting up stop words, stemmer, and lemmatizer.
        """
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        self.stop_words = set(stopwords.words('russian'))
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()

    def tokenize(self, text):
        """
        Tokenize the input text using word_tokenize and return the tokens.
        """
        # Токенизация текста
        tokens = word_tokenize(text)
        return tokens

    def remove_stopwords(self, tokens):
        """
        Remove stopwords from the given list of tokens and return the filtered tokens.
        
        Parameters:
        - tokens: a list of tokens to remove stopwords from
        
        Returns:
        - filtered_tokens: a list of tokens with stopwords removed
        """
        # Удаление стоп-слов
        filtered_tokens = [token for token in tokens if token.lower() not in self.stop_words]
        return filtered_tokens

    def to_lowercase(self, tokens):
        """
        A function to convert the input tokens to lowercase.
        
        Args:
            self: The instance of the class.
            tokens: A list of tokens to be converted to lowercase.
        
        Returns:
            list: A list of tokens converted to lowercase.
        """
        # Приведение к нижнему регистру
        lowercase_tokens = [token.lower() for token in tokens]
        return lowercase_tokens

    def remove_punctuation(self, text):
        """
        Remove punctuation from the input text and return the cleaned text.

        Args:
            text (str): The input text from which punctuation will be removed.

        Returns:
            str: The cleaned text with punctuation removed.
        """
        # Удаление знаков пунктуации
        cleaned_text = re.sub(r'[^\w\s]', '', text)
        return cleaned_text

    def stem(self, tokens):
        """
        A function that performs stemming on a list of tokens.

        Args:
            self: The object instance.
            tokens: A list of tokens to be stemmed.

        Returns:
            List: A list of stemmed tokens.
        """
        # Стемминг токенов
        stemmed_tokens = [self.stemmer.stem(token) for token in tokens]
        return stemmed_tokens

    def lemmatize(self, tokens):
        """
        Lemmatizes the given tokens using the lemmatizer and returns the lemmatized tokens.

        :param tokens: list of tokens to be lemmatized
        :return: list of lemmatized tokens
        """
        # Лемматизация токенов
        lemmatized_tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        return lemmatized_tokens

    def pos_tagging(self, tokens):
        """
        Perform part-of-speech tagging on the input tokens.

        Args:
            tokens (list): A list of tokens to be tagged.

        Returns:
            list: A list of tuples where each tuple contains a token and its corresponding part-of-speech tag.
        """
        tagged_tokens = pos_tag(tokens)
        return tagged_tokens

    def preprocess(self, text):
        """
        A method to preprocess text by removing punctuation, tokenizing, removing stopwords, converting to lowercase, stemming, and lemmatizing. 
        Parameters:
            text: str - The input text to be preprocessed.
        Returns:
            list - The preprocessed tokens.
        """
        # Общий метод предобработки текста
        cleaned_text = self.remove_punctuation(text)
        tokens = self.tokenize(cleaned_text)
        tokens = self.remove_stopwords(tokens)
        tokens = self.to_lowercase(tokens)
        tokens = self.stem(tokens)
        tokens = self.lemmatize(tokens)
        return tokens

if __name__ == "__main__":
    # Пример использования при запуске скрипта напрямую
    text = "This is an example text for NLP preprocessing."
    preprocessor = TextPreprocessor()
    processed_tokens = preprocessor.preprocess(text)
    print(processed_tokens)
