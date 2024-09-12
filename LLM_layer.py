from langchain_community.utilities import SerpAPIWrapper
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import HumanMessage
from langchain.chains import ConversationChain
from Search_read import request_parse
import os

serp_api_key = os.getenv("SERPAPI_API_KEY")
google_llm_api = os.getenv("GOOGLE_API_KEY")

class LLMLayer:
    
    def __init__(self):
        # Initialize a memory buffer to store conversation context
        self.memory = ConversationBufferWindowMemory()
        
        # Initialize SerpAPIWrapper to handle search queries
        self.search = SerpAPIWrapper(serpapi_api_key=serp_api_key)
        
        # Initialize the LLM model from Google (Gemini-1.5-flash)
        self.model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.5,api_key=google_llm_api)
        
        # Set up the conversation chain that uses the model and memory for storing ongoing conversation
        self.conversation_chain = ConversationChain(llm=self.model, verbose=True, memory=self.memory)

    def extract_response_content(self, response):
        """Extract content from the LLM's response object."""
        if isinstance(response, list):
            # If the response is a list, return the first item
            return response[0].content
        return response.content if hasattr(response, 'content') else str(response)

    def student_query_chain(self, prompt):
        """
        Handles student queries by first searching for relevant information 
        and then passing the combined query and search result to the LLM.
        """
        try:
            search_input = ""
            if isinstance(prompt, list):
                # Extract the content from HumanMessage in the list prompt
                for message in prompt:
                    if isinstance(message, HumanMessage):
                        search_input = message.content
            
            # Use SerpAPI to search for the input query
            search_result = self.search.run(search_input)
            
            # Combine search results and the prompt for LLM input
            combined_input = f"{search_result}\n{prompt}"
            
            # Get response from the LLM model
            response = self.model.invoke(combined_input)  
            
            # Extract and return the response content
            response_content = self.extract_response_content(response)
            return {"model_response": response_content}
        
        except Exception as e:
            return {"error": f"Error in student query: {str(e)}"}

    def book_recommender_chain(self, prompt):
        """
        Recommends books, papers, or articles based on the prompt. 
        It first searches for relevant sources and then feeds the results into the LLM.
        """
        try:
            # Search for books, papers, or articles related to the prompt
            search_result = self.search.run(f"{prompt} books, papers, or articles")
            
            # Combine search results with the prompt and pass it to the LLM
            combined_input = f"{search_result}\n{prompt}"
            response = self.model.invoke(combined_input) 
            
            # Extract and return the response content
            response_content = self.extract_response_content(response)
            return {"model_response": response_content}
        
        except Exception as e:
            return {"error": f"Error in book recommendation: {str(e)}"}

    def doc_reader(self, book_name):
        """
        Reads and extracts information from a document by searching for the document's PDF or related content.
        """
        try:
            # Search for the book using SerpAPI
            search_result = self.search.run(book_name)
            
            # Parse the content of the book using request_parse function
            parser = request_parse(book_name)
            
            # Combine parsed content and search result, then pass it to the LLM
            combined_input = f"{parser}\n{search_result}\n{book_name}"

            response = self.model.invoke(combined_input)  
            
            # Extract and return the response content
            response_content = self.extract_response_content(response)
            return {"model_response": response_content}
        
        except Exception as e:
            return {"error": f"Error in finding PDF link: {str(e)}"}

    def arrange_response_in_sequence(self, response):
        """
        Arranges responses in a conversational sequence using the conversation chain.
        """
        try:
            # Run the response through the conversation chain to arrange it properly
            seq_response = self.conversation_chain.run(response)  
            
            # Extract and return the sequential response content
            seq_response_content = self.extract_response_content(seq_response)
            return seq_response_content
        
        except Exception as e:
            return {"error": f"Error in arranging response: {str(e)}"}
