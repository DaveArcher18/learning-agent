import os
from dotenv import load_dotenv

# 1) bring the .env vars into the process
load_dotenv()

# Suppress HuggingFace tokenizers parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# pip install rich  ← needed for the colored terminal UI
from rich.console import Console
from rich.panel import Panel

console = Console()

from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from exa_py import Exa
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from langchain_qdrant import QdrantVectorStore

# 2) LLM – any OpenRouter model you like
llm = ChatOpenAI(
    model="meta-llama/llama-4-maverick:free",   # swap for others any time
    temperature=0.2,                          # a touch of creativity
)

exa = Exa(api_key=os.environ["EXA_API_KEY"])

# Setup local embedding model and Qdrant vector store for RAG
hf_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
client = QdrantClient(url="http://localhost:6333")
# Create the Qdrant collection if it doesn't exist
existing = client.get_collections().collections
if not any(c.name == "research_snippets" for c in existing):
    client.create_collection(
        collection_name="research_snippets",
        vectors_config=qmodels.VectorParams(
            size=384,  # embedding size for all-MiniLM-L6-v2
            distance=qmodels.Distance.COSINE
        )
    )
# Initialize the Qdrant vector store now that the collection exists
vectordb = QdrantVectorStore(
    client=client,
    collection_name="research_snippets",
    embedding=hf_embeddings
)

# Chain for answering questions based on stored research
qa_prompt = PromptTemplate(
    input_variables=["research", "question"],
    template=(
        "You are a research assistant. Use the following research to answer the question.\n\n"
        "Research:\n{research}\n\n"
        "Question: {question}\n"
        "Answer:"
    )
)
from langchain.schema.runnable import RunnableSequence
qa_chain = RunnableSequence(qa_prompt, llm)

# Chain to generate detailed sub-questions for deeper research
question_prompt = PromptTemplate(
    input_variables=["topic"],
    template=(
        "Given the research topic: {topic}, generate 5 detailed research questions "
        "to explore the topic thoroughly. Output as a numbered list, one per line."
    )
)
question_chain = RunnableSequence(question_prompt, llm)

# 6) Simple chat loop
stored_research = ""
stored_topic = None  # remembers the current topic for filtered retrieval

console.print("[bold magenta]🔍  Research Agent ready![/bold magenta]")
console.print("[cyan]Enter 'new_research <topic>' to add research to the database, or ask any question directly. Type 'exit' to quit.[/cyan]")
while True:
    user_input = console.input("[bold blue]> [/bold blue]").strip()
    if user_input.lower() in {"exit", "quit"}:
        break
    if user_input.lower().startswith("new_research"):
        topic = user_input[len("new_research"):].strip()
        # Generate sub-questions to deepen research
        q_result = question_chain.invoke({"topic": topic})
        # Normalize the result to plain text
        if isinstance(q_result, dict):
            q_text = q_result.get("text", "")
        elif hasattr(q_result, "content"):
            q_text = q_result.content
        else:
            q_text = str(q_result)
        questions = [
            line.lstrip("0123456789. ").strip()
            for line in q_text.splitlines() if line.strip()
        ]

        # Perform searches for each generated question
        enriched = []
        for q in questions:
            resp = exa.search_and_contents(
                q,
                use_autoprompt=True,
                num_results=5,
                text=True,
                highlights=True
            )
            items = resp.results
            snippets = []
            for item in items:
                snippet = getattr(item, "text", "") or ""
                url = getattr(item, "url", "") or ""
                snippets.append(f"[{url}] {snippet}")
            enriched.append(f"## {q}\n" + "\n\n".join(snippets[:5]))

        # Store the enriched research for Q&A
        stored_research = "\n\n".join(enriched)
        stored_topic = topic  # keep track of active topic

        # Build per‑snippet metadata
        metas = [{"topic": topic} for _ in enriched]

        # Persist vectors with topic metadata
        vectordb.add_texts(texts=enriched, metadatas=metas)

        # Show current vector count
        info = client.get_collection(collection_name="research_snippets")
        vector_total = info.points_count

        console.print(Panel.fit(
            f"🔖 Stored research for topic: [bold]{topic}[/bold]\n"
            f"💾 Collection now contains [bold green]{vector_total}[/bold green] vectors.", 
            title="System", 
            border_style="blue"
        ))
    else:
        # Ensure database has research
        info = client.get_collection(collection_name="research_snippets")
        if info.points_count == 0:
            console.print("[red]No research in DB. Use 'new_research <topic>' first.[/red]")
            continue

        # Set up retrieval kwargs
        search_kwargs = {"k": 3}  # fetch fewer docs to keep context small
        if stored_topic:
            search_kwargs["filter"] = qmodels.Filter(
                must=[qmodels.FieldCondition(
                    key="topic",
                    match=qmodels.MatchValue(value=stored_topic)
                )]
            )

        retriever = vectordb.as_retriever(search_kwargs=search_kwargs)
        # Invoke retriever with the query string directly (not a dict)
        retrieval = retriever.invoke(user_input)
        if isinstance(retrieval, list):
            docs = retrieval
        elif isinstance(retrieval, dict):
            docs = retrieval.get("documents", []) or []
        else:
            docs = []

        context = "\n\n".join([doc.page_content for doc in docs])
        # Hard cap context length (characters) to stay within model limits
        MAX_CONTEXT_CHARS = 600000
        if len(context) > MAX_CONTEXT_CHARS:
            context = context[:MAX_CONTEXT_CHARS] + "\n\n...[truncated]..."

        result = qa_chain.invoke({"research": context, "question": user_input})
        # Normalize the result to plain text
        if isinstance(result, dict):
            answer_str = result.get("text") or result.get("content") or ""
        elif hasattr(result, "content"):
            answer_str = result.content
        else:
            answer_str = str(result)

        if not answer_str.strip():
            console.print("[red]No answer generated. Try narrowing your query.[/red]")
        else:
            console.print(Panel.fit(answer_str, title="Agent", border_style="green"))