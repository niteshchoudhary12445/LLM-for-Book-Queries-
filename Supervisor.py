from LLM_layer import LLMLayer
from adapter import Adapter

class Supervisor:
    
    def __init__(self, prompt, query_type="student"):
        """
        Initialize with the student prompt and query type.
        
        Args:
            prompt (str): The query prompt from the user.
            query_type (str): The type of query, default is 'Student Query'. 
                              Options include 'Student Query', 'Upload Document', 'Medical Research (PubMed)', 'Scientific Papers (Arxiv)'.
        """
        self.prompt = prompt
        self.query_type = query_type
        self.llm = LLMLayer()

    def handle_query_type(self):
        """ 
        Handle the different query types based on the prompt context.
        
        Returns:
            list: A list of messages to be processed by the LLM.
        """
        adapter = Adapter(prompt=self.prompt)

        query_type_mapping = {
            "Student Query": adapter.student_basic_query,
            "Upload Document": adapter.document_reader_query,
            "Medical Research (PubMed)": adapter.pubmed_query,
            "Scientific Papers (Arxiv)": adapter.arxiv_query,
        }

        return query_type_mapping[self.query_type]()

    def generate_response(self):
        """ 
        Generate the LLM's response based on the query type and prompt.
        
        Returns:
            str: The LLM response or error message.
        """
        try:
            # Handle query type to generate the appropriate messages
            query_messages = self.handle_query_type()

            # Generate the response using the LLM layer
            response = self.llm.query_response(query=query_messages)

            return response

        except Exception as e:
            return f"Error generating response: {str(e)}"
