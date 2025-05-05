from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.load_local("../okrs_index", embeddings, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever()

qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=False
)

def ask_with_rag(query):
    return qa_chain.run(query)
