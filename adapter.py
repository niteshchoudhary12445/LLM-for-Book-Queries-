from langchain.schema import SystemMessage, HumanMessage, AIMessage

class Adapter:
    
    def __init__(self, prompt):
        self.prompt = prompt

    def student_query(self):
        """Prepare prompt for handling student queries."""
        self.student_query_prompt = [
            SystemMessage(content="You are a knowledgeable AI assistant. Your role is to answer all student queries with accurate and helpful information."),
            HumanMessage(content=self.prompt),
            AIMessage(content="I will gather the information and provide you with a detailed response shortly.")
        ]
        return self.student_query_prompt
    
    def recommender(self):
        """Prepare prompt for recommending books, articles, and papers."""
        self.recommend = [
            SystemMessage(content="You are a knowledgeable AI assistant. Your role is to recommend relevant books, papers, and articles based on the user's query."),
            HumanMessage(content=self.prompt),
            AIMessage(content="Based on your query, I recommend the following resources:")
        ]
        return self.recommend
    
    def pdf(self, book_content):
        """Prepare prompt for providing PDF links based on book content."""
        self.link_provider = [
            SystemMessage(content="You are an AI assistant specialized in reading documents and providing structured, concise information based on the content. Your responses should be well-organized and easy to follow."),
            HumanMessage(content=book_content),
            AIMessage(content="Based on the document you provided, here is the structured information:")
        ]
        return self.link_provider

    def response_sequence(self, query, recommender):
        """Prepare prompt for providing responses in a specific sequence."""
        self.response = [
            SystemMessage(content="You are a knowledgeable AI assistant tasked with analyzing and structuring responses accurately."),
            HumanMessage(content=f"""Please provide your response in the following sequence:
                1. **Explanation**: Offer a detailed explanation related to the query: "{query}". Ensure the information is relevant and well-structured.
                2. **Recommendations**: Based on the query and the recommendation context: "{recommender}", provide suggestions for books, papers, or articles. Ensure the recommendations are pertinent and presented clearly.
            """),
            AIMessage(content='Here is your organized response:')
        ]
        return self.response
