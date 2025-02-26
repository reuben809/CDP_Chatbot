import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TextProcessor:
    def __init__(self):
        """Initialize the text processor"""
        pass

    def clean_text(self, text):
        """
        Clean text by removing extra whitespace and normalizing

        Args:
            text (str): Input text

        Returns:
            str: Cleaned text
        """
        if not text:
            return ""

        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove special characters that aren't useful
        text = re.sub(r'[^\w\s.,;:?!()\[\]{}"\'`-]', '', text)

        return text.strip()

    def extract_keywords(self, text, max_keywords=10):
        """
        Extract keywords from text (simplified version)

        Args:
            text (str): Input text
            max_keywords (int): Maximum keywords to extract

        Returns:
            list: List of keywords
        """
        # This is a simple implementation - in a real app, you'd use NLP techniques
        text = self.clean_text(text.lower())

        # Remove common stop words
        stop_words = {"a", "an", "the", "and", "or", "but", "is", "are", "was", "were",
                      "be", "been", "being", "in", "on", "at", "to", "for", "with", "by", "about"}

        words = [word for word in text.split() if word not in stop_words and len(word) > 2]

        # Count word frequencies
        word_count = {}
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1

        # Sort by frequency
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

        # Return top keywords
        return [word for word, count in sorted_words[:max_keywords]]

    def summarize_text(self, text, max_sentences=3):
        """
        Create a simple summary of text by extracting key sentences

        Args:
            text (str): Input text
            max_sentences (int): Maximum sentences in summary

        Returns:
            str: Summary text
        """
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)

        if len(sentences) <= max_sentences:
            return text

        # Simple scoring - first and last sentences are important
        # Middle sentences with keywords are important
        keywords = set(self.extract_keywords(text))

        scored_sentences = []
        for i, sentence in enumerate(sentences):
            score = 0

            # First or last sentence
            if i == 0 or i == len(sentences) - 1:
                score += 3

            # Contains keywords
            for keyword in keywords:
                if keyword in sentence.lower():
                    score += 1

            # Longer sentences might have more information
            if len(sentence.split()) > 5:
                score += 1

            scored_sentences.append((score, sentence))

        # Sort by score and position
        scored_sentences.sort(reverse=True, key=lambda x: x[0])

        # Get top sentences and sort them by original position
        top_sentences = [sentence for score, sentence in scored_sentences[:max_sentences]]

        # Return summary
        return " ".join(top_sentences)