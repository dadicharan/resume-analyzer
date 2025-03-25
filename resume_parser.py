import PyPDF2
from docx import Document
import ollama
import re
from rapidjson import loads
from typing import Dict, Union

from resumeparser import parse_llm_response

def parse_resume(file_path: str) -> str:
    """
    Extract text from resume files (PDF or DOCX)
    
    Args:
        file_path: Path to the resume file
        
    Returns:
        Extracted text as a single string
    """
    text = ""
    
    try:
        if file_path.endswith('.pdf'):
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() or ""
        
        elif file_path.endswith('.docx'):
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        
        # Clean text
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    except Exception as e:
        raise ValueError(f"Failed to parse resume: {str(e)}")

def analyze_with_llm(resume_text: str, resume_type: str) -> Dict[str, Union[str, list, dict]]:
    """
    Analyze resume text using LLM
    
    Args:
        resume_text: Extracted text from resume
        resume_type: Either "Fresher" or "Experienced"
        
    Returns:
        Dictionary with parsed resume data or error information
    """
    # Define the expected JSON schema
    json_schema = {
        "Name": "string",
        "Contact": {
            "email": "string",
            "phone": "string",
            "linkedin": "string (optional)"
        },
        "Education": [{
            "degree": "string",
            "institution": "string",
            "year": "string"
        }],
        "Skills": ["list", "of", "skills"],
        "Projects": ["list", "of", "projects"] if resume_type == "Fresher" else None,
        "Experience": [{
            "role": "string",
            "company": "string",
            "duration": "string",
            "description": "string (optional)"
        }] if resume_type == "Experienced" else None,
        "Achievements": ["list", "of", "achievements"] if resume_type == "Experienced" else None
    }
    
    prompt = f"""Analyze this {resume_type.lower()} resume and return EXACTLY in this JSON format:
{str(json_schema)}

Important Rules:
1. Only return valid JSON without any additional text
2. Don't include markdown code blocks
3. All fields must match the schema exactly
4. For missing information, use null or empty strings

Resume Text:
{resume_text[:5000]}  # Limiting to first 5000 chars for performance
"""
    
    try:
        response = ollama.chat(
            model='llama3',  # Using llama3 as default
            options={'temperature': 0.3},  # More deterministic output
            messages=[{
                'role': 'user',
                'content': prompt
            }]
        )
        
        # Parse and validate the response
        raw_response = response['message']['content'].strip()
        
        # Try to extract JSON if wrapped in markdown
        if raw_response.startswith('```json'):
            raw_response = raw_response[7:-3].strip()
        
        parsed_data = loads(raw_response)
        
        # Basic validation
        if not isinstance(parsed_data, dict):
            raise ValueError("Response is not a JSON object")
        
        return parsed_data
    
    except Exception as e:
        return {
            "Error": f"Analysis failed: {str(e)}",
            "Raw Response": raw_response if 'raw_response' in locals() else None,
            "Suggestion": "Try again with a different model or check your Ollama installation"
        }
def analyze_with_llm(resume_text, resume_type):
    """Analyze resume with automatic model fallback"""
    models_to_try = ['llama3', 'mistral', 'deepseek-coder']
    
    for model in models_to_try:
        try:
            prompt = f"""Analyze this {resume_type} resume..."""  # Your existing prompt
            
            response = ollama.chat(
                model=model,
                messages=[{'role': 'user', 'content': prompt}]
            )
            return parse_llm_response(response['message']['content'])
            
        except Exception as e:
            continue  # Try next model
    
    return {
        "Error": f"All models failed. Available models: {ollama.list()}",
        "Solution": "Run: ollama pull llama3"
    }