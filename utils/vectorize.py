from chromadb import PersistentClient
from openai import OpenAI
from utils.common import config, logger

# to create embedding
openai_client = OpenAI(api_key=config["OPENAI"]["api_key"])

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

def insert_vector(session_id: str, content: str, metadatas: dict = None) -> bool:
    """
    A convenient wrapper to store vector into collection. 
    
    See `collection.add`.
    """
    try:
        chroma_coll.add(
            ids=session_id,
            embeddings=do_vectorize(content),
            documents=content,
            metadatas=metadatas
        )
    except Exception as e:
        logger.debug(e)
        return False
    return True
