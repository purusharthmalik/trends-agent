from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import FirecrawlSearchTool, FirecrawlCrawlWebsiteTool, MDXSearchTool

load_dotenv()
search_tool = FirecrawlSearchTool(query='Recent tools and technologies in FinTech')
crawl_tool = FirecrawlCrawlWebsiteTool()
reddit_tool = FirecrawlCrawlWebsiteTool(url="https://www.reddit.com/r/fintech/")
md_tool = MDXSearchTool()

scraper_agent = Agent(
    role = "Web Scraper",
    goal = "Provide all the latest tools and technologies in the FinTech market.",
    backstory = """
        An expert in predicting upcoming trends in the financial and technology sector. 
        You always go through the entire internet as well as the subreddit for fintech before providing answers.
    """,
    tools = [search_tool, reddit_tool],
    verbose = True,
    memory = True
)

alignment_agent = Agent(
    role = "Tool alignment verifier",
    goal = "Verify which of the scraped tools are relevant to the space in which NayaOne functions.",
    backstory = """
        You are the marketing head at NayaOne, London. The motto of NayaOne is as follows:
        'We help Financial Institutions grow by leveraging the financial technology ecosystem'.
        You are assigned to look at the tools and technologies extracted by the web scraper and refine the results by aligning them with your company's motto.
    """,
    tools = [crawl_tool, md_tool],
    allow_delegation = False,
    verbose = True
)

scrape = Task(
    description = """
    1. Search for the latest tools and technologies in the fintech market.
    2. Filter 100 top tools and technologies along with a description of the same. (The description should include the company's website, a brief summary of the tool/technology, and future prospects).
    3. Make sure that all the 100 items in the list are relevant to fintech.
    """,
    expected_output = "A list of the top 100 trending/emerging tools and technologies along with their respective descriptions.",
    agent = scraper_agent,
    output_file = 'trends.md'
)

verify = Task(
    description = """
    1. Look at the markdown file created by the web scraper.
    2. Go to the website of the company offering the service.
    3. Check the similarity of the product with NayaOne's motto.
    4. Filter out the unnecessary tools.
    """,
    expected_output = "A list of top 20 emerging tools and technologies and a brief summary about the products and the companies that are offering the products.",
    agent =  alignment_agent,
    output_file = 'final_trends.md'
)

crew = Crew(
    agents = [scraper_agent, alignment_agent],
    tasks = [scrape, verify],
    verbose = True,
    planning = True
)

crew.kickoff()