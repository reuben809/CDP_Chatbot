import logging
from services.gemini_service import GeminiService
from data.storage.document_store import DocumentStore
from data.processors.text_processor import TextProcessor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class QueryHandler:
    def __init__(self):
        """Initialize the query handler"""
        self.gemini_service = GeminiService()
        self.document_store = DocumentStore()
        self.text_processor = TextProcessor()
        logger.info("Query handler initialized")

    def handle_query(self, query, cdp=None, query_type="How-to Question"):
        """
        Handle user query about CDPs

        Args:
            query (str): User query
            cdp (str, optional): Specific CDP to focus on
            query_type (str): Type of query (How-to, Comparison, Advanced)

        Returns:
            str: Response to the query
        """
        try:
            # Create a prompt based on query type
            prompt = self._create_prompt(query, cdp, query_type)

            # Find relevant documents
            relevant_docs = self._find_relevant_documents(query, cdp)

            # Create context from relevant documents
            context = self._create_context(relevant_docs, query)

            # Generate response
            response = self.gemini_service.generate_response(prompt, context)

            return response

        except Exception as e:
            logger.error(f"Error handling query: {str(e)}")
            return f"I'm sorry, I encountered an error while processing your question: {str(e)}"

    def _create_prompt(self, query, cdp, query_type):
        """Create a prompt based on the query type"""

        base_prompt = f"Answer the following question about "

        if cdp:
            base_prompt += f"the {cdp} CDP platform: {query}"
        else:
            base_prompt += f"CDP platforms: {query}"

        if query_type == "Cross-CDP Comparison":
            base_prompt += "\n\nCompare different CDP platforms, highlighting their similarities and differences."
        elif query_type == "Advanced Configuration":
            base_prompt += "\n\nProvide detailed technical information and step-by-step instructions."

        base_prompt += "\n\nFormat your answer in a clear, structured way. Include code examples where appropriate."

        return base_prompt

    def _find_relevant_documents(self, query, cdp=None, limit=5):
        """Find documents relevant to the query"""

        # Extract keywords to improve search
        keywords = self.text_processor.extract_keywords(query)

        # Search for each keyword
        all_results = []
        for keyword in keywords:
            results = self.document_store.search_documents(keyword, cdp)
            all_results.extend(results)

        # Deduplicate results
        seen_urls = set()
        unique_results = []

        for doc in all_results:
            url = doc.get("url", "")
            if url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(doc)

        # Return top results
        return unique_results[:limit]

    def _create_context(self, documents, query):
        """Create context from relevant documents"""

        if not documents:
            # If no documents found, return a general prompt
            if "segment" in query.lower():
                return self._get_mock_segment_context()
            elif "mparticle" in query.lower():
                return self._get_mock_mparticle_context()
            elif "lytics" in query.lower():
                return self._get_mock_lytics_context()
            elif "zeotap" in query.lower():
                return self._get_mock_zeotap_context()
            else:
                return ""

        context = "Relevant information:\n\n"

        for i, doc in enumerate(documents, 1):
            title = doc.get("title", "Untitled Document")
            content = doc.get("content", "")
            source = doc.get("source", "Unknown")

            # Summarize long content
            if len(content) > 1000:
                content = self.text_processor.summarize_text(content)

            context += f"Document {i} - {title} (Source: {source}):\n{content}\n\n"

        return context

    def _get_mock_segment_context(self):
        """Get mock context for Segment queries"""
        return """
        Segment is a Customer Data Platform (CDP) that allows you to collect, clean, and control customer data.
        It provides tools for data collection, identity resolution, audience building, and data activation.
        Key features include:
        - Website and app tracking
        - Server-side event collection
        - Data warehouse integration
        - Identity resolution
        - Audience building
        - Destination connections to hundreds of tools
        """

    def _get_mock_mparticle_context(self):
        """Get mock context for mParticle queries"""
        return """
        mParticle is a Customer Data Platform (CDP) focused on mobile and web data collection.
        It specializes in real-time data collection, identity management, and audience creation.
        Key features include:
        - SDK-based data collection
        - Server-side event tracking
        - Identity resolution and management
        - Audience building and segmentation
        - Machine learning-powered insights
        - Integration with hundreds of destinations
        """

    def _get_mock_lytics_context(self):
        """Get mock context for Lytics queries"""
        return """
        Lytics is a Customer Data Platform (CDP) focused on predictive analytics and personalization.
        It specializes in behavioral scoring, content affinity, and predictive recommendations.
        Key features include:
        - Data collection from multiple sources
        - Machine learning-based user scoring
        - Content and product affinity modeling
        - Predictive audience building
        - Real-time personalization
        - Integration with marketing and analytics tools
        """

    def _get_mock_zeotap_context(self):
        """Get mock context for Zeotap queries"""
        return """
        Zeotap is a Customer Data Platform (CDP) specializing in identity resolution and data enrichment.
        It focuses on connecting first-party data with third-party data sources for enhanced profiles.
        Key features include:
        - Unified customer view
        - Identity resolution across devices
        - Data enrichment with third-party sources
        - Predictive analytics and modeling
        - Audience segmentation and targeting
        - Privacy-compliant data management
        """