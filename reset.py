from utils.database import engine, metadata, TABLE_NAME
from utils.vectorize import chroma_client, COLLECTION_NAME

passcode = input("Please input passcode <wizard_bob>:\n")

if passcode == "wizard_bob":
    # reset memory database
    metadata.reflect(bind=engine, only=[TABLE_NAME])
    table = metadata.tables[TABLE_NAME]
    table.drop(engine)

    # reset vector database
    chroma_client.delete_collection(COLLECTION_NAME)

print("Reset complete")
