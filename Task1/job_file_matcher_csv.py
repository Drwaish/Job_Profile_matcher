import pandas as pd
import time
import logging
from model import llm, get_file_data
from schema import Responseq1a, Resume

# Set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_csv_file(csv_file_path):
    """
    Reads a CSV file and returns role, company, and tech stack lists.
    """
    try:
        df = pd.read_csv(csv_file_path)
        required_columns = ['Role', 'Company', 'Tech Stack']
        if all(col in df.columns for col in required_columns):
            role_list = df['Role'].tolist()
            company_list = df['Company'].tolist()
            tech_stack_list = df['Tech Stack'].tolist()
            return role_list, company_list, tech_stack_list
        else:
            missing = [col for col in required_columns if col not in df.columns]
            logger.error(f"Missing columns in CSV: {missing}")
            return [], [], []
    except Exception as e:
        logger.error(f"Error reading CSV file: {e}")
        return [], [], []

def preparation():
    """
    Processes resume data and rates them against job roles from the CSV.
    """
    logger.info("Reading CSV file...")
    role, company, tech_stack = read_csv_file(csv_file_path="data/ParaformJobs.csv")

    df_data = []
    for i in range(len(role)):
        df_data.append({
            "Role": role[i],
            "Company": company[i],
            "Tech Stack": tech_stack[i]
        })

    logger.info(f"Job profiles from CSV data extracted")
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
            f"Job Profiles: {df_data}"
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
