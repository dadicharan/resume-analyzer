import streamlit as st
import pandas as pd
from utils.resume_parser import parse_pdf_from_bytes, parse_docx_from_bytes, analyze_with_llm
from io import BytesIO
from rapidjson import loads

# Set page config
st.set_page_config(page_title="Resume Analyzer Pro", page_icon="📄", layout="wide")

# Custom CSS (unchanged)
st.markdown("""
<style>
    .resume-preview {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 20px;
        background-color: #f9f9f9;
        max-height: 300px;
        overflow-y: auto;
    }
    .analysis-table {
        margin-top: 20px;
    }
    .stSelectbox div[data-baseweb="select"] {
        margin-bottom: 10px;
    }
    .error-box {
        background-color: #ffebee;
        padding: 15px;
        border-radius: 5px;
        border: 1px solid #ffcdd2;
    }
</style>
""", unsafe_allow_html=True)

def display_analysis_results(results):
    """Display analysis results in organized sections"""
    st.subheader("📊 Analysis Results")
    
    # Main table view
    with st.expander("📋 Structured Data View", expanded=True):
        if isinstance(results, dict) and "Error" not in results:
            # Flatten nested structures for display
            flat_data = {}
            for key, value in results.items():
                if isinstance(value, (list, dict)):
                    flat_data[key] = str(value)
                else:
                    flat_data[key] = value
            st.dataframe(pd.DataFrame.from_dict(flat_data, orient='index', columns=['Value']))
    
    # Key insights section
    st.subheader("🔍 Key Insights")
    
    if isinstance(results, dict):
        if "Error" in results:
            st.error("Analysis failed. Please try again.")
            with st.expander("Error Details"):
                st.markdown(f"```\n{results['Error']}\n```")
                if "Raw Response" in results:
                    st.text_area("Raw LLM Response", results["Raw Response"], height=200)
        else:
            # Fresher resume insights
            if st.session_state.get('resume_type') == "Fresher":
                cols = st.columns(2)
                with cols[0]:
                    st.markdown("### 🎓 Education")
                    for edu in results.get("Education", []):
                        st.markdown(f"- **{edu.get('degree', 'N/A')}** at {edu.get('institution', 'N/A')} ({edu.get('year', 'N/A')})")
                
                with cols[1]:
                    st.markdown("### 💻 Technical Skills")
                    st.markdown("\n".join([f"- {skill}" for skill in results.get("Skills", [])]))
                
                st.markdown("### 🏆 Projects")
                for project in results.get("Projects", []):
                    st.markdown(f"- {project}")
            
            # Experienced resume insights
            else:
                cols = st.columns(2)
                with cols[0]:
                    st.markdown("### 💼 Experience")
                    for exp in results.get("Experience", []):
                        st.markdown(f"- **{exp.get('role', 'N/A')}** at {exp.get('company', 'N/A')} ({exp.get('duration', 'N/A')})")
                
                with cols[1]:
                    st.markdown("### 🛠️ Skills")
                    st.markdown("\n".join([f"- {skill}" for skill in results.get("Skills", [])]))
                
                st.markdown("### 🏅 Achievements")
                for achievement in results.get("Achievements", []):
                    st.markdown(f"- {achievement}")

def main():
    st.title("📄 AI Resume Analyzer")
    st.markdown("Upload your resume (PDF or DOCX) for detailed analysis using advanced AI")
    
    # Initialize session state
    if 'resume_text' not in st.session_state:
        st.session_state.resume_text = ""
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        st.session_state['resume_type'] = st.selectbox("Resume Type", ["Fresher", "Experienced"])
        analyze_btn = st.button("🔍 Analyze Resume", type="primary")
        st.markdown("---")
        st.markdown("**ℹ️ Model Info**")
        st.markdown("Using `llama3` via Ollama")
    
    # File uploader
    uploaded_file = st.file_uploader("📤 Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
    
    if uploaded_file is not None:
        try:
            # Read file directly into memory
            file_bytes = uploaded_file.getvalue()
            
            # Parse based on file type
            if uploaded_file.name.endswith('.pdf'):
                st.session_state.resume_text = parse_pdf_from_bytes(file_bytes)
            elif uploaded_file.name.endswith('.docx'):
                st.session_state.resume_text = parse_docx_from_bytes(file_bytes)
            
            # Display resume preview
            st.subheader("📝 Resume Preview")
            st.markdown(f'<div class="resume-preview">{st.session_state.resume_text[:3000]}</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Failed to process file: {str(e)}")
            st.session_state.resume_text = ""
        
        # Analyze button action
        if analyze_btn and st.session_state.resume_text:
            with st.spinner("🧠 Analyzing resume with AI..."):
                st.session_state.analysis_results = analyze_with_llm(
                    st.session_state.resume_text, 
                    st.session_state['resume_type']
                )
    
    # Display analysis results if available
    if st.session_state.analysis_results:
        display_analysis_results(st.session_state.analysis_results)

if __name__ == "__main__":
    main()
