from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

# Initialize the Ollama model
llm = Ollama(model="llama2")

# Create a FAISS vector store for the transcript
transcript = "Your YouTube transcript text goes here."
embeddings = OpenAIEmbeddings()
vector_store = FAISS.from_texts([transcript], embeddings)

# Define the retriever and QA chain
retriever = vector_store.as_retriever()
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

# Example interaction
user_input = "What is this video about?"
response = qa({"query": user_input})
print(response)