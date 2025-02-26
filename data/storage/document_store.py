import os
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DocumentStore:
    def __init__(self, data_dir="data/documents"):
        """
        Initialize the document store

        Args:
            data_dir (str): Directory to store documents
        """
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.documents = {}
        self._load_documents()

    def _load_documents(self):
        """Load documents from the data directory"""
        try:
            for cdp in ["segment", "mparticle", "lytics", "zeotap"]:
                file_path = os.path.join(self.data_dir, f"{cdp}_docs.json")
                if os.path.exists(file_path):
                    with open(file_path, "r") as f:
                        self.documents[cdp] = json.load(f)
                    logger.info(f"Loaded {len(self.documents[cdp])} documents for {cdp}")
                else:
                    self.documents[cdp] = []
        except Exception as e:
            logger.error(f"Error loading documents: {str(e)}")

    def save_documents(self, cdp, documents):
        """
        Save documents for a specific CDP

        Args:
            cdp (str): CDP name
            documents (list): List of document dictionaries
        """
        try:
            self.documents[cdp] = documents
            file_path = os.path.join(self.data_dir, f"{cdp}_docs.json")
            with open(file_path, "w") as f:
                json.dump(documents, f)
            logger.info(f"Saved {len(documents)} documents for {cdp}")
        except Exception as e:
            logger.error(f"Error saving documents: {str(e)}")

    def get_documents(self, cdp=None):
        """
        Get documents for a specific CDP or all documents

        Args:
            cdp (str, optional): CDP name

        Returns:
            list: List of document dictionaries
        """
        if cdp:
            return self.documents.get(cdp, [])
        else:
            # Combine all documents
            all_docs = []
            for docs in self.documents.values():
                all_docs.extend(docs)
            return all_docs

    def search_documents(self, query, cdp=None, limit=10):
        """
        Search documents for a query (simple keyword search)

        Args:
            query (str): Search query
            cdp (str, optional): CDP name to limit search
            limit (int, optional): Maximum results to return

        Returns:
            list: List of matching document dictionaries
        """
        query = query.lower()
        results = []

        docs = self.get_documents(cdp)

        for doc in docs:
            score = 0
            # Check title
            if query in doc.get("title", "").lower():
                score += 3
            # Check content
            if query in doc.get("content", "").lower():
                score += 1

            if score > 0:
                results.append((score, doc))

        # Sort by score and return top results
        results.sort(reverse=True, key=lambda x: x[0])
        return [doc for score, doc in results[:limit]]