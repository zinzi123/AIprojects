import os
from crewai import Agent, Crew, Process, Task
from crewai_tools import YoutubeChannelSearchTool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch API key and model ID from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # Corrected the environment variable key
model_ID = os.getenv('GPT_MODEL')

# Ensure the API key is set in the environment
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["OPENAI_MODEL_NAME"] = model_ID

# Initialize the YouTube channel search tool
youtube_tool = YoutubeChannelSearchTool(youtube_channel_handle='@techwithzoum')

# Topic Researcher Agent
topic_researcher = Agent(
    role='Topic Researcher',
    goal='Search for relevant videos on the topic {topic} from the provided YouTube channel',
    verbose=True,
    memory=True,
    backstory="Expert in finding and analyzing relevant content from YouTube channels, specializing in AI, Data Science, Machine Learning, and Generative AI topics.",
    tools=[youtube_tool],
    allow_delegation=True
)

# LinkedIn Post Agent
linkedin_post_agent = Agent(
    role='LinkedIn Post Creator',
    goal='Create a concise LinkedIn post summary from the transcription provided by the Topic Researcher.',
    verbose=True,
    memory=True,
    backstory="Expert in crafting engaging LinkedIn posts that summarize complex topics and include trending hashtags for maximum visibility.",
    allow_delegation=False
)

# Twitter Agent
twitter_agent = Agent(
    role='Twitter Content Creator',
    goal='Create a short tweet from the transcription provided by the Topic Researcher that captures key points and insights',
    verbose=True,
    memory=True,
    backstory="Specializes in distilling complex information into concise, impactful tweets that resonate with a tech-savvy audience.",
    allow_delegation=False
)

# Blog Writer Agent
blog_writer = Agent(
    role='Blog Writer',
    goal='Write a comprehensive blog post from the transcription provided by the Topic Researcher, covering all necessary sections',
    verbose=True,
    memory=True,
    backstory="Experienced in creating in-depth, well-structured blog posts that explain technical concepts clearly and engage readers from introduction to conclusion.",
    allow_delegation=False
)

# Define the tasks
research_task = Task(
    description="Identify and analyze videos on the topic {topic} from the specified YouTube channel.",
    expected_output="A complete word-by-word report on the most relevant video found on the topic {topic}.",
    agent=topic_researcher,
    tools=[youtube_tool]
)

blog_writing_task = Task(
    description="""Write a comprehensive blog post based on the transcription provided by the Topic Researcher.
                   The article must include an introduction, step-by-step guides, and a conclusion.
                   The overall content must be about 1200 words long.""",
    expected_output="A markdown-formatted blog post.",
    agent=blog_writer,
    output_file='blog-post.md'
)

linkedin_post_task = Task(
    description="Create a LinkedIn post summarizing the key points from the transcription provided by the Topic Researcher, including relevant hashtags.",
    expected_output="A markdown-formatted LinkedIn post.",
    agent=linkedin_post_agent,
    output_file='linkedin-post.md'
)

twitter_task = Task(
    description="Create a tweet from the transcription provided by the Topic Researcher, including relevant hashtags.",
    expected_output="A markdown-formatted Twitter post.",
    agent=twitter_agent,
    output_file='tweets.md'
)

# Setup the crew with agents and tasks
my_crew = Crew(
    agents=[topic_researcher, linkedin_post_agent, twitter_agent, blog_writer],
    tasks=[research_task, linkedin_post_task, twitter_task, blog_writing_task],
    verbose=True,
    process=Process.sequential,
    memory=True,
    cache=True,
    max_rpm=100,
    share_crew=True
)

# Define the topic of interest and kick off the process
topic_of_interest = 'GPT-3.5 Turbo Fine-tuning and Graphical Interface'
result = my_crew.kickoff(inputs={'topic': topic_of_interest})

print("-----------------------------")
print(result)


