import os
import google.generativeai as genai
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class GeminiService:
    def __init__(self):
        """Initialize the Gemini API client"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("GEMINI_API_KEY environment variable not set")
            raise ValueError("GEMINI_API_KEY environment variable not set")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        logger.info("Gemini service initialized")

    def generate_response(self, query, context=None, max_tokens=1024):
        """
        Generate a response using the Gemini API

        Args:
            query (str): The query text
            context (str, optional): Additional context to provide
            max_tokens (int, optional): Maximum output tokens

        Returns:
            str: The generated response
        """
        try:
            # Create prompt with context if provided
            prompt = query
            if context:
                prompt = f"Using the following information as context:\n\n{context}\n\n{query}"

            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "max_output_tokens": max_tokens,
                    "temperature": 0.2,
                    "top_p": 0.95,
                    "top_k": 40
                }
            )

            return response.text

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"I'm sorry, I couldn't process your request due to an error: {str(e)}"