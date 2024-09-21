import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from langchain.memory import ConversationBufferWindowMemory
from langchain.agents import AgentType, initialize_agent
from Tools import Tools

# Initialize Hugging Face authentication token if required
huggingface_api_token = os.getenv("HUGGINGFACE_API_KEY")

class LLMLayer:
    def __init__(self):
        """Initialize the Llama model, memory, and agent with tools."""
        # Initialize a memory buffer to store conversation context
        self.memory = ConversationBufferWindowMemory(memory_key="chat_history", return_messages=True, k=100)

        # Initialize Meta-Llama-3.1-8B-Instruct model and tokenizer from Hugging Face
        self.tokenizer = AutoTokenizer.from_pretrained(
            "meta-llama/Meta-Llama-3.1-8B-Instruct", use_auth_token=huggingface_api_token
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            "meta-llama/Meta-Llama-3.1-8B-Instruct",
            use_auth_token=huggingface_api_token,
            torch_dtype=torch.float16,  # Use float16 for efficiency
            device_map="auto"  # Automatically maps the model to GPU/CPU depending on the available hardware
        )

        # Initialize tools from the Tools class
        self.tools = Tools().create_tools()

        # Initialize the conversational agent using Llama
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
            input_ids = self.tokenizer.encode(query, return_tensors="pt").to(self.model.device)
            
            # Generate a response using the model
            output = self.model.generate(input_ids, max_length=1024, num_return_sequences=1)
            response = self.tokenizer.decode(output[0], skip_special_tokens=True)
            
            return response
        except Exception as e:
            return {"error": f"Failed to process query: {str(e)}"}

