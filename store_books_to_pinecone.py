import os
from dotenv import load_dotenv
from src.helper import download_hugging_face_embeddings, process_uploaded_file, text_split
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

# Load environment variables from .env
load_dotenv()

# Settings
DATA_FOLDER = "data"
INDEX_NAME = "legalbot"

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
if INDEX_NAME not in pc.list_indexes().names():
    print(f"Creating Pinecone index '{INDEX_NAME}'...")
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
else:
    print(f"Pinecone index '{INDEX_NAME}' already exists.")

# Load embeddings
embeddings = download_hugging_face_embeddings()

# Ingest documents
print("🔍 Scanning data/ folder for legal documents...")
for file_name in os.listdir(DATA_FOLDER):
    file_path = os.path.join(DATA_FOLDER, file_name)
    if not os.path.isfile(file_path):
        continue
    try:
        print(f"📄 Processing {file_name}...")
        docs = process_uploaded_file(file_path)
        chunks = text_split(docs)

        PineconeVectorStore.from_documents(
            documents=chunks,
            embedding=embeddings,
            index_name=INDEX_NAME
        )

        print(f"✅ Uploaded: {file_name}")

    except Exception as e:
        print(f"❌ Error processing {file_name}: {str(e)}")

print("🎉 All files processed and stored in Pinecone.")
