
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# Load environment variables
load_dotenv()

# Read PDF and extract text
pdfreader = PdfReader("../aprilia-manual.pdf")
pdf_text = ""
for i, page in enumerate(pdfreader.pages):
    content = page.extract_text()
    if content:
        pdf_text += content

# Split the text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
text_chunks = text_splitter.split_text(pdf_text)

# Initialize embeddings and vector store
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
doc_array = DocArrayInMemorySearch.from_texts(text_chunks, embedding=embeddings)

# Maintain a message history
message_history = [
    SystemMessage(
        content="You are a helpful assistant trained to use provided context to answer questions accurately."
    )
]


def rag_query(query):
    global message_history

    retrieved_docs = doc_array.similarity_search(
        query, k=3
    )  # Retrieve top 3 relevant chunks

    # Concatenate retrieved chunks for context
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])

    # Add the new question to the message history
    message_history.append(
        HumanMessage(
            content=f"Based on the following extracted content from a document, answer the question:\n\n{context}\n\nQuestion: {query}"
        )
    )

    # Initialize the ChatOpenAI class
    llm = ChatOpenAI(model="gpt-4o")

    # Use the conversation history for the response
    response = llm.invoke(message_history)

    # Add the assistant's response to the message history
    message_history.append(response)

    return response.content  # Return the answer content directly
