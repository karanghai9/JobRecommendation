import streamlit as st
from langchain_groq import ChatGroq
from io import BytesIO
import PyPDF2
import time
from playwright.sync_api import sync_playwright

# Define Groq API key and model
GROQ_API_KEY = "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"  # Replace with your actual Groq API key
groq_llama3_llm = ChatGroq(
    temperature=0.4,
    groq_api_key=GROQ_API_KEY,
    model_name="mixtral-8x7b-32768",  # Replace with the desired model
)

def main():
    st.title("LLM Powered Job Recommendation System")

    # File uploader for PDF
    uploaded_file = st.file_uploader("Upload your resume", type="pdf")

    if uploaded_file is not None:
        # Extract text from the uploaded PDF
        resume = extract_text_from_pdf(uploaded_file)

        if resume:
            st.success("File uploaded and processed successfully!")
            st.text_area("Extracted Text", resume, height=300)

            # Call the LLM to extract skills and location
            applicant_info = callLLM(resume)

            # Extract skills and location from the LLM response
            applicantSkills, applicantLocation = extract_skills_and_location(applicant_info)

            # Display the extracted skills and location
            st.subheader("Extracted Information:")
            st.write(f"Skills: {applicantSkills}")
            st.write(f"Location: {applicantLocation}")

            # Display the extracted skills and location
            st.subheader("Extracted Information:")
            st.write(f"Skills: {applicantSkills}")
            st.write(f"Location: {applicantLocation}")

            # Scrape jobs based on extracted skills and location
            fetched_data = scrapeJobsData(applicantSkills, applicantLocation)

            # Display the fetched job data
            st.subheader("Job Recommendations:")
            for job in fetched_data:
                st.write(f"Job URL: {job['URL']}")
                st.write(f"Job Description: {job['data']}")

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

def callLLM(resume):
    query = f"""Please extract the following information from the provided text and return it in the following fixed format:

    Skills = List of skills of Applicant
    Location = City, Pincode of Applicant's current residence

    The input text is as follows:
    '{resume}'

    Ensure that:
    1. The "Skills" section lists the relevant skills separated by commas.
    2. The "Location" section contains the location name (city) followed by the "Pincode" containing the postal code. Do not add Country name to it.

    Make sure the output follows the format exactly as shown, with no extra lines or spaces."""

    response = groq_llama3_llm.invoke(query)
    return response.content  # The extracted information

def extract_skills_and_location(applicant_info):
    try:
        # Split the applicant_info string based on the defined keywords and extract relevant data
        applicantSkills = applicant_info.split("Skills = ")[1].split("\n")[0].strip()
        applicantLocation = applicant_info.split("Location = ")[1].split("\n")[0].strip()
        
        return applicantSkills, applicantLocation
    except IndexError:
        return "Error: Could not extract skills or location.", "Error: Could not extract skills or location."


def scrapeJobsData(applicantSkills, applicantLocation):
    fetched_data = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Launch in headless mode
        page = browser.new_page()
    
        # Go to the target page
        page.goto("https://www.stepstone.de/work/?action=facet_selected")
    
        # Accept cookies if present
        try:
            page.click("button#ccmgt_explicit_accept")
            print("Clicked on Accept Cookies")
        except Exception as e:
            print("Could not click on 'Accept Cookies':", e)
    
        # Fill in skills and location
        page.fill('input[placeholder="(job title, skill, or company)"]', applicantSkills)
        page.fill('input[placeholder="(city or 5-digit zip code)"]', applicantLocation)
    
        # Click the search button
        page.click('button[data-at="searchbar-search-button"]')
        print("Search button clicked!")
    
        # Wait for results to load
        page.wait_for_selector('.res-nehv70')
    
        # Get job data
        job_listings = page.query_selector_all('.res-nehv70')
    
        for job in job_listings[:10]:  # Limit to the first 10 results
            job_url = job.query_selector('a').get_attribute('href')
            job_description = job.text_content()
    
            # Store the job information
            fetched_data.append({"URL": job_url, "data": job_description})
    
        # Close the browser
        browser.close()
    
    return fetched_data

if __name__ == "__main__":
    main()
