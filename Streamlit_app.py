import streamlit as st
from langchain_groq import ChatGroq
from io import BytesIO
import PyPDF2
import time
import pandas as pd
import json
import requests

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import aiohttp
import asyncio
import httpx
from concurrent.futures import ThreadPoolExecutor
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Open the page
        await page.goto('https://www.stepstone.de/work/reactjs_javascript_expo-go_react-native_expressjs_git_mongodb_machine-learning_deep-learning_azure-ml-studio_python_tensorflow_keras_pandas_numpy_scikit-learn_matplotlib_ci-cd_agile/in-mainz_de?radius=30&searchOrigin=Resultlist_top-search&q=ReactJS,%20JavaScript,%20Expo%20Go,%20React%20Native,%20ExpressJS,%20Git,%20MongoDB,%20Machine%20Learning,%20Deep%20Learning,%20Azure%20ML%20Studio,%20Python,%20Tensorflow,%20Keras,%20Pandas,%20Numpy,%20Scikit-learn,%20Matplotlib,%20CI%2FCD,%20Agile')

        # Optionally wait for page elements to load
        await page.wait_for_selector("div")

        # Get the page source (HTML)
        content = await page.content()
        
        st.code(content)  # This will print the HTML content
        await browser.close()

def get_cookies_from_selenium(url):
    options = Options()
    options.add_argument("--headless")  # Run in headless mode for faster execution
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)  # Open the website in the browser
        # Perform any required actions like clicking buttons or filling forms

        # Extract cookies
        selenium_cookies = driver.get_cookies()
        return {cookie["name"]: cookie["value"] for cookie in selenium_cookies}
    finally:
        driver.quit()

async def fetch_data(url,cookies):
    timeout = httpx.Timeout(30.0, connect=10.0)  # Increase read and connect timeout
    async with httpx.AsyncClient(verify=False, timeout=timeout) as client:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Connection": "keep-alive",
            }
            response = await client.get(url, headers=headers, cookies=cookies)
            response.raise_for_status()  # Raise an error for HTTP errors
            return response.text  # Get raw HTML source
        except httpx.RequestError as e:
            return f"An error occurred: {e}"

async def fetch_url(driver_url):
    st.write("fetch_url called with: ", driver_url)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(driver_url, ssl=True) as response:
                st.code(f"Status Code: {response.status}")
                content = await response.text()  # or use `response.read()` for binary data
                st.code(content)  # Print the full response content
    except aiohttp.ClientError as e:
        st.code(f"Request failed: {e}")


def scrapeJobsData(applicantSkills, applicantLocation):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=NetworkService")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument('--ignore-ssl-errors=yes')
    options.set_capability("acceptInsecureCerts", True)

    with webdriver.Chrome(options=options) as driver:
        try:
            requests = 0
            driver.implicitly_wait(10)
            driver.get("https://www.stepstone.de/work/?action=facet_selected")
            sleep(randint(8, 10))
            # data = driver.find_elements(by=By.XPATH, value="ccmgt_explicit_accept")
            # return str(data)
            # Wait until the element is clickable
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ccmgt_explicit_accept"))
            )
            # Click the element
            element.click()

            input_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="(job title, skill, or company)"]'))
            )
            driver.execute_script("arguments[0].removeAttribute('readonly');", input_element)
            input_element.send_keys(applicantSkills)
        
            location_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="(city or 5-digit zip code)"]'))
            )
            driver.execute_script("arguments[0].removeAttribute('readonly');", location_input)
            location_input.send_keys(applicantLocation)

            location_input.send_keys(Keys.RETURN)
            st.success("Search button clicked (via send_keys)!")
            time.sleep(5)
            st.code(driver.current_url)
            # st.code(driver.page_source)






        

            # try:
            #     WebDriverWait(driver, 20).until(
            #         EC.presence_of_element_located((By.CLASS_NAME, "res-nehv70"))
            #     )
            #     divs = driver.find_elements(By.XPATH, "//div[contains(@class, 'res-nehv70')]")
            # except TimeoutException:
            #     st.write("Divs with class 'res-nehv70' did not load in time.")
 
            # divs = driver.find_elements(By.CLASS_NAME, "res-nehv70")

            #Get the first div's HTML
            # if divs:
            #     div_html = divs[0].get_attribute("outerHTML")
            #     st.write(div_html)
            # else:
            #     st.write("No div found with class 'res-nehv70'")

            # st.write(len(divs))
            # divs = divs[:6]
            
            # Store the URLs to track if the page is already opened
            # opened_urls = []
            # fetched_data = []
            # Loop through each div, click it and retrieve the new window URL
            # for div in divs:
            #     try:
            #         main_window = driver.current_window_handle  # Store main window handle
            #         # Get the current URL (before switching to the new window)
            #         current_url = driver.current_url
            #         st.write("Current URL:", current_url)

            #         # Ensure the element is clickable before clicking
            #         WebDriverWait(driver, 5).until(EC.element_to_be_clickable(div))
            #         div.click()
            #         # Wait for the new window to load
            #         time.sleep(2)

            #         # Switch to the new window
            #         for handle in driver.window_handles:
            #             if handle != main_window:
            #                 driver.switch_to.window(handle)
            #                 break
            #         # Get the new window URL
            #         new_url = driver.current_url
            #         # Optional: You can extract more details from the new page if needed here
        
            #         # Check if the new URL has been already processed
            #         if new_url in opened_urls:
            #             driver.close()
            #             driver.switch_to.window(main_window)
            #             continue
            #         else:
            #             opened_urls.append(new_url)
            #             st.write("Opened new URL:", new_url)
            #             try:
            #                 articles = driver.find_elements(By.CLASS_NAME, "job-ad-display-147ed8i")
        
            #                 # Ensure there are at least 3 articles
            #                 if len(articles) >= 3:
            #                     # Access the third article (index 2)
            #                     article = articles[2]
        
            #                     # Get the text content (visible text) of the third article
            #                     job_requirements = article.text
        
            #                     # Print the details of the third article
            #                     print(f"Text Content:\n{job_requirements}")
            #                 else:
            #                     print("Less than 3 articles found.")
        
            #             except Exception as e:
            #                 print("Error fetching article content: {e}")
        
            #             fetched_data.append({"URL": new_url, "data": job_requirements})
        
            #         # Close the new window and switch back to the main window
            #         driver.close()
            #         driver.switch_to.window(main_window)
            #         st.write("BACK ON URL:", driver.current_url)
                
            #     except Exception as e:
            #         print(f"Error occurred: {e}")

            current_url = driver.current_url
            driver.quit()
            
            #temporary
            return current_url
            # return opened_urls

        except IndexError:
            pass

# Define Groq API key and model
GROQ_API_KEY = st.secrets.auth_token  # Replace with your actual Groq API key
groq_llama3_llm = ChatGroq(
    temperature=0.4,
    groq_api_key=GROQ_API_KEY,
    model_name="mixtral-8x7b-32768",  # Replace with the desired model
)

async def main():
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

            # fetched_data = scrapeJobsData(applicantSkills, applicantLocation)

            #temporary
            current_url = scrapeJobsData(applicantSkills, applicantLocation)
            st.write("fetching from main:", current_url)
            # Step 1: Use Selenium to fetch cookies
            cookies = get_cookies_from_selenium(current_url)
            st.code(cookies)

            await run()
            
            # data = await fetch_data(current_url,cookies)
            # st.write(data)

            
            
            # Convert the list to a JSON string
            # data_str = json.dumps(fetched_data)
            # st.json(fetched_data)
            st.success("Done")

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

if __name__ == "__main__":
   asyncio.run(main())
