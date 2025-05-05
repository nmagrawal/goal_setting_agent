from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import time

def build_index(pdf_path="Measure-What-Matters-John-Doerr.pdf"):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()
    batch_size = 20
    faiss_index = None

    print(f"📄 Total chunks: {len(chunks)}")

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        print(f"🔄 Embedding batch {i//batch_size + 1}/{(len(chunks) + batch_size - 1)//batch_size}...")

        try:
            if faiss_index is None:
                faiss_index = FAISS.from_documents(batch, embeddings)
            else:
                new_index = FAISS.from_documents(batch, embeddings)
                faiss_index.merge_from(new_index)
        except Exception as e:
            print(f"❌ Batch {i} failed: {e}")
        time.sleep(1.5)  # prevent hitting TPM limits

    if faiss_index:
        faiss_index.save_local("okrs_index")
        print("✅ Saved FAISS index to 'okrs_index'")
    else:
        print("❌ No index was created")

if __name__ == "__main__":
    build_index()
