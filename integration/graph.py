from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from .state import State
from .nodes import router_request, disease_Detector, ragChatbot


def build_app(checkpointer=None):
    """
    Builds and compiles the LangGraph app.

    Pass a checkpointer (e.g. a Postgres/Sqlite saver) for production use.
    Defaults to an in-memory MemorySaver, matching the notebook's setup.
    """

    graph = StateGraph(State)

    # Nodes
    graph.add_node("diseaseDetect", disease_Detector)
    graph.add_node("ragChatbot", ragChatbot)

    # Edges
    graph.add_conditional_edges(
        START,
        router_request,
        {
            "diseaseDetect": "diseaseDetect",
            "ragChatbot": "ragChatbot"
        }
    )

    graph.add_edge("diseaseDetect", "ragChatbot")
    graph.add_edge("ragChatbot", END)

    if checkpointer is None:
        checkpointer = MemorySaver()

    return graph.compile(checkpointer=checkpointer)
