import os
import google.generativeai as genai
import requests
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
news_api_key = os.getenv("NEWS_API_KEY")

# ✅ Set up Gemini AI Summarizer Agent
summarizer_llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-pro-latest",
    temperature=0.7,
    google_api_key=api_key
)

# ✅ Define AI summarization prompt
summarizer_prompt = PromptTemplate(
    input_variables=["news"],
    template="Summarize the following news article in 3 sentences:\n\n{news}"
)
summarizer_agent = summarizer_prompt | summarizer_llm

# ✅ Fetch latest news using NewsAPI
def fetch_latest_news(topic="technology", country="us", num_articles=3):
    url = f"https://newsapi.org/v2/top-headlines?country={country}&category={topic}&apiKey={news_api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        news_list = [
            {"title": article["title"], "description": article["description"], "url": article["url"]}
            for article in articles[:num_articles]
        ]
        return news_list
    else:
        return f"Error fetching news: {response.json()}"

# ✅ Streamlit UI
st.title("📰 AI News Summarizer")

# **Step 1: User selects news topic**
topics = ["technology", "business", "sports", "health", "science", "entertainment", "general"]
selected_topic = st.selectbox("Select a news category:", topics)

if st.button("Get Latest News"):
    st.write(f"🔍 Fetching latest **{selected_topic}** news...\n")

    # **Step 2: Fetch and display news articles**
    news_articles = fetch_latest_news(topic=selected_topic)

    if isinstance(news_articles, str):  # If an error occurred
        st.error(news_articles)
    else:
        for idx, article in enumerate(news_articles, start=1):
            st.subheader(f"📰 {article['title']}")
            st.write(f"[Read full article]({article['url']})")

            # **Step 3: AI Summarization**
            with st.spinner("Summarizing..."):
                summary = summarizer_agent.invoke({"news": article["description"]})
                summary_text = summary.content if hasattr(summary, "content") else str(summary)

            st.success(f"🤖 AI Summary: {summary_text}")

