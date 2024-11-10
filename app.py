import streamlit as st
import requests
from bs4 import BeautifulSoup
import PyPDF2
import io
from groq import Groq
from typing import List, Dict, Optional
import validators
import time
import asyncio
import concurrent.futures
from functools import lru_cache

# Set Streamlit theme to dark mode
st.set_page_config(
    page_title="GovEase",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.example.com/help',
        'Report a bug': "https://www.example.com/bug",
        'About': "# GovEase - Your Government Document Assistant"
    }
)

# Force dark theme with original styling
st.markdown("""
    <script>
        var elements = window.parent.document.getElementsByTagName('iframe');
        for (var i = 0; i < elements.length; i++) {
            elements[i].setAttribute('data-theme', 'dark');
        }
    </script>
    """, unsafe_allow_html=True)

# Apply your custom styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    }
    .main {
        color: white !important;
    }
    .stButton button {
        background-color: #2a5298;
        color: white;
    }
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
    }
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
    }
    .sidebar-logo {
        width: 150px;
        margin: 0 auto;
        display: block;
    }
    .stSpinner {
        color: white !important;
    }
    .stProgress .st-bo {
        background-color: #2a5298;
    }
    .stAlert {
        background-color: rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Cache configurations
@st.cache_data(ttl=3600)
def cached_search_google(query: str, api_key: str, max_results: int = 5) -> List[Dict]:
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query,
        "num": max_results
    }
    try:
        response = requests.post(
            "https://google.serper.dev/search",
            headers=headers,
            json=payload,
            timeout=10
        )
        return response.json().get('organic', [])[:max_results]
    except Exception as e:
        st.warning(f"Search error: {str(e)}")
        return []

@st.cache_data(ttl=3600)
def cached_webpage_content(url: str) -> str:
    if not validators.url(url):
        return ""
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = ' '.join([p.get_text() for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'li'])])
        return text[:2000]
    except Exception:
        return ""

class DocumentSearchTool:
    def __init__(self):
        self.serper_api_key = st.secrets.SERPER_API_KEY
        self.browserless_api_key = st.secrets.BROWSERLESS_API_KEY
        self.visited_urls = set()
        self.pdf_docs = []
        self.search_timeout = 20  # Reduced from 30
        self.max_pdfs = 2  # Reduced from 3
        self.max_pages = 1  # Reduced from 2

    def search_google(self, query: str, max_results: int = 5):
        return cached_search_google(query, self.serper_api_key, max_results)

    def process_url_with_timeout(self, url: str, timeout: int = 5) -> Optional[Dict]:
        try:
            if url.lower().endswith('.pdf'):
                content = self.extract_pdf_content(url)
                doc_type = "pdf"
            else:
                content = cached_webpage_content(url)
                doc_type = "webpage"

            if content:
                return {
                    "url": url,
                    "title": url.split('/')[-1],
                    "content": content[:1000],
                    "type": doc_type
                }
        except Exception as e:
            st.warning(f"Error processing {url}: {str(e)}")
        return None

    def extract_pdf_content(self, pdf_url: str) -> Optional[str]:
        try:
            response = requests.get(pdf_url, timeout=5)
            pdf_file = io.BytesIO(response.content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            return ' '.join([page.extract_text() for page in pdf_reader.pages[:1]])
        except Exception:
            return None

class SearchAssistant:
    def __init__(self):
        self.search_tool = DocumentSearchTool()
        self.groq_client = Groq(api_key=st.secrets.GROQ_API_KEY)

    async def translate_text(self, text: str, target_language: str) -> str:
        try:
            prompt = f"Translate the following text to {target_language}:\n\n{text}"
            chat_completion = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama2-70b-4096",
                temperature=0.3,
                max_tokens=500,
                timeout=10
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            st.error(f"Translation error: {str(e)}")
            return text

    def process_query(self, query: str, language: str, country: str) -> Dict:
        start_time = time.time()
        
        with st.spinner("🔍 Searching for relevant documents..."):
            enhanced_query = f"{query} {country} government documents"
            search_results = self.search_tool.search_google(enhanced_query)
        
        documents = []
        processed_count = 0
        total_urls = min(len(search_results), 3)  # Reduced from 5

        with st.spinner("📄 Processing documents..."):
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                future_to_url = {
                    executor.submit(
                        self.search_tool.process_url_with_timeout, 
                        result.get('link', '')
                    ): result.get('link', '')
                    for result in search_results[:total_urls]
                }

                for future in concurrent.futures.as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        doc = future.result(timeout=5)
                        if doc:
                            documents.append(doc)
                    except Exception:
                        continue
                    
                    processed_count += 1
                    
                    if time.time() - start_time > 20:  # Reduced from 30
                        break

        with st.spinner("🤔 Analyzing information..."):
            docs_text = "\n\n".join([
                f"Document: {doc['title']}\nType: {doc['type']}\nURL: {doc['url']}\nContent: {doc['content']}"
                for doc in documents
            ])

            prompt = f"""
            Query: {query}
            Country: {country}
            
            Based on the available information, provide a concise response that includes:
            1. Key requirements and documents needed
            2. Basic steps to follow
            3. Relevant official links
            
            If the information is incomplete, please indicate what might be missing.
            
            Available Information:
            {docs_text}
            """

            try:
                chat_completion = self.groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama2-70b-4096",
                    temperature=0.3,
                    max_tokens=500
                )
                response_content = chat_completion.choices[0].message.content

                if language != "English":
                    with st.spinner("🌐 Translating response..."):
                        response_content = asyncio.run(self.translate_text(response_content, language))

            except Exception as e:
                st.error(f"Error processing response: {str(e)}")
                response_content = "Could not process the complete response. Here's what we found in our initial search:"
                for doc in documents:
                    response_content += f"\n\n- {doc['title']}: {doc['content'][:200]}..."

        return {
            "response": response_content,
            "documents": documents,
            "search_time": f"{time.time() - start_time:.1f} seconds"
        }

def home_page():
    st.title("Welcome to GovEase")
    st.write("""
    ### Your Government Document Assistant
    
    GovEase helps you navigate government procedures and documentation requirements 
    across different countries. Get started by:
    
    1. Selecting your preferred language
    2. Choosing your country
    3. Asking your question about government processes
    
    We'll help you find the information you need!
    """)
    
    if st.button("Start Your Search"):
        st.session_state.page = "AskWithEase"
        st.experimental_rerun()

def ask_with_ease_page():
    st.title("Ask With Ease")
    
    languages = {
        "English": "en",
        "Urdu": "ur",
        "Hindi": "hi",
        "Spanish": "es",
        "French": "fr",
        "German": "de"
    }
    selected_language = st.selectbox("Select Language", list(languages.keys()))
    
    default_countries = [
        "Pakistan", "United States", "United Kingdom", "Canada", "Australia", "India",
        "Germany", "France", "Spain", "Brazil", "Japan"
    ]
    country = st.text_input("Enter Country", key="country_input")
    if not country:
        country = st.selectbox("Or select from common countries", default_countries)
    
    query = st.text_input("What information are you looking for?", key="query_input",
                         placeholder="e.g., How to renew my passport?")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        search_button = st.button("🔍 Search")
    
    if search_button and query and country:
        try:
            search_assistant = SearchAssistant()
            results = search_assistant.process_query(query, selected_language, country)
            
            st.success(f"✨ Search completed in {results['search_time']}")
            
            st.subheader("📋 Results")
            st.write(results["response"])
            
            if results["documents"]:
                st.subheader("📚 Sources")
                for doc in results["documents"]:
                    with st.expander(f"📄 {doc['title'][:50]}..."):
                        st.write(f"Type: {doc['type']}")
                        st.write(f"URL: {doc['url']}")
                        st.write("Preview:", doc['content'][:200] + "...")
            else:
                st.warning("No detailed sources found, but we've provided the best available information.")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.error("Please try again with a different query or check your internet connection.")

def about_us_page():
    st.title("About Us")
    st.write("""
    ### Our Mission
    We aim to simplify access to government information and procedures through intelligent 
    search and comprehensive guidance. Our platform helps citizens navigate complex 
    bureaucratic processes with ease.
    
    ### What We Offer
    - Intelligent document search
    - Multi-language support with translation
    - Country-specific guidance
    - Step-by-step assistance
    - Access to official sources
    
    ### Contact Information
    For support or inquiries, please reach out to:
    - Email: support@govease.com
    - Phone: +1-XXX-XXX-XXXX
    """)

def main():
    try:
        st.sidebar.image(
            "https://your-logo-url.com/logo.png",
            width=150,
            caption="GovEase"
        )
        
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["Home", "AskWithEase", "About Us"])
        
        if page == "Home":
            home_page()
        elif page == "AskWithEase":
            ask_with_ease_page()
        else:
            about_us_page()
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        st.error("Please refresh the page and try again.")

if __name__ == "__main__":
    main()
