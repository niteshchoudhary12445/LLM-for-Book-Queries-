import streamlit as st
from Supervisor import Supervisor
from pdf_reader import document_loader
from LLM_layer import LLMLayer
from langchain.schema import HumanMessage, AIMessage

# Initialize the LLM layer for conversation history and responses
llm_conv_history = LLMLayer()

# Initialize session state for conversation history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def load_document(uploaded_file):
    """Load and process a document from a file."""
    try:
        document_content = document_loader(uploaded_file)
        if document_content:
            return document_content
        else:
            st.error("Error loading the document. Please upload a valid PDF file.")
            return ""
    except Exception as e:
        st.error(f"Failed to load document: {str(e)}")
        return ""

def handle_query(query_type, document_content=None):
    """Handle query based on selected query type."""
    if query_type == "Upload Document":
        user_query = st.text_input("Enter your query related to the document:")
        if user_query and document_content:
            return document_content + "\n" + user_query
    else:
        user_query = st.text_input("Enter your queries:")
        if user_query:
            return user_query
    return None

def display_response(response, user_query):
    """Display the response from the LLM and update conversation history."""
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    st.session_state.chat_history.append(AIMessage(content=response.strip()))
    st.write(response.strip())

def show_conversation_history():
    """Display the conversation history in the sidebar."""
    st.sidebar.title("Conversation History")
    if st.session_state.chat_history:
        history = st.session_state.chat_history
        for i in range(0, len(history), 2):
            if i < len(history) and history[i].content.strip():
                st.sidebar.write(f"**User**: {history[i].content}")
            if i + 1 < len(history) and history[i + 1].content.strip():
                st.sidebar.write(f"**AI**: {history[i + 1].content.strip()}")

def main():
    """Main function to run the Streamlit app."""
    st.title("📚 Interactive Document and Query-Based Assistant with LLM-Powered Responses")

    # Define query type options
    options = ['Student Query', 'Upload Document', 'Medical Research (PubMed)', 'Scientific Papers (Arxiv)']
    
    # Create the selection box for query type
    selected_query = st.selectbox("Select a query type:", options)
    
    document_content = ""
    if selected_query == "Upload Document":
        uploaded_file = st.file_uploader("Upload your PDF here:")
        if uploaded_file:
            document_content = load_document(uploaded_file)

    # Handle query input
    combined_input = handle_query(selected_query, document_content)

    # If query exists and the user clicks the search button
    if combined_input and st.button("Search"):
        with st.spinner("Processing your query..."):
            # Create the Supervisor instance with the combined input
            supervisor = Supervisor(prompt=combined_input, query_type=selected_query)

            # Generate the response using the LLM layer and internal memory
            response = llm_conv_history.query_response(combined_input, st.session_state.chat_history)

            # Display the response and update conversation history
            display_response(response, combined_input)

    # Display the conversation history in the sidebar
    show_conversation_history()

if __name__ == "__main__":
    main()

# Apply CSS styling to remove unnecessary blank spaces and adjust UI
st.markdown(
    """
    <style>
        .block-container {
            padding-bottom: 0px !important;
            padding-top: 0px !important;
            margin-bottom: 0px !important;
        }
        .sidebar .block-container {
            padding-top: 0px !important;
            padding-bottom: 0px !important;
            margin-bottom: 0px !important;
        }
        input[type=text] {
            margin-bottom: 0px !important;
            padding-bottom: 0px !important;
        }
        button[kind="primary"] {
            margin-bottom: 0px !important;
            padding-bottom: 0px !important;
        }
        .stText {
            margin-bottom: 0px !important;
            padding-bottom: 0px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)
