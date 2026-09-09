from app.vector_store import create_vector_store


def search_knowledge(query):

    db = create_vector_store()

    results = db.similarity_search_with_score(
        query,
        k=3
    )

    return results


if __name__ == "__main__":

    query = "How long does refund take?"

    results = search_knowledge(query)


    for result in results:
        print("----------------")
        print(result.page_content)