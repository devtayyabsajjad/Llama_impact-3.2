<div align="center">

# 🏛️ GovEase

<img src="https://raw.githubusercontent.com/Platane/snk/output/github-contribution-grid-snake.svg" alt="snake animation" width="100%"/>

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-FF4B4B.svg)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Groq-AI-orange.svg)](https://groq.com/)
[![BeautifulSoup](https://img.shields.io/badge/BS4-Latest-green.svg)](https://www.crummy.com/software/BeautifulSoup/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

<p align="center">
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=2196F3&center=true&vCenter=true&width=435&lines=Your+Government+Document+Assistant;Simplifying+Bureaucratic+Processes;Multi-language+Support;Intelligent+Document+Search" alt="Typing SVG" />
</p>

Navigate government procedures with ease using AI-powered document search and comprehensive guidance.

</div>

## ✨ Features

<div align="center">
<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">
</div>

- 🌐 **Multi-Language Support**
  - English, Hindi, Spanish, French, German, Urdu
  - Real-time translation capabilities
  
- 🔍 **Intelligent Search**
  - Advanced web crawling
  - PDF document processing
  - Concurrent document analysis
  
- 🎯 **User-Friendly Interface**
  - Clean, modern design
  - Dark mode support
  - Progress tracking
  - Responsive layout

- 🚀 **Smart Processing**
  - Asynchronous operations
  - Concurrent document processing
  - Timeout handling
  - Robust error management

<div align="center">
<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">
</div>

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/govease.git

# Navigate to project directory
cd govease

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Run the application
streamlit run main.py
```

## 🛠️ Environment Setup

```env
GROQ_API_KEY=your_groq_api_key
SERPER_API_KEY=your_serper_api_key
BROWSERLESS_API_KEY=your_browserless_api_key
```

## 🏗️ Architecture

```mermaid
graph TD
    A[User Query] --> B[Language Selection]
    B --> C[Country Selection]
    C --> D[Search Processing]
    D --> E[Document Analysis]
    E --> F[Translation]
    F --> G[Results Display]
    
    style A fill:#2196F3,stroke:#fff,stroke-width:2px
    style G fill:#2196F3,stroke:#fff,stroke-width:2px
```

## 💻 Tech Stack

<div align="center">
<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">
</div>

- **Frontend**: 
  - Streamlit
  - Custom CSS
  - Responsive Design

- **Backend**:
  - Python 3.9+
  - Asyncio
  - Concurrent.futures

- **AI & Processing**:
  - Groq AI
  - BeautifulSoup4
  - PyPDF2
  - Langdetect

- **APIs**:
  - Serper API
  - Browserless API

## 📱 Interface

<div align="center">
<table>
<tr>
<td width="50%">
<p align="center">
<strong>Home Page</strong><br>
• Welcome Screen<br>
• Language Selection<br>
• Quick Start Guide
</p>
</td>
<td width="50%">
<p align="center">
<strong>Search Interface</strong><br>
• Query Input<br>
• Progress Tracking<br>
• Results Display
</p>
</td>
</tr>
</table>
</div>

## 🌟 Key Features Explained

<div align="center">
<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">
</div>

### 🔄 Concurrent Processing
```python
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    future_to_url = {
        executor.submit(
            self.search_tool.process_url_with_timeout, 
            result.get('link', '')
        ): result.get('link', '')
        for result in search_results[:total_urls]
    }
```

### 🎨 Custom Styling
```python
gradient_css = """
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    }
```

## 📈 Future Enhancements

- [ ] Document Template Generation
- [ ] User Authentication System
- [ ] Mobile Application
- [ ] API Integration for Third-party Services
- [ ] Offline Document Cache

## 🤝 Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Contact

Project Link: [https://github.com/yourusername/govease](https://github.com/yourusername/govease)

<div align="center">

### ⭐ Star this repo if you find it helpful!

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

<p align="center">
Made with ❤️ by Your Name
</p>

</div>

<!-- Team Section with Hover Effects -->
## 👥 Meet Team LegalBuddy

<table>
  <tr>
    <td align="center">
      <a href="https://www.linkedin.com/in/asim-khan-baloch/"><img src="https://github.com/Asimbaloch.png" width="120px;" alt="Asim Khan"/><br /><sub><b>Asim Khan</b><br></sub></a><br />
      <a href="https://www.linkedin.com/in/asim-khan-baloch/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" width="100px"/></a>
      <a href="https://github.com/Asimbaloch"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" width="100px"/></a>
    </td>
    <td align="center">
      <a href="http://www.linkedin.com/in/tayyab-sajjad-156ab2267"><img src="https://avatars.githubusercontent.com/u/124726671?v=4" width="120px;" alt="Tayyab Sajjad"/><br /><sub><b>Tayyab Sajjad</b><br></sub></a><br />
      <a href="http://www.linkedin.com/in/tayyab-sajjad-156ab2267"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" width="100px"/></a>
      <a href="https://github.com/devtayyabsajjad"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" width="100px"/></a>
    </td>
    <td align="center">
      <a href="https://www.linkedin.com/in/muhammad-jawad-86507b201"><img src="https://github.com/mj-awad17.png" width="120px;" alt="Muhammad Jawad"/><br /><sub><b>Muhammad Jawad</b><br></sub></a><br />
      <a href="https://www.linkedin.com/in/muhammad-jawad-86507b201"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" width="100px"/></a>
      <a href="https://github.com/mj-awad17"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" width="100px"/></a>
    </td>
    <td align="center">
      <a href="https://www.linkedin.com/in/muhammad-bilal-a75782280/"><img src="https://github.com/bilal77511.png" width="120px;" alt="Muhammad Bilal"/><br /><sub><b>Muhammad Bilal</b><br></sub></a><br />
      <a href="https://www.linkedin.com/in/muhammad-bilal-a75782280/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" width="100px"/></a>
      <a href="https://github.com/bilal77511"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" width="100px"/></a>
    </td>
    <td align="center">
      <a href="https://www.linkedin.com/in/muhammad-ibrahim-qasmi-9876a1297/"><img src="https://github.com/muhammadibrahim313.png" width="120px;" alt="Muhammad Ibrahim"/><sub><br><b>Muhammad Ibrahim</b><br></sub></a><br />
      <a href="https://www.linkedin.com/in/muhammad-ibrahim-qasmi-9876a1297/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" width="100px"/></a>
      <a href="https://github.com/muhammadibrahim313"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" width="100px"/></a>
    </td>
   <td align="center">
  <a href="https://www.linkedin.com/in/rosannamannan/"><img src="https://avatars.githubusercontent.com/u/26120707?v=4" width="120px;" alt="Rosana Mannan"/><sub><br><b>Rosana Mannan</b><br></sub></a><br />
  <a href="https://www.linkedin.com/in/rosannamannan/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" width="100px"/></a>
  <a href="https://github.com/RMannan6"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" width="100px"/></a>
</td>
  </tr>
</table>

<div align="center">

## Connect with Us

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/muhammad-ibrahim-qasmi-9876a1297/)
[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/LegalBuddyAI)

<sub> Built by __B-TAJI Crew__ </sub>

</div>


