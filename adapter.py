from langchain.schema import SystemMessage, HumanMessage

class Adapter:
    def __init__(self, prompt: str):
        """Initialize with a student prompt."""
        self.prompt = prompt

    def create_system_message(self, role_description: str) -> SystemMessage:
        """Create a system message based on the assistant's role description."""
        return SystemMessage(content=f"You are a helpful AI assistant. Your job is to {role_description}.")

    def student_basic_query(self):
        """Set up the message chain for basic student queries."""
        return [
            self.create_system_message("answer student queries"),
            HumanMessage(content=self.prompt)
        ]

    def document_reader_query(self):
        """Set up the message chain for document-reading queries."""
        return [
            self.create_system_message("Read this doc and answer the student's query"),
            HumanMessage(content=self.prompt)
        ]

    def pubmed_query(self):
        """Set up the message chain for PubMed-related queries."""
        return [
            self.create_system_message("answer queries related to medical papers, research articles, and clinical studies on PubMed"),
            HumanMessage(content=self.prompt)
        ]

    def arxiv_query(self):
        """Set up the message chain for Arxiv-related queries."""
        return [
            self.create_system_message("answer queries related to research papers on computer science, physics, mathematics, and other scientific fields on Arxiv"),
            HumanMessage(content=self.prompt)
        ]
