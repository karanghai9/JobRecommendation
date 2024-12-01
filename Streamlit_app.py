import streamlit as st

def main():
    st.title("PDF File Uploader")

    # File uploader for PDF
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    if uploaded_file is not None:
        st.write(f"Uploaded File: {uploaded_file.name}")

        # Read and display the uploaded file's content
        file_bytes = uploaded_file.read()
        st.success("File uploaded successfully!")

        # Show the first few bytes as proof of upload
        st.write("File Content (First 500 bytes):")
        st.code(file_bytes[:500])

        # Save the file locally (optional)
        with open("uploaded_file.pdf", "wb") as f:
            f.write(file_bytes)
        st.write("File saved locally as 'uploaded_file.pdf'.")

if __name__ == "__main__":
    main()
