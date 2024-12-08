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
from bs4 import BeautifulSoup
import os

os.system("playwright install")
        
async def fetch_data(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        content = await page.content()
        await browser.close()
        return content

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
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ccmgt_explicit_accept"))
            )
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
            st.success("Search button clicked!")
            time.sleep(5)
            st.code(driver.current_url)
            st.write("Please wait, searching for the jobs...")






        

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
    st.write("Disclaimer: This is just a university project developed for learning, kindly visit https://www.stepstone.de/ for searching jobs.")
    uploaded_file = st.file_uploader("Upload your resume", type="pdf")

    if uploaded_file is not None:
        # Extract text from the uploaded PDF
        resume = extract_text_from_pdf(uploaded_file)

        if resume:
            st.success("Resume uploaded successfully.")
            st.text_area("Extracted Text", resume, height=200)

            applicant_info = callLLM(resume)
            applicantSkills, applicantLocation = extract_skills_and_location(applicant_info)

            # Display the extracted skills and location
            st.subheader("Extracted Information:")
            st.write(f"Skills: {applicantSkills}")
            st.write(f"Location: {applicantLocation}")
        
            current_url = scrapeJobsData(applicantSkills, applicantLocation)
            # st.write("fetching from main:", current_url)

            content = await fetch_data(current_url)
            soup = BeautifulSoup(content, 'lxml')
            links = soup.find_all('a', class_='res-1foik6i')
            job_links = [(link['href'], link.text) for link in links]

            if not job_links:
                st.error("Make sure the address in your CV is from Germany!")
            else:
                # Proceed with the normal processing (e.g., displaying jobs)
                for job_url, job_name in job_links:
                    job_url_full = f"https://www.stepstone.de{job_url}"  # Complete the URL if it's relative
                    st.success("Found relevant jobs:")
                    st.write(f"**{job_name}**: [Link]({job_url_full})")
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
