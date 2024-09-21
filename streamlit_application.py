import streamlit as st
from Supervisor import Supervisor
from pdf_reader import document_loader
from LLM_layer import LLMLayer
from langchain.schema import HumanMessage, AIMessage

def load_document(uploaded_file):
    """Load and process a document from a file."""
    document_content = document_loader(uploaded_file)
    if document_content:
        return document_content
    else:
        st.error("Error loading the document. Please upload a valid PDF file.")
        return ""

# Initialize the LLM layer for conversation history and responses
llm_conv_history = LLMLayer()

# Initialize session state for conversation history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.title("📚 Interactive Document and Query-Based Assistant with LLM-Powered Responses")

# Define query type options
options = ['Student Query', 'Upload Document', 'Medical Research (PubMed)', 'Scientific Papers (Arxiv)']

# Create the selection box for query type
selected_query = st.selectbox("Select a query type:", options)

combined_input = ""

if selected_query == "Upload Document":
    # For document-based queries
    uploaded_file = st.file_uploader("Upload your PDF here:")
    if uploaded_file:
        # Load the document content
        document_content = load_document(uploaded_file)
        user_query = st.text_input("Enter your query related to the document:")
        if user_query and document_content:
            # Combine the document content and user's query
            combined_input = document_content + "\n" + user_query
else:
    # For other query types (non-document)
    user_query = st.text_input("Enter your queries:")
    if user_query:
        combined_input = user_query

if combined_input and st.button("Search"):
    # Create the Supervisor instance with the combined input
    supervisor = Supervisor(prompt=combined_input, query_type=selected_query)

    # Generate the response using the LLM layer and internal memory
    response = llm_conv_history.query_response(combined_input, st.session_state.chat_history)

    st.session_state.chat_history.append(HumanMessage(content=user_query))
    st.session_state.chat_history.append(AIMessage(content=response.strip()))

    # Display the response
    st.write(response.strip())

# Display the conversation history in the sidebar
st.sidebar.title("Conversation History")

if st.session_state.chat_history:
    history = st.session_state.chat_history

    for i in range(0, len(history), 2):
        if i < len(history) and history[i].content.strip():
            st.sidebar.write(f"**User**: {history[i].content}")
        if i + 1 < len(history) and history[i + 1].content.strip():
            st.sidebar.write(f"**AI**: {history[i + 1].content.strip()}")

# Apply CSS styling to remove unnecessary blank spaces and adjust UI
st.markdown(
    """
    <style>
        /* Remove extra space from the main content */
        .block-container {
            padding-bottom: 0px !important;
            padding-top: 0px !important;
            margin-bottom: 0px !important;
        }
        /* Remove extra padding from the sidebar */
        .sidebar .block-container {
            padding-top: 0px !important;
            padding-bottom: 0px !important;
            margin-bottom: 0px !important;
        }
        /* Ensure text input fields have no margin or padding */
        input[type=text] {
            margin-bottom: 0px !important;
            padding-bottom: 0px !important;
        }
        /* Ensure buttons have no extra margin or padding */
        button[kind="primary"] {
            margin-bottom: 0px !important;
            padding-bottom: 0px !important;
        }
        /* Customize the chat message style to prevent space between them */
        .stText {
            margin-bottom: 0px !important;
            padding-bottom: 0px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)
