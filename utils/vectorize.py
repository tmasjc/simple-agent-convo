from chromadb import PersistentClient
from openai import OpenAI
from utils.common import config, logger

# to create embedding
openai_client = OpenAI(api_key=config["OPENAI"]["api_key"])
OUTPUT_DIMENSIONS = 1536

# to store embedding
chroma_client = PersistentClient("./")
chroma_coll = chroma_client.create_collection(
    name="memory_collection", get_or_create=True
)


def do_vectorize(content: str, model: str = "text-embedding-ada-002") -> list:
    """
    Generate a 1536-dimensional embedding vector for the given text content.

    This function uses the OpenAI Embeddings API to convert a text string into a
    high-dimensional vector representation.

    Args:
    content (str): The text content to be vectorized.

    Returns:
    list: A list representing the 1536-dimensional embedding vector of the input text.
    """
    resp = openai_client.embeddings.create(input=content, model=model)
    return resp.data[0].embedding


def initiate_vector(session_id: str, user: str) -> None:
    """
    A convenient wrapper to store vector into collection.

    Mainly to put metadata into vector database. Once `session_destroyed` is triggered, there's no way to pass session metadata to session handler.

    See `collection.add`.
    """
    chroma_coll.add(
        ids=session_id,
        documents="",
        embeddings=[0] * OUTPUT_DIMENSIONS,
        metadatas={"user": user},
    )


def insert_vector(session_id: str, content: str) -> bool:
    """
    A convenient wrapper to update vector into collection.

    See `collection.update`.
    """
    try:
        content_vec = do_vectorize(content)
        logger.trace(content_vec[1:10:])
        chroma_coll.update(ids=session_id, embeddings=content_vec, documents=content)
    except Exception as e:
        logger.debug(e)
        return False
    return True


def find_similar(event: str):
    """
    Recall similar event from vector database.
    """
    resp = chroma_coll.query(
        query_embeddings=do_vectorize(event),
        n_results=1,
        include=["documents", "distances", "metadatas"],
    )
    metadatas = resp.get("metadatas")
    documents = resp.get("documents")
    if metadatas:
        docs = [
            f"Talking to {meta['user']} the other day, {doc[0]}."
            for meta, doc in zip(metadatas[0], documents)
        ]
    else:
        docs = [f"{doc[0]}." for doc in documents]
    logger.trace(docs)
    return "\n".join(docs)


def get_metadata(person: str):
    """
    Recall previous dialogues with someone.
    """
    resp = chroma_coll.get(where={"user": person})
    docs = [_ for _ in resp.get("documents") if _] # remove empty strings
    logger.trace(docs)
    return f"{person} and I talked about " + "...".join(docs)
