from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_knowledge_base():

    loader = TextLoader(
        "knowledge_base/company_faq.txt"
    )

    documents = loader.load()

    return documents


def split_documents(documents):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )

    chunks = text_splitter.split_documents(documents)

    return chunks


if __name__ == "__main__":

    documents = load_knowledge_base()

    chunks = split_documents(documents)

    print("Total documents:", len(documents))
    print("Total chunks:", len(chunks))

    print("\nFirst chunk:")
    print(chunks[0].page_content)