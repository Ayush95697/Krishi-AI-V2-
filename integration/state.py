from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]
    image_path: str | None
    disease: str | None
    rag_context: str | None
    response: dict | None
