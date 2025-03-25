# Resume Analyzer AI  
✨ *Analyze resumes with AI (no cloud needed!)*  

### How to Run:  
1. Install Ollama:  
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama pull llama3

# resume-analyzer
**AI Resume Analyzer** 📊    LLM-powered tool (Ollama/Streamlit) that extracts key details from resumes (PDF/DOCX). Analyzes fresher/experienced profiles with structured insights. Easy setup, customizable prompts.    🔗 [github.com/dadicharan/resume-analyzer](https://github.com/dadicharan/resume-analyzer)    #AI #LLM #RecruitmentTech

Here's a polished **GitHub repository description** for your Resume Analyzer project that clearly explains its purpose and features:

---

# **Resume Analyzer AI**  
**📄 LLM-Powered Resume Analysis Tool**  

A **Streamlit** web app that uses **Ollama's LLM models** (like `llama3`, `mistral`) to analyze resumes in PDF/DOCX format. Extracts key details, categorizes information for freshers/experienced candidates, and presents structured insights.

➡ **Live Demo**: [Coming Soon] *(Host on Streamlit Cloud if needed)*  

---

## **✨ Key Features**  
✅ **Smart Resume Parsing**  
- Extracts text from **PDF & DOCX** files  
- Cleans and preprocesses resume content  

✅ **LLM-Powered Analysis**  
- Uses **Ollama** (local LLM) with `llama3`/`mistral`  
- Custom prompts for **freshers** (education, projects) and **experienced** (work history, skills)  

✅ **User-Friendly Interface**  
- **Streamlit** dashboard with:  
  - Resume preview  
  - Structured data tables  
  - Key insights sections  
- Dark/light mode compatible  

✅ **Error Handling**  
- Fallback models if primary fails  
- Clear error messages for debugging  

---

## **🛠️ Tech Stack**  
| Component       | Technology Used |  
|----------------|----------------|  
| **Frontend**   | Streamlit |  
| **LLM**        | Ollama (`llama3`, `mistral`) |  
| **Parsing**    | PyPDF2, python-docx |  
| **Data**       | pandas, rapidjson |  

---

## **📌 Ideal For**  
- **Job seekers** to optimize resumes  
- **Recruiters** to quickly scan candidate profiles  
- **Developers** learning LLM integration  

---

### **📂 Repository Structure**  
```bash
resume-analyzer/
├── app.py                # Main Streamlit app
├── utils/
│   ├── __init__.py       # Package initialization
│   └── resume_parser.py  # Core parsing/analysis logic
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── .gitignore            # Excludes virtualenv/files
```

---

### **🚀 Why Contribute?**  
- **Easy to customize** (change LLM prompts/models)  
- **Lightweight** (runs locally without GPU)  
- **Educational** for AI/Streamlit beginners  

🔗 **GitHub Link**: https://github.com/dadicharan/resume-analyzer  

---

### **🎯 Future Improvements**  
- [ ] Add **multi-resume comparison**  
- [ ] Support **image-based resumes** (OCR)  
- [ ] Deploy as **public web app**  

   

**Pro Tip**: Add a `demo.gif` showing the app in action to make it more engaging!
