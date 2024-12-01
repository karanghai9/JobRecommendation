import streamlit as st
from langchain_groq import ChatGroq
from io import BytesIO
import PyPDF2
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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
    @st.cache_resource
    def get_driver():
        return webdriver.Chrome(
            service=Service(
                ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            ),
            options=options,
        )

    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")

    driver = get_driver()
    driver.get("https://www.stepstone.de/work/?action=facet_selected")

    # Accept cookies
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ccmgt_explicit_accept"))
        ).click()
        print("Clicked on Accept Cookies")
    except Exception as e:
        print(f"Could not click on 'Accept Cookies': {e}")

    # Wait for the job title input field and location input field
    try:
        input_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'input[placeholder="(job title, skill, or company)"]')
            )
        )
        driver.execute_script("arguments[0].removeAttribute('readonly');", input_element)
        input_element.send_keys(applicantSkills)

        location_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'input[placeholder="(city or 5-digit zip code)"]')
            )
        )
        driver.execute_script("arguments[0].removeAttribute('readonly');", location_input)
        location_input.send_keys(applicantLocation)

        # Locate and click the search button
        search_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-at="searchbar-search-button"]'))
        )
        search_button.click()
        print("Search button clicked successfully!")

    except Exception as e:
        print(f"Error interacting with elements: {e}")
        driver.quit()
        return []

    # Continue with scraping logic...
    time.sleep(2)
    # Ensure the job listings are loaded
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "res-nehv70"))
    )
    
    # Fetch job listings
    divs = driver.find_elements(By.CLASS_NAME, "res-nehv70")
    divs = divs[:10]  # Limit to first 10 listings

    fetched_data = []
    for div in divs:
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable(div)).click()
            time.sleep(2)  # Wait for the new page to load
            
            # Retrieve job details
            job_requirements = driver.find_element(By.CLASS_NAME, "job-ad-display-147ed8i").text
            fetched_data.append({"URL": driver.current_url, "data": job_requirements})
            driver.back()  # Go back to the search results

        except Exception as e:
            print(f"Error occurred: {e}")

    driver.quit()
    return fetched_data

if __name__ == "__main__":
    main()
