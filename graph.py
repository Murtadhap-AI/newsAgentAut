# graph.py

from langgraph.graph import StateGraph, END
from agent.collector import collector_agent
from agent.filter_agent import filter_agent
from agent.summarizer_agent import summarizer_agent
from agent.delivery_agent import delivery_agent
from typing import TypedDict, List, Any


class AgentState(TypedDict):
    raw_articles: List[Any]
    filtered_articles: List[Any]
    summarized_articles: List[Any]
    delivery_status: str


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("collector", collector_agent)
    graph.add_node("filter", filter_agent)
    graph.add_node("summarizer", summarizer_agent)
    graph.add_node("delivery", delivery_agent)

    graph.set_entry_point("collector")

    graph.add_edge("collector", "filter")
    graph.add_edge("filter", "summarizer")
    graph.add_edge("summarizer", "delivery")
    graph.add_edge("delivery", END)

    return graph.compile()


news_graph = build_graph()