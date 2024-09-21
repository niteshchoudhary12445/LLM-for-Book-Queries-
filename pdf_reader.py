import tempfile
import fitz  

def document_loader(uploaded_file):
    """Loads PDF documents from an uploaded file using PyMuPDF."""
    
    # Check if the uploaded file is valid
    if uploaded_file:
        try:
            # Create a temporary file to store the uploaded file
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(uploaded_file.read())  # Use read() to get the binary content
                tmp_file_path = tmp_file.name  # Get the path of the temporary file

            # Load the PDF using PyMuPDF
            pdf_text = ""
            with fitz.open(tmp_file_path) as pdf_document:
                for page in pdf_document:
                    pdf_text += page.get_text()  # Extract text from each page

            return pdf_text
        except Exception as e:
            print(f"Error loading PDF: {str(e)}")
            return None
    else:
        print("No valid PDF file uploaded.")
        return None
