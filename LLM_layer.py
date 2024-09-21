from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.agents import AgentType, initialize_agent
from Tools import Tools
import os

google_llm = os.getenv("GOOGLE_API_KEY")

class LLMLayer:
    def __init__(self):
        """Initialize the LLM model, memory, and agent with tools."""
        # Initialize a memory buffer to store conversation context
        self.memory = ConversationBufferWindowMemory(memory_key="chat_history", return_messages=True, k=100)

        # Initialize the LLM model from Google (Gemini-1.5-flash)
        self.model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.5, api_key=google_llm)

        # Initialize tools from the Tools class
        self.tools = Tools().create_tools()

        # Initialize the conversational agent
        self.agent = initialize_agent(
            tools=self.tools,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            llm=self.model,
            memory=self.memory,
            verbose=True
        )

    def query_response(self, query: str, chat_history):
        """Process a query and return the LLM's response."""
        # Append new messages to memory
        self.memory.chat_memory.messages.extend(chat_history)
        
        try:
            # Process the query with the current memory context
            response = self.agent.run(query)
            return response
        except Exception as e:
            return {"error": f"Failed to process query: {str(e)}"}

