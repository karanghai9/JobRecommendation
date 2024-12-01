import streamlit as st
from langchain_groq import ChatGroq
from io import BytesIO
import PyPDF2
import time
import pandas as pd

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.core.os_manager import ChromeType
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.chrome import ChromeType
from datetime import datetime
from random import randint
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

def scrape_permutations():

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=NetworkService")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-features=VizDisplayCompositor")

    with webdriver.Chrome(options=options) as driver:
        try:
            requests = 0
            driver.implicitly_wait(10)
            driver.get("https://www.stepstone.de/work/?action=facet_selected")
            sleep(randint(8, 10))
            data = driver.find_elements(by=By.XPATH, value="ccmgt_explicit_accept")
            return "hello"
        except IndexError:
            pass

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

            # Scrape jobs based on extracted skills and location
            # msg = scrapeJobsData()
            # st.success(msg)
            
            # @st.cache_resource
            # def get_driver():
            #     return webdriver.Chrome(
            #         service=Service(
            #             ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            #         ),
            #         options=options,
            #     )
            
            # options = Options()
            # options.add_argument("--disable-gpu")
            # options.add_argument("--headless")
            # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36")
            # options.add_argument("--disable-extensions")  # Disable any extensions
            # options.add_argument("--no-sandbox")  # For certain systems like Linux
            
            # driver = get_driver()
            # driver.get("https://www.stepstone.de/work/?action=facet_selected")

            scrape_permutations()

            # Display the fetched job data
            # st.subheader("Job Recommendations:")
            # for job in fetched_data:
            #     st.write(f"Job URL: {job['URL']}")
            #     st.write(f"Job Description: {job['data']}")

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

def scrapeJobsData():
    return "Hello KG"

if __name__ == "__main__":
    main()
