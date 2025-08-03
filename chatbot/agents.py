import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph
from langchain_groq import ChatGroq
from typing import TypedDict

load_dotenv()

llm = ChatGroq(
    model="llama3-8b-8192",
    api_key=os.getenv("GROQ_API_KEY")
)

class ChatState(TypedDict):
    input: str
    history: str
    output: str

def chat_func(state: ChatState) -> ChatState:
    history = state['history']
    user_input = state['input']
    prompt = f"{history}\nUser: {user_input}\nAI:"
    response = llm.invoke(prompt)
    updated_history = history + f"\nUser: {user_input}\nAI: {response.content}"
    return {
        "input": user_input,
        "history": updated_history,
        "output": response.content
    }

def create_agent():
    builder = StateGraph(ChatState)
    builder.add_node("chat", chat_func)
    builder.set_entry_point("chat")
    builder.set_finish_point("chat")
    return builder.compile()
agent_executor = create_agent()