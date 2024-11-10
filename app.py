import os
import streamlit as st
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import PyPDF2
import io
from langdetect import detect
from groq import Groq
from typing import List, Dict
import validators
import json

# Load environment variables
load_dotenv()

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class DocumentSearchTool:
    def __init__(self):
        self.serper_api_key = os.getenv("SERPER_API_KEY")
        self.browserless_api_key = os.getenv("BROWSERLESS_API_KEY")

    def search_google(self, query: str) -> List[Dict]:
        """Search Google using Serper API"""
        headers = {
            "X-API-KEY": self.serper_api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "q": query,
            "num": 5
        }
        response = requests.post(
            "https://google.serper.dev/search",
            headers=headers,
            json=payload
        )
        return response.json().get('organic', [])

    def scrape_webpage(self, url: str) -> str:
        """Scrape webpage content using Browserless"""
        if not validators.url(url):
            return ""
        
        payload = {
            "url": url,
            "elements": ["p", "h1", "h2", "h3", "li"]
        }
        response = requests.post(
            f"https://chrome.browserless.io/content?token={self.browserless_api_key}",
            json=payload
        )
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return ' '.join([p.get_text() for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'li'])])
        return ""

    def extract_pdf_content(self, pdf_url: str) -> str:
        """Download and extract content from PDF"""
        try:
            response = requests.get(pdf_url)
            pdf_file = io.BytesIO(response.content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            return ' '.join([page.extract_text() for page in pdf_reader.pages])
        except:
            return ""

class SearchAssistant:
    def __init__(self):
        self.search_tool = DocumentSearchTool()

    def process_query(self, query: str, language: str) -> Dict:
        # Search for relevant documents
        search_results = self.search_tool.search_google(query)
        
        # Collect and process information
        documents = []
        for result in search_results:
            url = result.get('link', '')
            content = ""
            
            if url.lower().endswith('.pdf'):
                content = self.search_tool.extract_pdf_content(url)
            else:
                content = self.search_tool.scrape_webpage(url)
            
            if content:
                documents.append({
                    "url": url,
                    "title": result.get('title', ''),
                    "content": content[:1000]  # Limit content length
                })

        # Format documents for prompt
        docs_text = "\n\n".join([
            f"Document: {doc['title']}\nURL: {doc['url']}\nContent: {doc['content']}"
            for doc in documents
        ])

        # Process with Llama model through Groq
        prompt = f"""
        Query: {query}
        Language: {language}
        
        Based on the following documents, provide a comprehensive response that:
        1. Summarizes the key requirements and documents needed
        2. Lists the specific steps to follow
        3. Provides relevant links to official sources
        
        Documents:
        {docs_text}
        """

        try:
            chat_completion = groq_client.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                model="llama3-8b-8192",
                temperature=0.3,
                max_tokens=2000
            )
            response_content = chat_completion.choices[0].message.content
        except Exception as e:
            st.error(f"Error with Groq API: {str(e)}")
            response_content = "Error processing the request with the language model."

        return {
            "response": response_content,
            "documents": documents[:5]
        }

def main():
    st.title("Government Document Search Assistant")
    
    # Language selection
    languages = {
        "English": "en",
        "Hindi": "hi",
        "Spanish": "es",
        "French": "fr",
        "German": "de"
    }
    selected_language = st.selectbox("Select Language", list(languages.keys()))
    
    # Search query input
    query = st.text_input("What information are you looking for?")
    
    if st.button("Search") and query:
        try:
            # Initialize assistant
            search_assistant = SearchAssistant()
            
            with st.spinner("Searching for relevant information..."):
                # Execute search
                results = search_assistant.process_query(query, languages[selected_language])
                
                # Display results
                st.subheader("Results")
                st.write(results["response"])
                
                st.subheader("Relevant Documents")
                for doc in results["documents"]:
                    st.markdown(f"[{doc['title']}]({doc['url']})")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()