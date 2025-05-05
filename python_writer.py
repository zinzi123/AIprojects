from crewai import Agent, Task, Crew

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool

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

# Define the agents
collector = Agent(
    role="Requirements Collector",
    goal="Gather all necessary details for the coding task on {topic}",
    backstory="You are responsible for collecting detailed requirements from the user, including functionality, input/output format, and any specific considerations.",
    allow_delegation=False,
    verbose=True,
    llm=llm  # Use the Gemini model
)

planner = Agent(
    role="Code Planner",
    goal="Plan the structure and components of the code for {topic}",
    backstory="You use the requirements collected to plan the architecture of the solution, including selecting algorithms, data structures, and design patterns.",
    allow_delegation=False,
    verbose=True,
    llm=llm  # Use the Gemini model
)

writer = Agent(
    role="Code Writer",
    goal="Write clean and efficient Python code for {topic}",
    backstory="You write the code based on the plan provided by the Code Planner. You ensure the code is readable, well-documented, and meets the requirements.",
    allow_delegation=False,
    verbose=True,
    llm=llm  # Use the Gemini model
)

reviewer = Agent(
    role="Code Reviewer",
    goal="Review the code to ensure it meets best practices and optimize it",
    backstory="You review the code written by the Code Writer. You check for best practices, potential bugs, and optimize the code for performance.",
    allow_delegation=False,
    verbose=True,
    llm=llm  # Use the Gemini model
)

# Define the tasks
collect_requirements = Task(
    description="Gather detailed information about what the program needs to do and any specific requirements.",
    expected_output="A detailed set of requirements including functional and non-functional aspects.",
    agent=collector,
)

plan_code = Task(
    description="Create a detailed plan for the code structure, including which algorithms and data structures to use.",
    expected_output="A structured code plan, including pseudo-code or flowcharts.",
    agent=planner,
)

write_code = Task(
    description="Write the actual code in the specified programming language based on the provided plan.",
    expected_output="Well-documented and functioning code that fulfills the outlined requirements.",
    agent=writer,
)

review_code = Task(
    description="Review the code for adherence to coding standards and optimize it for performance and readability.",
    expected_output="Reviewed and optimized code, possibly with comments on improvements.",
    agent=reviewer,
)

# Create the crew
crew = Crew(
    agents=[collector, planner, writer, reviewer],
    tasks=[collect_requirements, plan_code, write_code, review_code],
    verbose=True  # Set verbose to a boolean value
)

# Execute the crew with a specific topic
from IPython.display import Markdown

topic = "Implement the fastest sort algorithm in Python for large data sets"
result = crew.kickoff(inputs={"topic": topic})

# Convert the CrewOutput to string (assuming the object can be converted to a meaningful string representation)
output_str = str(result)

# Save the result to a .txt file
with open("generated_code.txt", "w") as file:
    file.write(output_str)

# Optionally save the result to a .csv file (as a single column)
import csv

with open("generated_code.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([output_str])
