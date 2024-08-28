import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from sklearn.metrics.pairwise import cosine_similarity
from scrape_me import scrape_linkedin_posts

load_dotenv()
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
# llm = ChatGroq(temprature=0)

topic = 'technology'
topic_embedding = embeddings.embed_query(topic)

THRESHOLD = 0.6

# prompt_template = PromptTemplate(
#     template=f"Is this LinkedIn post relevant to {topic} ? {{post}}",
#     input_variables=['post']
# )
# chain = LLMChain(prompt=prompt_template,
#                  llm=llm)

posts = scrape_linkedin_posts(10000)

for post in posts:
    post_embeddings = embeddings.embed_query(post)
    sim = cosine_similarity([topic_embedding], [post_embeddings])[0][0]

    if sim > THRESHOLD:
        print(f"Relevant Post: {post}")