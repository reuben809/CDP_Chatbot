# CDP Support Agent

## 📌 Overview
CDP Support Agent is a web scraping and AI-powered query system that extracts, processes, and retrieves documentation from multiple **Customer Data Platforms (CDPs)**, including **Lytics, mParticle, Segment, and Zeotap**. It enables users to search and retrieve relevant documentation efficiently by leveraging Google's **Gemini AI**.

### **🔧 Key Features**
- **Web Scraping**: Automates the extraction of documentation from various CDP platforms.
- **Data Storage & Retrieval**: Stores extracted documentation and enables keyword-based search.
- **AI-Powered Query Handling**: Uses **Gemini AI** to summarize and format responses.

---

## 📂 Project Structure
```
cdp_support_agent/
├── data/
│   ├── processors/        # Scraping and text processing
│   │   ├── lytics_scraper.py
│   │   ├── mparticle_scraper.py
│   │   ├── segment_scraper.py
│   │   ├── text_processor.py
│   │   └── zeotap_scraper.py
│   ├── storage/           # Storage and retrieval
│   │   ├── __init__.py
│   │   └── document_store.py
├── services/              # AI query handling
│   ├── __init__.py
│   ├── gemini_service.py
│   └── query_handler.py
├── utils/                 # Helper functions
│   ├── __init__.py
│   └── helper.py
├── app.py                 # Main application entry point
├── requirements.txt        # Dependencies
└── .env                   # API keys and environment variables
```

---

## 🚀 Installation & Setup

### **🔹 Prerequisites**
- Python 3.8+
- Virtual Environment (Recommended)
- ChromeDriver (if using Selenium for authentication)

### **🔹 Clone the Repository**
```bash
git clone https://github.com/your-repo/cdp-support-agent.git
cd cdp-support-agent
```

### **🔹 Set Up Virtual Environment (Optional)**
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### **🔹 Install Dependencies**
```bash
pip install -r requirements.txt
```

### **🔹 Set Up Environment Variables**
Create a `.env` file to store API keys:
```
GEMINI_API_KEY=your_gemini_api_key
```

---

## 📌 Usage
### **🔹 Run the Application**
```bash
python app.py
```

### **🔹 Scrape Documentation**
```bash
python data/processors/lytics_scraper.py
python data/processors/mparticle_scraper.py
python data/processors/segment_scraper.py
python data/processors/zeotap_scraper.py
```

### **🔹 Query the Documentation**
```python
from services.query_handler import QueryHandler

query_handler = QueryHandler()
response = query_handler.handle_query("How do I set up user tracking in Segment?")
print(response)
```

---

## 🛠️ Troubleshooting
**Issue:** Scraper fails to extract certain pages.
- Solution: Check if the website structure has changed. Update CSS selectors accordingly.

**Issue:** Getting 403 Forbidden errors.
- Solution: Add proper headers (User-Agent, Cookies) to avoid bot detection.

**Issue:** No response from Gemini API.
- Solution: Ensure `GEMINI_API_KEY` is correctly set in `.env`.

---

## 📜 License
This project is licensed under the MIT License.

---

## 🙌 Contributions
Pull requests are welcome! If you’d like to contribute, please open an issue first.

---

## 📩 Contact
For questions, reach out via [LinkedIn](https://www.linkedin.com/in/reuben-joseph-452939291/) or email at **reuben.joseph010@icloud.com**.

