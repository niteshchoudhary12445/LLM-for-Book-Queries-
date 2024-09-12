import requests
import fitz  
from io import BytesIO
import os

api_key = os.getenv("API_KEY")
cse_id = os.getenv("CSE_ID")

def google_search(query, api_key, cse_id):
    # Google Custom Search API endpoint
    url = 'https://www.googleapis.com/customsearch/v1'

    # Parameters for the search query
    params = {
        'key': api_key,
        'cx': cse_id,
        'q': query,  # Search query/topic
        'num': 10     # Number of search results to return
    }

    # Make a request to the Google Custom Search API
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        results = response.json()
        pdf_link = None
        non_pdf_links = []

        # Extract the first PDF link, if found
        for item in results.get('items', []):
            link = item.get('link')
            if link.endswith(".pdf"):
                pdf_link = link
                break  # Stop the loop once a PDF is found
            else:
                if len(non_pdf_links) < 7:  # Collect up to 3 non-PDF links
                    non_pdf_links.append(link)

        # Return the PDF link if found, otherwise return the first 7 non-PDF links
        if pdf_link:
            return pdf_link
        elif non_pdf_links:
            return non_pdf_links
        else:
            return None
    else:
        print(f"Error: {response.status_code}")
        return None

def request_parse(query):
    url = google_search(query=query, api_key=api_key, cse_id=cse_id)
    
    if not url:
        print("No valid URL found.")
        return None
    
    # If multiple non-PDF links are returned, display them
    if isinstance(url, list):
        return f"Non-PDF links: {', '.join(url)}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)  # Send the request for the URL
    
    if response.status_code == 200:
        # If it's a PDF, handle it
        if url.endswith('.pdf'):
            pdf_content = BytesIO(response.content)  # Create a BytesIO object from the response content

            # Open the PDF using PyMuPDF
            pdf_opener = fitz.open(stream=pdf_content, filetype="pdf")
            
            # Extract text from all pages
            all_text = ""
            for page_num in range(pdf_opener.page_count):
                page = pdf_opener.load_page(page_num)
                page_content = page.get_text()
                all_text += f"Page {page_num + 1}:\n{page_content}\n"  # Append page content with page num
            
            return all_text
        else:
            return f"Non-PDF link: {url}"
    else:
        print(f"Failed to fetch the URL. Status code: {response.status_code}")
        return None
