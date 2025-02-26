import os
import google.generativeai as genai
import requests
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
news_api_key = os.getenv("NEWS_API_KEY")  # For fetching news

# ✅ Set up the AI summarizer agent (Gemini)
summarizer_llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-pro-latest",
    temperature=0.7,
    google_api_key=api_key
)

# ✅ Define a simple summarization prompt
summarizer_prompt = PromptTemplate(
    input_variables=["news"],
    template="Summarize the following news article in 3 sentences:\n\n{news}"
)

# ✅ Summarizer Agent (LangChain)
summarizer_agent = summarizer_prompt | summarizer_llm

# ✅ News Fetcher Agent: Uses NewsAPI to get latest news
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

# ✅ AI Team Function: Fetch & Summarize News
def news_ai_team():
    print("Welcome to the AI News Team! Type a topic (e.g., 'technology', 'sports', 'business') or 'exit' to quit.")
    
    while True:
        topic = input("Enter a news topic: ")
        if topic.lower() == "exit":
            print("AI News Team: Goodbye!")
            break

        print(f"\n🔍 Fetching latest {topic} news...\n")
        news_articles = fetch_latest_news(topic=topic)

        if isinstance(news_articles, str):  # If an error occurred
            print(news_articles)
            continue

        for idx, article in enumerate(news_articles, start=1):
            print(f"\n📰 **News {idx}: {article['title']}**")
            print(f"🔗 Read more: {article['url']}\n")

            # ✅ Summarize the news using AI
            summary = summarizer_agent.invoke({"news": article["description"]})
            summary_text = summary.content if hasattr(summary, "content") else str(summary)

            print(f"🤖 AI Summary: {summary_text}\n")

# ✅ Run AI News Team
if __name__ == "__main__":
    news_ai_team()
