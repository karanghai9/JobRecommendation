import streamlit as st

def main():
    st.title("LLM Powered Job Recommendation System")

    # File uploader for PDF
    uploaded_file = st.file_uploader("Upload your resume", type="pdf")

    if uploaded_file is not None:
        st.write(f"Uploaded File: {uploaded_file.name}")

        # Read and display the uploaded file's content
        file_bytes = uploaded_file.read()
        st.success("File uploaded successfully!")

if __name__ == "__main__":
    main()
