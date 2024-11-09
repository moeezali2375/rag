import os
import sys
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

load_dotenv()

pdfreader = PdfReader("../aprilia-manual.pdf")

pdf_text = ""
for i, page in enumerate(pdfreader.pages):
    content = page.extract_text()
    if content:
        pdf_text += content

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
text_chunks = text_splitter.split_text(pdf_text)

embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
doc_array = DocArrayInMemorySearch.from_texts(text_chunks, embedding=embeddings)


def rag_query(query):
    # Retrieve the most relevant chunks
    retrieved_docs = doc_array.similarity_search(
        query, k=3
    )  # Retrieve top 3 relevant chunks

    # Concatenate retrieved chunks for context using the correct attribute
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])

    # Initialize the ChatOpenAI class
    llm = ChatOpenAI(model="gpt-4o")

    # Prepare the messages with a clarified instruction
    messages = [
        SystemMessage(
            content="You are a helpful assistant trained to use provided context to answer questions accurately."
        ),
        HumanMessage(
            content=f"Based on the following extracted content from a document, answer the question:\n\n{context}\n\nQuestion: {query}"
        ),
    ]

    # Use invoke() to get the response
    response = llm.invoke(messages)
    return response


question = sys.argv[1] if len(sys.argv) > 1 else "What is the document about?"
answer = rag_query(question)
print(answer.content)
