from LLM_layer import LLMLayer
from adapter import Adapter

class Supervisor:
    
    def __init__(self, prompt):
        self.prompt = prompt
        self.llm = LLMLayer()
        self.adapter = Adapter(prompt=self.prompt)

    def generate_response(self):
        try:
            # Generate the student query prompt and get the response
            student_query_prompt = self.adapter.student_query()
            query_response = self.llm.student_query_chain(student_query_prompt)

            # Generate the recommendation prompt and get the recommendation response
            recommender_prompt = self.adapter.recommender()
            recommender_response = self.llm.book_recommender_chain(recommender_prompt)

            # Arrange the final response sequence
            response_seq = self.adapter.response_sequence(
                query_response, recommender_response
            )

            # Arrange the response and get the final response
            final_response = self.llm.arrange_response_in_sequence(response_seq)

            return final_response

        except Exception as e:
            return f"Error generating response: {str(e)}"
        
    def generate_response_for_book(self):
        try:
            # Provide the answer related to the book
            pdf_prompt = self.adapter.pdf(self.prompt)
            pdf_response = self.llm.doc_reader(pdf_prompt)
            return pdf_response
        except Exception as e:
            return f"Error unable to read book content: {str(e)}"
        