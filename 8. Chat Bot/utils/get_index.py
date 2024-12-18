from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core import Settings

from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec

import time
from dotenv import load_dotenv
import os

load_dotenv("./.env")
pincone_api = os.getenv('PINECONE_API')

# Set Embedding Model

Settings.embed_model = HuggingFaceEmbedding(
    model_name = 'sentence-transformers/all-MiniLM-L6-v2',
)

def create_index():
  '''
    Create index if necessary else dont create
  
  '''
  index_name = 'geeta'
  pc = Pinecone(api_key=pincone_api)

  # Check existing indexes
  existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

  if index_name not in existing_indexes:
    # Create a new index if it doesn't exist
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

    # Wait until the index is ready
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)

    # Load documents from the directory and create the index
    pinecone_index = pc.Index(index_name)
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    documents = SimpleDirectoryReader("./data/").load_data()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context
    )
    return index

  else:
    pinecone_index = pc.Index(index_name)
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    index = VectorStoreIndex.from_vector_store(
      vector_store=vector_store
    )
    return index