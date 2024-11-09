from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

loader = PyPDFLoader("aprilia-manual.pdf")
documents = loader.load()

embeddings = OpenAIEmbeddings()

vector_store = Chroma.from_documents(documents, embeddings)

llm = ChatOpenAI(model_name="gpt-4", openai_api_key=api_key)

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm, retriever=vector_store.as_retriever()
)

query = "What is the main topic of the document?"
response = qa_chain({"question": query, "chat_history": []})

print(response["answer"])
