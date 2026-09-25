from pathlib import Path
import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
FAISS_DIR = BASE_DIR / "faiss_db"
ENV_FILE = BASE_DIR.parent / ".env"

load_dotenv(ENV_FILE)


# ============================================================
# API KEY
# ============================================================

if not os.getenv("GROQ_API_KEY"):
    raise ValueError(
        "GROQ_API_KEY not found. "
        "Create a .env file in the project root."
    )


# ============================================================
# STRUCTURED RESPONSE
# ============================================================

class AgriculturalResponse(BaseModel):

    disease: str = Field(
        description="The detected or discussed plant disease."
    )

    symptoms: str = Field(
        description="Symptoms supported by the knowledge base."
    )

    causes: str = Field(
        description="Causes supported by the knowledge base."
    )

    treatment: str = Field(
        description="Treatment and management supported by the knowledge base."
    )

    prevention: str = Field(
        description="Prevention measures supported by the knowledge base."
    )


class GeneralAgricultureResponse(BaseModel):
    topic: str = Field(
        description="The agricultural topic being discussed."
    )

    answer: str = Field(
        description="Direct answer to the user's agricultural question."
    )

    recommendations: str = Field(
        description="Useful recommendations supported by the knowledge base."
    )

    precautions: str = Field(
        description="Relevant precautions or limitations supported by the knowledge base."
    )


# ============================================================
# LLM
# ============================================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.3,
    max_tokens=1000,
)


# ============================================================
# STRUCTURED LLM
# ============================================================

disease_llm = llm.with_structured_output(
    AgriculturalResponse
)

general_llm = llm.with_structured_output(
    GeneralAgricultureResponse
)


# ============================================================
# PROMPT
# ============================================================

disease_prompt = ChatPromptTemplate.from_template("""
You are an agricultural plant disease assistant.

Use ONLY the information present in the CONTEXT.

Detected disease:
{disease}

Previous conversation:
{conversation_history}

Current user question:
{question}

CONTEXT:
{context}

Return information using these fields:

- disease
- symptoms
- causes
- treatment
- prevention

Rules:

1. Use the previous conversation only to understand what the user is referring to.
2. Use ONLY the CONTEXT for factual agricultural information.
3. Do not invent information.
4. If information for a field is unavailable, write:
   "Information not available in the knowledge base."
5. Keep the answer concise.
""")

general_prompt = ChatPromptTemplate.from_template("""
You are an agricultural assistant.

Use ONLY the information present in the CONTEXT.

Previous conversation:
{conversation_history}

Current user question:
{question}

CONTEXT:
{context}

Return information using these fields:

- topic
- answer
- recommendations
- precautions

Rules:

1. Use previous conversation to understand follow-up questions.
2. This is a general agricultural question unless a disease is explicitly being discussed.
3. Do not force a disease-related answer.
4. Use ONLY information supported by the CONTEXT.
5. Do not invent information.
6. If information for a field is unavailable, write:
   "Information not available in the knowledge base."
7. Keep the answer concise.
""")

# ============================================================
# CHAIN
# ============================================================

disease_chain = disease_prompt | disease_llm

general_chain = general_prompt | general_llm
# ============================================================
# EMBEDDINGS
# ============================================================

embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3",
    model_kwargs={
        "device": "cpu"
    }
)


# ============================================================
# FAISS
# ============================================================

if not FAISS_DIR.exists():
    raise FileNotFoundError(
        f"FAISS database not found at: {FAISS_DIR}"
    )


vectorstore = FAISS.load_local(
    str(FAISS_DIR),
    embedding_model,
    allow_dangerous_deserialization=True
)


# ============================================================
# RETRIEVER
# ============================================================

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 5
    }
)


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(
    question: str,
    disease: str | None = None,
    conversation_history: str = ""
):

    # --------------------------------------------------------
    # Retrieval query
    # --------------------------------------------------------

    if disease:

        retrieval_query = (
            f"Plant disease: {disease}\n"
            f"Conversation:\n{conversation_history}\n"
            f"Question: {question}"
        )

    else:

        retrieval_query = (
            f"Conversation:\n{conversation_history}\n"
            f"Question: {question}"
        )

    # --------------------------------------------------------
    # Retrieve documents
    # --------------------------------------------------------

    docs = retriever.invoke(
        retrieval_query
    )

    # --------------------------------------------------------
    # Create context
    # --------------------------------------------------------

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    # --------------------------------------------------------
    # Disease response
    # --------------------------------------------------------

    if disease:

        result = disease_chain.invoke({
            "context": context,
            "question": question,
            "disease": disease,
            "conversation_history": conversation_history
        })

    # --------------------------------------------------------
    # General agriculture response
    # --------------------------------------------------------

    else:

        result = general_chain.invoke({
            "context": context,
            "question": question,
            "conversation_history": conversation_history
        })

    # --------------------------------------------------------
    # Return
    # --------------------------------------------------------

    return {
        "context": context,
        "response": result.model_dump()
    }