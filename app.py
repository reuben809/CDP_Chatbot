import streamlit as st
from services.query_handler import QueryHandler
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the query handler
query_handler = QueryHandler()

# Set up Streamlit page config
st.set_page_config(
    page_title="CDP Support Agent",
    page_icon="🤖",
    layout="wide"
)

# App title and description
st.title("CDP Support Agent 🤖")
st.markdown("""
This support agent can answer how-to questions about Customer Data Platforms (CDPs):
- Segment
- mParticle
- Lytics
- Zeotap
""")

# Sidebar for CDP selection
st.sidebar.title("Settings")
cdp_options = ["All CDPs", "Segment", "mParticle", "Lytics", "Zeotap"]
selected_cdp = st.sidebar.selectbox("Focus on specific CDP:", cdp_options)

# Query type selection
query_type = st.sidebar.radio(
    "Query Type:",
    ["How-to Question", "Cross-CDP Comparison", "Advanced Configuration"]
)

# Information about query types
with st.sidebar.expander("Query Type Information"):
    st.markdown("""
    **How-to Question**: Basic instructions for using CDP features.
    
    **Cross-CDP Comparison**: Compare functionality between different CDPs.
    
    **Advanced Configuration**: Complex setup and integration questions.
    """)

# Example questions based on query type
example_questions = {
    "How-to Question": [
        "How do I set up a new source in Segment?",
        "How can I create a user profile in mParticle?",
        "How do I build an audience segment in Lytics?",
        "How can I integrate my data with Zeotap?"
    ],
    "Cross-CDP Comparison": [
        "How does Segment's audience creation process compare to Lytics'?",
        "What are the differences between mParticle and Zeotap data collection?",
        "Compare user identification methods across all CDPs",
        "Which CDP has better data export capabilities?"
    ],
    "Advanced Configuration": [
        "How to implement server-side tracking in Segment?",
        "Advanced custom attribute mapping in mParticle?",
        "Setting up real-time personalization with Lytics?",
        "Configure multi-channel identity resolution in Zeotap?"
    ]
}

# Display example questions
st.sidebar.markdown("### Example Questions")
for q in example_questions[query_type]:
    if st.sidebar.button(q, key=q):
        st.session_state.user_query = q

# Initialize chat history if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if "user_query" not in st.session_state:
    st.session_state.user_query = ""

user_query = st.chat_input("Ask a question about CDP platforms...")
if not user_query and st.session_state.user_query:
    user_query = st.session_state.user_query
    st.session_state.user_query = ""

if user_query:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_query)
    
    # Get response from query handler
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = query_handler.handle_query(
                user_query, 
                selected_cdp if selected_cdp != "All CDPs" else None,
                query_type
            )
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.markdown("Built with Streamlit and Gemini AI")
