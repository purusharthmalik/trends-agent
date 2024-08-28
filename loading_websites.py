import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import FirecrawlSearchTool

load_dotenv()
tool = FirecrawlSearchTool(query='Recent tools and technologies in FinTech')

scraper = Agent(
    role = "Web Scraper",
    goal = "Provide all the latest tools and technologies in the FinTech market.",
    backstory = "An expert in predicting upcoming trends in the financial and technology sector.",
    tools = [tool],
    verbose = True,
    memory = True
)

scrape = Task(
    description = "Scrape all the websites that mention the latest tools and technologies in the fintech market and provide a list of the same.",
    expected_output = "Top 10 tools and technologies and a brief summary about the companies offering those services.",
    agent = scraper,
    output_file = 'trends.md'
)

crew = Crew(
    agents = [scraper],
    tasks = [scrape],
    verbose = True,
    planning = True
)

print(crew.kickoff().raw)