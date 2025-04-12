import pandas as pd
import time
import logging
from model import structured_llm, get_resume_data, llm
from schema import Responseq1a, Resume
from crawler import WebCrawler


# Set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

web_crawler = WebCrawler()
def prepare_web_data(url:str, mode: str):
    """
    """
    try:
        docs = web_crawler.get_web_data(url, mode = "crawl")
        logger.info(f"successfully crawled {url}---- {docs}")
        jobs_data = []
        for doc in  docs:
            job_data =  structured_llm.invoke(doc)
            logger.info(f"Job data: {job_data}")
            jobs_data.append(job_data)
        return jobs_data
    except Exception as e:
        logger.info(f"Exception as in prepare web data {e}")
        return None



def preparation():
    """
    Processes resume data and rates them against job roles from the CSV.
    """
    #Scrap only one profile due to api limitation

    job_data = prepare_web_data(url=os.getenv("SYNAPSE_JOB_PAGE"), mode="scrap")

    

    # logger.info(f"Job profiles from CSV data extracted")
    resume_data = get_file_data()

    structured_llm = llm.with_structured_output(Responseq1a)

    system_message = (
        "You are a helpful assistant that analyzes resume data and rates the resume "
        "according to the tech stack, giving a score out of 10. A high score means "
        "the resume is a good match for the job role. The resume data is in the form of a dictionary with keys: "
        "'Role', 'Company', and 'Tech Stack'. The tech stack is a list of technologies. "
        "Response Format:\n"
        "{\n"
        '    "resume_name": "Resume Name",\n'
        '    "fit_score": 8,\n'
        '    "job_matches": ["Company1", "Company2"]\n'
        "}"
    )

    messages = [("system", system_message)]

    candidate_profiling = []
    # resume_data =  {'alonso-alphonsovich-koumba-r.-resume.pdf': Resume(position='Software Engineer', technical_skill='Python, Java, Javascript, Django, React, SQL, PostgreSQL, Bash, ZSH, Git, Lisp, Haskell, Erlang, Scala, HTML, CSS, Java, C, C++, C#, SQL, HTML, CSS, Java, Python, Javascript, gRPC, Protobuf, SQL, Bazel, Lisp, Bash, ZSH, Lucene, Solr, Dojo, script.aculo.us, lighttpd, MySQL, XML, PHP, Apache server', experience='10+ years'), 'Calvin Goah Resume (3).pdf': Resume(position='Senior Software Engineer', technical_skill='TypeScript, JavaScript, Python, Java, PHP, HTML, CSS, SQL, PostgreSQL, C, C++, Elixir, C#, yaml, LATEX, ReactTS, ReactJS, NodeJS, React Native, Amazon Web Services (AWS), OpenAI API, Azure, Git, Scikit-Learn, Linux, Objection ORM, Keras, Praat, Tensorﬂow, PyTorch, Kubernetes, Datadog, Sumo Logic, Bugsnag', experience='10 years'), 'celena.pdf': Resume(position='Software Engineer', technical_skill='Python, TypeScript, ReactJS, JavaScript, C#, .NET, HTML/CSS, Git, Agile (scrum) methodology', experience='4 years')}

    for data in resume_data:
    #     resume_text = data.get("resume_text", "N/A")
    #     resume_name = data.get("resume_name", "Unnamed Resume")
        logger.info(f"Profiling candidate: {data}")

        updated_human_msg = (
            "Here is my Resume data.\n"
            f"Resume Name: {data}\n"
            f"Resume Data : {resume_data[data]}\n"
            f"Job Profiles: {job_data}"
        )
        # logger.info(f"Updated human message: {updated_human_msg}")
        interaction_messages = messages + [("human", updated_human_msg)]

        try:
            response = llm.invoke(interaction_messages)
            logger.info(f"Response: {response.content}")
            candidate_profiling.append(response.content)
        except Exception as e:
            logger.error(f"Error during LLM invocation for  {e}")

        logger.info("Sleeping for 1 minute due to technical constraints...")
        time.sleep(60)

    return candidate_profiling

if __name__ == "__main__":
    profiles = preparation()
    logger.info(f"Final candidate profiling result: {profiles}")

    # You can save the profiling results to CSV here if needed.
