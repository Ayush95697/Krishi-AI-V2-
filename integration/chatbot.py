from langchain_core.messages import HumanMessage

from .graph import build_app


class PlantRAGChatbot:
    """
    Reusable wrapper around the LangGraph app.

    Usage:
        bot = PlantRAGChatbot()

        result = bot.ask(
            "What disease does this plant have and how should I treat it?",
            thread_id="session-1",
            image_path=r"D:\\rag chatbot\\...\\0.jpeg"
        )
        print(result["response"])

        # Follow-up in the same session — no need to resend image_path/disease,
        # the checkpointer carries them forward automatically.
        result = bot.ask("isse kaise theek kare?", thread_id="session-1")
        print(result["response"])
    """

    def __init__(self, checkpointer=None):
        self.app = build_app(checkpointer=checkpointer)

    def ask(self, question: str, thread_id: str, image_path: str | None = None):
        state = {
            "messages": [HumanMessage(content=question)],
            "image_path": image_path,
            "disease": None,
            "rag_context": None,
            "response": None
        }

        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        return self.app.invoke(state, config=config)

    def reset(self, thread_id: str):
        """
        Starts a fresh conversation on this thread_id by using a new
        checkpoint namespace. Simplest approach: have the caller use a
        new thread_id for a new session.
        """
        raise NotImplementedError(
            "Use a new thread_id to start a fresh session; "
            "MemorySaver keys conversation state by thread_id."
        )
