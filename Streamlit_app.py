import streamlit as st
import PyPDF2
from io import BytesIO

def main():
    st.title("LLM Powered Job Recommendation System")

    # File uploader for PDF
    uploaded_file = st.file_uploader("Upload your resume", type="pdf")

    if uploaded_file is not None:
        st.write(f"Uploaded File: {uploaded_file.name}")

        # Extract text from the uploaded PDF
        text = extract_text_from_pdf(uploaded_file)

        if text:
            st.success("File uploaded and processed successfully!")
            st.text_area("Extracted Text", text, height=300)
        else:
            st.error("No text found in the PDF.")

def extract_text_from_pdf(uploaded_file):
    try:
        # Use BytesIO to simulate file-like object
        pdf_file = BytesIO(uploaded_file.read())
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""  # Handle potential None return
        return text.strip() if text else "No text found."
    except Exception as e:
        return f"Error extracting text: {str(e)}"

if __name__ == "__main__":
    main()
