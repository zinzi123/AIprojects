from crewai import Agent, Task, Crew
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileReadTool

# Load environment variables
load_dotenv()

# Fetch the Google API key from environment variables
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Ensure the API key is set in the environment
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Initialize the Gemini Flash model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=GOOGLE_API_KEY
)

# Tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
read_resume = FileReadTool(file_path='./fake_resume.md')

# Agent 1: Researcher
researcher = Agent(
    role="Tech Job Researcher",
    goal="Analyze job postings to extract key qualifications and skills required.",
    tools=[scrape_tool, search_tool],
    verbose=True,
    backstory="You excel at extracting critical information from job postings, helping applicants tailor their applications."
)

# Agent 2: Resume Strategist
resume_strategist = Agent(
    role="Resume Strategist",
    goal="Tailor the resume to highlight relevant skills and experiences for the job.",
    tools=[read_resume],
    verbose=True,
    backstory="You refine resumes to ensure they align perfectly with the job's requirements."
)

# Task 1: Extract Job Requirements
research_task = Task(
    description="Analyze the job posting URL provided ({job_posting_url}) to extract key skills and qualifications required.",
    expected_output="A structured list of job requirements, including necessary skills and experiences.",
    agent=researcher,
    async_execution=True
)

# Task 2: Align Resume with Job Requirements
resume_strategy_task = Task(
    description="Tailor the resume based on the job requirements extracted. Ensure the resume effectively highlights the most relevant skills and experiences.",
    expected_output="An updated resume that effectively highlights the candidate's qualifications relevant to the job.",
    output_file="tailored_resume.md",
    context=[research_task],
    agent=resume_strategist
)

# Crew setup
job_application_crew = Crew(
    agents=[researcher, resume_strategist],
    tasks=[research_task, resume_strategy_task],
    verbose=True
)

# Job application inputs
job_application_inputs = {
    'job_posting_url': 'https://jobs.lever.co/AIFund/6c82e23e-d954-4dd8-a734-c0c2c5ee00f1?lever-origin=applied&lever-source%5B%5D=AI+Fund'
}

# Execute the crew
result = job_application_crew.kickoff(inputs=job_application_inputs)

# Display and save the result
from IPython.display import Markdown, display
display(Markdown("./tailored_resume.md"))
