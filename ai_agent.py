import os
import google.generativeai as genai
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# ✅ Use the correct Gemini model
llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-pro-latest",  # 🔹 Use a valid model from your list
    temperature=0.7,
    google_api_key=api_key
)

# Define a simple prompt
prompt = PromptTemplate(
    input_variables=["question"],
    template="You are an AI assistant called robot with ability to understand the emotion. Answer the question: {question}"
)

# ✅ Use LangChain’s recommended format
agent = prompt | llm

# Function to interact with the AI agent
def chat_with_ai():
    print("robot: Hello! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("robot: Goodbye!")
            break
        
        response = agent.invoke({"question": user_input})  # Get structured response
        response_text = response.content if hasattr(response, "content") else str(response)  # ✅ Extract text only
        
        print(f"robot: {response_text}")  # ✅ Print only the AI's message

# Run the AI Agent
if __name__ == "__main__":
    chat_with_ai()
