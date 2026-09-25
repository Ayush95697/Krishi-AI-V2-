import json

from langchain_core.messages import AIMessage

from .prediction import disease_Detection
from .generation import generate_answer
from .state import State


def router_request(state: State):

    if state.get("image_path"):
        return "diseaseDetect"

    return "ragChatbot"


def disease_Detector(state: State):
    image_path = state.get("image_path")

    if not image_path:
        return {
            "disease": None
        }

    disease = disease_Detection(image_path)

    return {
        "disease": disease
    }


def ragChatbot(state: State):

    messages = state["messages"]

    # Current user question
    user_query = messages[-1].content

    disease = state.get("disease")

    # ------------------------------------------------
    # Build conversation history
    # ------------------------------------------------

    history = []

    for message in messages[:-1]:

        role = "User" if message.type == "human" else "Assistant"

        history.append(
            f"{role}: {message.content}"
        )

    conversation_history = "\n".join(history)

    # ------------------------------------------------
    # Generate response
    # ------------------------------------------------

    result = generate_answer(
        question=user_query,
        disease=disease,
        conversation_history=conversation_history
    )

    response = result["response"]

    # ------------------------------------------------
    # Store assistant response in messages
    # ------------------------------------------------

    assistant_message = AIMessage(
        content=json.dumps(
            response,
            ensure_ascii=False
        )
    )

    return {
        "messages": [assistant_message],
        "rag_context": result["context"],
        "response": response
    }
