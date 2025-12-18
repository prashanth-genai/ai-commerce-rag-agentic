from langgraph.graph import StateGraph
from agent_service.agents.intent_agent import detect_intent
from agent_service.agents.order_agent import handle_order

def intent_node(state):
    state["intent"] = detect_intent(state["query"])
    return state

def order_node(state):
    state["result"] = handle_order(state["user_id"])
    return state

graph = StateGraph(dict)
graph.add_node("intent", intent_node)
graph.add_node("order", order_node)

graph.set_entry_point("intent")
graph.add_edge("intent", "order")

agent_executor = graph.compile()

# multiagent
"""
agent_graph.py
---------------
Multi-agent workflow orchestrated using LangGraph.

Agents included:
✔ Catalog Agent
✔ Order Agent
✔ Return Agent
✔ Cancel Agent
✔ Pricing Agent (stub)
✔ Intent Classifier
✔ RAG Retriever

The graph determines which agent to call based on user intent
and coordinates multi-step reasoning.
"""

from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

# Import agents
from agents.catalog_agent import handle_catalog_query
from agents.order_agent import handle_order_query
from agents.return_agent import handle_return_request
from agents.cancel_agent import handle_order_cancellation

# LLM for intent detection
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# -------------------------------------------
# Define Shared State
# -------------------------------------------
class AgentState(Dict):
    """
    Holds conversation state for multi-agent orchestration.
    """
    user_query: str
    intent: str | None
    result: Dict[str, Any] | None


# -------------------------------------------
# Intent Classification Node
# -------------------------------------------
def classify_intent(state: AgentState):
    """
    Determine intent using LLM.
    """

    prompt = f"""
    User Query: "{state['user_query']}"

    Identify the intent from categories:
    - catalog_search
    - order_status
    - return_request
    - order_cancellation
    - pricing_query
    - unknown

    Provide only the intent keyword.
    """

    intent = llm.invoke(prompt).content.strip()

    state["intent"] = intent
    return state


# -------------------------------------------
# Route Nodes (Decision Layer)
# -------------------------------------------
def route_intent(state: AgentState):
    """
    Route to the correct agent based on intent.
    """
    return state["intent"]


# -------------------------------------------
# Agent Nodes
# -------------------------------------------
def catalog_agent(state: AgentState):
    state["result"] = handle_catalog_query(state["user_query"])
    return state


def order_agent(state: AgentState):
    order_id = extract_order_id(state["user_query"])
    state["result"] = handle_order_query(order_id)
    return state


def return_agent(state: AgentState):
    order_id = extract_order_id(state["user_query"])
    sku = extract_sku(state["user_query"])
    state["result"] = handle_return_request(order_id, sku)
    return state


def cancel_agent(state: AgentState):
    order_id = extract_order_id(state["user_query"])
    state["result"] = handle_order_cancellation(order_id)
    return state


def unknown_handler(state: AgentState):
    state["result"] = {
        "message": "I'm sorry, I couldn't understand your request."
    }
    return state


# -------------------------------------------
# Helper Extraction Functions (Simplified)
# -------------------------------------------
def extract_order_id(text: str) -> str:
    """
    Extract order ID from user text (dummy logic).
    """
    import re
    match = re.search(r"ORD\d+", text.upper())
    return match.group(0) if match else "ORD1001"


def extract_sku(text: str) -> str:
    """
    Extract SKU from user text (dummy logic).
    """
    import re
    match = re.search(r"SKU\d+", text.upper())
    return match.group(0) if match else "SKU1001"


# -------------------------------------------
# Build Agent Graph
# -------------------------------------------
def build_agent_graph():
    workflow = StateGraph(AgentState)

    # Nodes
    workflow.add_node("classify_intent", classify_intent)
    workflow.add_node("catalog_agent", catalog_agent)
    workflow.add_node("order_agent", order_agent)
    workflow.add_node("return_agent", return_agent)
    workflow.add_node("cancel_agent", cancel_agent)
    workflow.add_node("unknown", unknown_handler)

    # Entry Point
    workflow.set_entry_point("classify_intent")

    # Router
    workflow.add_conditional_edges(
        "classify_intent",
        route_intent,
        {
            "catalog_search": "catalog_agent",
            "order_status": "order_agent",
            "return_request": "return_agent",
            "order_cancellation": "cancel_agent",
            "pricing_query": "catalog_agent",  # placeholder
            "unknown": "unknown",
        }
    )

    # End all paths
    workflow.add_edge("catalog_agent", END)
    workflow.add_edge("order_agent", END)
    workflow.add_edge("return_agent", END)
    workflow.add_edge("cancel_agent", END)
    workflow.add_edge("unknown", END)

    return workflow.compile()


# -------------------------------------------
# Example Run
# -------------------------------------------
if __name__ == "__main__":
    graph = build_agent_graph()

    user_query = "I want to cancel my order ORD9912"
    response = graph.invoke({"user_query": user_query})

    print("\n===== AGENT GRAPH RESPONSE =====")
    print(response["result"])


