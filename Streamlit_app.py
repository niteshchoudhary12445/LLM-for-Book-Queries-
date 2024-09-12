import streamlit as st
from Supervisor import Supervisor
from LLM_layer import LLMLayer
from langchain.schema import HumanMessage, AIMessage

st.title("📚 LLM for Book Queries ")

# Initialize conversation memory in session state if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize the LLMLayer for conversation history and load memory from session state
llm_conv_history = LLMLayer()
llm_conv_history.memory.chat_memory.messages = st.session_state.chat_history

# User input prompts
prompt = st.text_input(label="Enter the topic you want to ask:")
book_prompt = st.text_input(label="Enter the book-related query")

# Initialize Supervisor instances based on user input
supervisor_prompt = Supervisor(prompt=prompt) if prompt else None
supervisor_book = Supervisor(prompt=book_prompt) if book_prompt else None

def print_history(history):
    """Return conversation history as a list of formatted strings."""
    formatted_history = []
    for i, msg in enumerate(history):
        if i % 2 == 0:
            formatted_history.append(f"Human: {msg.content}")
        else:
            formatted_history.append(f"AI: {msg.content}")
    return formatted_history

# Button to generate response
if st.button(label="Search"):
    if supervisor_prompt or supervisor_book:
        if supervisor_prompt:
            generated_text = supervisor_prompt.generate_response()
            # Ensure generated_text is a string
            generated_text = str(generated_text)

            # Add the prompt and response to memory and session state
            human_message = HumanMessage(content=prompt)
            ai_message = AIMessage(content=generated_text)

            llm_conv_history.memory.chat_memory.add_message(human_message)
            llm_conv_history.memory.chat_memory.add_message(ai_message)

            # Store the updated memory back to session state
            st.session_state.chat_history = llm_conv_history.memory.chat_memory.messages

            st.write("Response for the topic query:")
            st.write(generated_text.strip())

        if supervisor_book:
            generated_text_1 = supervisor_book.generate_response_for_book()
            # Ensure generated_text_1 is a string
            generated_text_1 = str(generated_text_1['model_response'])

            # Add the book query and response to memory and session state
            human_message_book = HumanMessage(content=book_prompt)
            ai_message_book = AIMessage(content=generated_text_1)

            llm_conv_history.memory.chat_memory.add_message(human_message_book)
            llm_conv_history.memory.chat_memory.add_message(ai_message_book)

            # Store the updated memory back to session state
            st.session_state.chat_history = llm_conv_history.memory.chat_memory.messages

            st.write("Response for the book-related query:")
            st.write(generated_text_1)
                
    else:
        st.warning("Please enter a valid prompt or book-related query.")

# Show the conversation history in the sidebar
st.sidebar.title("Conversation History")
history = llm_conv_history.memory.chat_memory.messages
st.sidebar.write(print_history(history=history))
