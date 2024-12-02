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
        
            # Locate the second input element (location input) using XPath by placeholder
            location_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="(city or 5-digit zip code)"]'))
            )
            driver.execute_script("arguments[0].removeAttribute('readonly');", location_input)
            location_input.send_keys(applicantLocation)

            st.code(driver.current_url)
            # st.code(driver.page_source)





            

            # Get all window handles
            window_handles = driver.window_handles
            
            # Assuming you're closing the child window, ensure that the main window is still open
            main_window = driver.current_window_handle  # Store main window handle
            
            # Wait for the element to be clickable
            try:
                # Wait for any iframe or popup to disappear before clicking
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, "iframe[src='https://accounts.google.com/gsi/iframe/select?client_id=199488283516-r84mu91g8mrjk465qrm48cm2int6ah7c.apps.googleusercontent.com&auto_select=true&ux_mode=popup&ui_mode=card&as=a3Jj8hUfSDzdsFJLuC0TZg&is_itp=true&channel_id=c5f755f09decb009361e2375cb6e096b364f96555ef2f55069a490bf49ebda4b&origin=https%3A%2F%2Fwww.stepstone.de&oauth2_auth_url=https%3A%2F%2Faccounts.google.com%2Fo%2Foauth2%2Fv2%2Fauth']"))
                )
            
                # Wait for the search button to be clickable
                search_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@data-at="searchbar-search-button"]'))
                )
            
                # Click the search button
                search_button.click()
                st.write("Search button clicked successfully-1!")
            
            except ElementClickInterceptedException as e:
                # Handle situations where an element is blocked by something else (like a popup or iframe)
                # print(f"Error: Element was not clickable due to overlay or iframe: {e}")
                # Optionally: try using JavaScript to click the element
                driver.execute_script("arguments[0].click();", search_button)
                st.write("Search button clicked successfully-2!")
            
            except TimeoutException as e:
                # Handle timeout if element is not found within the wait time
                print(f"Error: Timeout waiting for the search button: {e}")
                # st.write("Search button COULDN'T be clicked!")

            time.sleep(2)
            
            st.code(driver.current_url)
            
            driver.close()


            # Ensure that we're switching back to the main window
            # If there are multiple windows, make sure the main window handle exists in the list of window handles
            if main_window in window_handles:
                driver.switch_to.window(main_window)
            else:
                print("Main window handle not found.")
            
            # Optionally, capture the current URL and inspect the result
            st.code(driver.current_url)
            # st.code(driver.page_source)



            # try:
            #     response = requests.get("https://www.google.com", verify=False)
            #     st.write(f"Response Status: Done")
            # except Exception as e:
            #     st.write(f"Error accessing URL: {e}")


            # try:
            #     response = requests.get("https://www.stepstone.de/work/llms_langchain_rag_sap-fiori-ui5_fine-tuning_python_machine-learning_deep-learning_reactjs_react-native_javascript_expressjs_mongodb_tensorflow_keras_pandas_numpy_scikit-learn_matplotlib_git_docker_ci-cd_agile/in-walldorf_69190?radius=30&searchOrigin=Resultlist_top-search&q=LLMs,%20LangChain,%20RAG,%20SAP%20Fiori%20Ui5,%20Fine%20tuning,%20Python,%20Machine%20Learning,%20Deep%20Learning,%20ReactJS,%20React%20Native,%20JavaScript,%20ExpressJS,%20MongoDB,%20Tensorflow,%20Keras,%20Pandas,%20Numpy,%20Scikit-learn,%20Matplotlib,%20Git,%20Docker,%20CI%2FCD,%20Agile", verify=False)
            #     st.write(f"Response Status: {response.status_code}")
            # except Exception as e:
            #     st.write(f"Error accessing URL: {e}")

            # try:
            #     WebDriverWait(driver, 10).until(
            #         EC.presence_of_element_located((By.CLASS_NAME, "res-nehv70"))
            #     )
            #     divs = driver.find_elements(By.XPATH, "//div[contains(@class, 'res-nehv70')]")
            # except TimeoutException:
            #     st.write("Divs with class 'res-nehv70' did not load in time.")
                
            # divs = driver.find_elements(By.CLASS_NAME, "res-nehv70")

            # Get the first div's HTML
            # if divs:
            #     div_html = divs[0].get_attribute("outerHTML")
            #     st.write(div_html)
            # else:
            #     st.write("No div found with class 'res-nehv70'")
    
            # divs = divs[:1]
            
            # Store the URLs to track if the page is already opened
            opened_urls = []
            fetched_data = []
            # Loop through each div, click it and retrieve the new window URL
            # for div in divs:
                # try:
                    # Ensure the element is clickable before clicking
                    # WebDriverWait(driver, 5).until(EC.element_to_be_clickable(div))
                    # div.click()
                    # # Wait for the new window to load
                    # time.sleep(2)
                    # # Get the current URL (before switching to the new window)
                    # current_url = driver.current_url
                    # print("Current URL:", current_url)
                    # # Switch to the new window
                    # main_window = driver.current_window_handle  # Store main window handle
                #     for handle in driver.window_handles:
                #         if handle != main_window:
                #             driver.switch_to.window(handle)
                #             break
                #     # Get the new window URL
                #     new_url = driver.current_url
                #     # Optional: You can extract more details from the new page if needed here
        
                #     # Check if the new URL has been already processed
                #     if new_url in opened_urls:
                #         driver.close()
                #         driver.switch_to.window(main_window)
                #         continue
                #     else:
                #         opened_urls.append(new_url)
                #         print("Opened new URL:", new_url)
                #         try:
                #             articles = driver.find_elements(By.CLASS_NAME, "job-ad-display-147ed8i")
        
                #             # Ensure there are at least 3 articles
                #             if len(articles) >= 3:
                #                 # Access the third article (index 2)
                #                 article = articles[2]
        
                #                 # Get the text content (visible text) of the third article
                #                 job_requirements = article.text
        
                #                 # Print the details of the third article
                #                 print(f"Text Content:\n{job_requirements}")
                #             else:
                #                 print("Less than 3 articles found.")
        
                #         except Exception as e:
                #             print("Error fetching article content: {e}")
        
                #         fetched_data.append({"URL": new_url, "data": job_requirements})
        
                #     # Close the new window and switch back to the main window
                #     driver.close()
                #     driver.switch_to.window(main_window)
                #     print("BACK ON URL:", driver.current_url)
                
                # except Exception as e:
                    # print(f"Error occurred: {e}")
        
            # driver.quit()
            return opened_urls

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

            fetched_data = scrapeJobsData(applicantSkills, applicantLocation)
            # Convert the list to a JSON string
            # data_str = json.dumps(fetched_data)
            st.json(fetched_data)
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
    main()
