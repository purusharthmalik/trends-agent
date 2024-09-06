import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import FirecrawlScrapeWebsiteTool, FirecrawlCrawlWebsiteTool, MDXSearchTool

load_dotenv()
def trend_analysis():
    crawl_tool = FirecrawlCrawlWebsiteTool()
    scrape_tool = FirecrawlScrapeWebsiteTool()
    md_tool = MDXSearchTool()

    scraper_agent = Agent(
        role = "Web Scraper",
        goal = "Provide a list of 20 latest tools and technologies in the FinTech market for the banking sector.",
        backstory = """
            An expert in predicting upcoming trends in the financial and technology sector.
            You always look at articles only from the past week.
            You are known for doing the job in an efficient manner.
            You do not scrape unless you are sure an article is relevant.
            You check the relevance by looking at the title of the article.
            You have a job to monitor the following pages:
            1 - https://fintech.global/category/fintech-news/fintech-industry-news/
            2 - https://fintechos.com/blog/
            3 - https://fintechmagazine.com/banking?
        """,
        tools = [scrape_tool, crawl_tool],
        verbose = True,
        memory = True
    )
    # 3 - https://news.google.com/search?q=fintech+in+banks

    alignment_agent = Agent(
        role = "Tool alignment verifier",
        goal = "Verify which of the scraped tools are relevant to the space in which NayaOne functions.",
        backstory = """
            You are the marketing head at NayaOne, London. The motto of NayaOne is as follows:
            'We help Financial Institutions grow by leveraging the financial technology ecosystem'.
            You are assigned to look at the tools and technologies extracted by the web scraper and refine the results by aligning them with your company's motto.
            The results are stored in a file called 'trends.md'.
        """,
        tools = [md_tool],
        allow_delegation = False,
        verbose = True
    )

    scrape = Task(
        description = """
        1. Search for the latest tools and technologies in the fintech market for the banking sector.
        2. Filter 20 top tools and technologies along with a description of the same. (The description should include the product's website, a brief summary of the tool/technology, and future prospects).
        3. Make sure that all the 20 items in the list are relevant to fintech in the banking sector.
        """,
        expected_output = "A list of the top 20 trending/emerging tools and technologies along with their respective descriptions.",
        agent = scraper_agent,
        output_file = 'trends.md'
    )

    verify = Task(
        description = """
        1. Look at the markdown file created by the web scraper.
        2. Go to the website of the product.
        3. Check the similarity of the product with NayaOne's motto.
        4. Filter out the unnecessary tools.
        5. Before writing the final list to the markdown file, write the following sentence in the beginning: 'Here's the top 10 trends that have emergred in the fintech space for financial institutions in the past week,'
        """,
        expected_output = "A list of top 10 emerging tools and technologies and a brief summary about the products and the companies that are offering the products.",
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