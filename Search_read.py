import requests
import fitz  
from io import BytesIO
import os
from bs4 import BeautifulSoup

api_key = os.getenv("API_KEY")
cse_id = os.getenv("CSE_ID")

def google_search(query, api_key, cse_id):
    # Google Custom Search API endpoint
    url = 'https://www.googleapis.com/customsearch/v1'

    # Parameters for the search query
    params = {
        'key': api_key,
        'cx': cse_id,
        'q': query,  # Search query
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
                if len(non_pdf_links) < 3:  # Collect up to 3 non-PDF links
                    non_pdf_links.append(link)

        # Return the PDF link if found, otherwise return the first 3 non-PDF links
        if pdf_link:
            return pdf_link
        elif non_pdf_links:
            return non_pdf_links
        else:
            return None
    else:
        print(f"Error: {response.status_code}")
        return None

def fetch_pdf_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)  # Send the request for the URL
    
    if response.status_code == 200:
        pdf_content = BytesIO(response.content)  # Create a BytesIO object from the response content
        pdf_opener = fitz.open(stream=pdf_content, filetype="pdf")
        all_text = ""
        for page_num in range(pdf_opener.page_count):
            page = pdf_opener.load_page(page_num)
            page_content = page.get_text()
            all_text += f"Page {page_num + 1}:\n{page_content}\n"  # Append page content with page num
        return all_text
    else:
        print(f"Failed to fetch the PDF. Status code: {response.status_code}")
        return None

def fetch_html_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)  # Send the request for the URL
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        # Extract main content (you can customize this based on the structure of the webpage)
        main_content = soup.get_text(separator="\n")
        return main_content.strip()  # Return the extracted text
    else:
        print(f"Failed to fetch the HTML. Status code: {response.status_code}")
        return None

def request_parse(query):
    url = google_search(query=query, api_key=api_key, cse_id=cse_id)
    
    if not url:
        print("No valid URL found.")
        return None
    
    # If multiple non-PDF links are returned, display them
    if isinstance(url, list):
        non_pdf_texts = []
        for link in url:
            print(f"Fetching content from non-PDF link: {link}")
            content = fetch_html_content(link)
            if content:
                non_pdf_texts.append(content)
        return "\n\n".join(non_pdf_texts) if non_pdf_texts else "No valid content found for non-PDF links."
    
    # If it's a single PDF link, handle it
    if url.endswith('.pdf'):
        return fetch_pdf_content(url)
    else:
        return fetch_html_content(url)
