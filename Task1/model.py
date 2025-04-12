import os
from pathlib import Path
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from schema import Resume
import glob
from typing import Dict, Any
import pypdf
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

structured_llm = llm.with_structured_output(Resume)
messages = [
    (
        "system",
        "You are a helpful assistant that analyz es resumes and extracts structured data. Suitable for position, technical expereince",
    ),
    
]
def get_resume_data(resume_text: str) -> Resume:
    """
    This function takes a resume text as input and returns structured data
    in the form of a Resume object.
    """
    # Call the LLM with the resume text
    # structured_data = structured_llm(resume_text)
    updated_human_msg = """
            Here is my resume content .
            Resume: {resume_txt}

    """
    messages.append(("human", updated_human_msg.format(resume_txt=resume_text)))
    response = structured_llm.invoke(messages)
    logger.info(f"Structured data: {response}")
    # Convert the structured data to a Resume object
    # resume = Resume(**structured_data)
    # logger.info(f"Resume data: {resume}")
    
    return response

def get_file_data(dir_path: Path = "Resumes") -> Dict:
    """
    This function takes a resume text as input and returns structured data
    in the form of a Resume object.
    """
    file_names = glob.glob(os.path.join(dir_path, "*.pdf"))  #Assuming resumes only in pdf format
    if file_names:
        resume_data = {}
        logger.info(f"Resume files found: {file_names}")
        for i,file_path in enumerate(file_names):
            logger.info(f"Resume file path: {file_path}")
            file_name = file_names[i].split("/")[-1]
            with open(file_path, "rb") as f:
                reader = pypdf.PdfReader(f)
                resume_text = ""
                for page in reader.pages:
                    resume_text += page.extract_text()
            # Call the LLM with the resume text
            resume_file_data = get_resume_data(resume_text)
            resume_data[file_name] = resume_file_data
        logger.info(f"Resume data: {resume_data}")
        return resume_data

    else:
        print("No resume found in the directory.")
        return {}



if __name__ == "__main__":
    dir_path = Path("Resumes")
    resume_data = get_file_data(dir_path)

    print(resume_data)
    # resume = get_resume_data(resume_text)
    # print(resume)
    
