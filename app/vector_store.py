from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from app.rag import load_knowledge_base, split_documents


def create_vector_store():

    documents = load_knowledge_base()

    chunks = split_documents(documents)


    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


    vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="database/chroma",
    collection_name="company_faq"
)


    return vector_store



if __name__ == "__main__":

    db = create_vector_store()


    query = "I want my money back"


    results = db.similarity_search(
        query,
        k=2
    )


    for result in results:
        print("----------------")
        print(result.page_content)