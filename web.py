import streamlit as st
from PIL import Image
from loading_websites import trend_analysis

def update_markdown_file():
    trend_analysis()

def read_markdown_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

icon = Image.open("nayaone_logo.png")
st.set_page_config(page_title="Trend Analysis", 
                   page_icon=icon, 
                   layout="centered")

st.markdown(
    """
    <style>
        .main {
            background-color: #fff;
            color: #4b0082;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        .stButton>button {
            margin: 0 auto;
            display: block;
            background-color: #8e44ad;
            color: white;
            border-radius: 12px;
            padding: 12px 24px;
            border: none;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.3s ease, color 0.3s ease;
        }

        .stButton>button:hover {
            background-color: #f8f0fc;
            color: #4b0082;
        }

        .stButton>button:click {
            background-color: #4b0082;
            color: #f8f0fc;
        }

        .header {
            text-align: center;
            padding: 30px;
            font-size: 28px;
            font-weight: bold;
        }

        .header img {
            max-width: 200px;
            margin-bottom: 20px;
        }

        .markdown-content {
            margin-top: 30px;
            padding: 20px;
            background-color: #f8f0fc;
            border-radius: 10px;
            color: #4b0082;
            font-size: 16px;
            line-height: 1.6;
        }

        .markdown-content h1, .markdown-content h2, .markdown-content h3, .markdown-content h4, .markdown-content h5, .markdown-content h6 {
            color: #4b0082;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.columns(3)[1].image("nayaone_logo.png", )
st.markdown('<div class="header"><h1 style="color: #4b0082;">Latest Trends</h1></div>', unsafe_allow_html=True)

if st.button("Refresh"):
    with st.spinner("We're getting the latest trends for you, this will only take about a minute...Hold tight!"):
        update_markdown_file()

markdown_file_path = 'final_trends.md'
markdown_content = read_markdown_file(markdown_file_path)
st.markdown(f'<div class="markdown-content">{markdown_content}</div>', unsafe_allow_html=True)