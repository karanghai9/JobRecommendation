import streamlit as st
import PyPDF2

def main():
    st.title("LLM Powered Job Recommendation System")

    # File uploader for PDF
    uploaded_file = st.file_uploader("Upload your resume", type="pdf")

    if uploaded_file is not None:
        st.write(f"Uploaded File: {uploaded_file.name}")

        # Read and display the uploaded file's content
        file_bytes = uploaded_file.read()

        # Extract text from the uploaded PDF
        resume_text = extract_text_from_pdf(file_bytes)
        
        if resume_text:
            st.success("File uploaded and text extracted successfully!")
            st.text_area("Extracted Text", resume_text, height=300)
        else:
            st.error("No text found in the PDF.")

def extract_text_from_pdf(file_bytes):
    try:
        # Use PyPDF2 to read from in-memory bytes
        reader = PyPDF2.PdfReader(file_bytes)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text.strip() if text else "No text found."
    except Exception as e:
        return f"Error extracting text: {str(e)}"

if __name__ == "__main__":
    main()
