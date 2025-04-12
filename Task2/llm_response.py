import os
from pathlib import Path
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from schema import Reponse
import glob
from typing import Dict, Any
import pypdf
import logging
import time

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


job_data = """
Role: Backend Engineer,Invest in people and ideas.,
One liner: 10.5 first year,
Location : New York,
Tech Stack : "AWS, Kafka, Kubernetes, PostgreSQL, Python",
Workplace: Hybrid,
Salary: $150k - $180k,
Equitytop 75% tier for companies at their stage,
Valuation : US$ 17M
,https://www.dubapp.com,
Expereince: "5+ years of experience in backend software engineering building micro services using Python, C#/.NET Core or equivalent languages (Java, Python, NodeJS). 
Should have mid-level experience (not junior) at startups that have gone through growth phases.",

Industry: Fintech
"""

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

structured_llm = llm.with_structured_output(Reponse)
messages = [
    (
        "system",
        """You are a helpful assistant that analyz es resumes and extracts structured data. Suitable for name,
         linkedinin url , fit_score and why its good for job. You have to match the candidate profile content with job""",
    ),
    
]
def linkedin_data_matching(linkedin_candidate_data: str): # Simulate , when crawlei
    """
    This function takes a resume text as input and returns structured data
    in the form of a Resume object.
    """
    # Call the LLM with the resume text
    # structured_data = structured_llm(resume_text)
    updated_human_msg = """
            Here is my linkedin profile content of candidate .
            Linkedin Content: {linked_in_content}

            Job agains which candidate needs to be matched.
            {job_data}

    """
    messages.append(("human", updated_human_msg.format(linked_in_content=linkedin_candidate_data, job_data=job_data)))
    response = structured_llm.invoke(messages)
    logger.info(f"Structured data: {response}")
    logger.info(f"Waiting for 1 minute for technical consraints")
    time.sleep(60)
    # Convert the structured data to a Resume object
    # resume = Resume(**structured_data)
    # logger.info(f"Resume data: {resume}")
    
    return response

def get_file_data(dir_path: Path = "Task2/simulate_profiles") -> Dict:
    """
    This function takes a resume text as input and returns structured data
    in the form of a Resume object.
    """
    file_names = glob.glob(os.path.join(dir_path, "*.pdf"))  #Assuming resumes only in pdf format
    if file_names:
        linked_in_data = {}
        logger.info(f"Linkedin profiles found: {file_names}")
        for i,file_path in enumerate(file_names):
            logger.info(f"Linkedin url: {file_path}")
            file_name = file_names[i].split("/")[-1]
            with open(file_path, "rb") as f:
                reader = pypdf.PdfReader(f)
                linkedin_text = ""
                for page in reader.pages:
                    linkedin_text += page.extract_text()
            # Call the LLM with the resume text
            linkedin_data = linkedin_data_matching(linkedin_text)
            linked_in_data[file_name] = linkedin_data
        logger.info(f"Linked_in data: {linked_in_data}")
        return linked_in_data

    else:
        print("No Any Linked in Profile.")
        return {}



if __name__ == "__main__":
    dir_path = Path("simulate_profiles")
    linkedin_data = get_file_data(dir_path)

    print(linkedin_data)
    # resume = get_resume_data(resume_text)
    # print(resume)
    
