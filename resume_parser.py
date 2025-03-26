import PyPDF2
from docx import Document
import ollama
import re
from rapidjson import loads
from typing import Dict, Union
from io import BytesIO
import random
import time

def parse_pdf_from_bytes(file_bytes: bytes) -> str:
    """Parse PDF directly from bytes in memory"""
    try:
        text = ""
        reader = PyPDF2.PdfReader(BytesIO(file_bytes))
        for page in reader.pages:
            text += page.extract_text() or ""
        return re.sub(r'\s+', ' ', text).strip()
    except Exception as e:
        raise ValueError(f"PDF parsing failed: {str(e)}")

def parse_docx_from_bytes(file_bytes: bytes) -> str:
    """Parse DOCX directly from bytes in memory"""
    try:
        text = ""
        doc = Document(BytesIO(file_bytes))
        for para in doc.paragraphs:
            text += para.text + "\n"
        return re.sub(r'\s+', ' ', text).strip()
    except Exception as e:
        raise ValueError(f"DOCX parsing failed: {str(e)}")

def analyze_with_llm(resume_text: str, resume_type: str) -> Dict[str, Union[str, list, dict]]:
    """
    Analyze resume text with robust error handling
    Returns either:
    - LLM analysis results
    - Mock data if LLM fails
    - Error details if all fails
    """
    # First try with Ollama
    try:
        start_time = time.time()
        
        prompt = f"""Extract structured information from this {resume_type} resume in JSON format:
        {{
            "Name": "full name",
            "Contact": {{"email": "", "phone": ""}},
            "Education": [{{"degree": "", "institution": "", "year": ""}}],
            "Skills": ["skill1", "skill2"],
            {"Projects" if resume_type == "Fresher" else "Experience"}: []
        }}
        
        Resume Content:
        {resume_text[:3000]}
        """
        
        response = ollama.chat(
            model='llama3',
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0.2}
        )
        
        # Parse response
        result = parse_llm_response(response['message']['content'])
        result["Analysis Time"] = f"{time.time() - start_time:.2f} seconds"
        return result
        
    except Exception as e:
        # Fallback to mock data
        try:
            return generate_mock_data(resume_type)
        except Exception:
            return {
                "Error": "Analysis failed",
                "Details": str(e),
                "Suggestion": "Try again later or check Ollama service"
            }

def generate_mock_data(resume_type: str) -> dict:
    """Generate realistic sample resume data"""
    base = {
        "Name": "John Doe",
        "Contact": {"email": "john@example.com", "phone": "123-456-7890"},
        "Skills": ["Python", "Data Analysis", "Machine Learning"],
        "Status": "Sample Data (LLM Unavailable)"
    }
    
    if resume_type == "Fresher":
        base.update({
            "Education": [{"degree": "B.Tech CS", "institution": "State University", "year": "2023"}],
            "Projects": ["Resume Analyzer", "Student Portal"]
        })
    else:
        base.update({
            "Education": [{"degree": "M.Tech AI", "institution": "Tech University", "year": "2018"}],
            "Experience": [{
                "role": "Data Scientist",
                "company": "TechCorp", 
                "duration": "3 years",
                "description": "Developed ML models"
            }]
        })
    return base

def parse_llm_response(response_text: str) -> dict:
    """Clean and parse LLM response"""
    try:
        # Remove markdown formatting
        if response_text.startswith('```json'):
            response_text = response_text[7:-3].strip()
        return loads(response_text)
    except Exception:
        return {"Raw Response": response_text, "Status": "Unparsed Output"}
