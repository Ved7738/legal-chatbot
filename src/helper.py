from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, UnstructuredFileLoader
import logging

def load_pdf_file(data):
    try:
        loader = DirectoryLoader(path=data, glob="*.pdf", loader_cls=PyPDFLoader)
        return loader.load()
    except Exception as e:
        logging.error(f"PDF load error: {str(e)}")
        raise

def text_split(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20,
        separators=["\n\n", "\n", " ", ""]
    )
    return splitter.split_documents(documents)

def download_hugging_face_embeddings():
    return HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2',
        model_kwargs={'device': 'cpu'}
    )

def clean_metadata(documents):
    """Strip unsupported Pinecone metadata fields like dicts, lists, None."""
    cleaned = []
    for doc in documents:
        meta = {}
        for key, value in doc.metadata.items():
            if isinstance(value, (str, int, float, bool)) or (
                isinstance(value, list) and all(isinstance(i, str) for i in value)
            ):
                meta[key] = value
        doc.metadata = meta
        cleaned.append(doc)
    return cleaned

def process_uploaded_file(file_path):
    try:
        loader = UnstructuredFileLoader(file_path)
        documents = loader.load()
        return clean_metadata(documents)  # Sanitize before returning
    except Exception as e:
        raise RuntimeError(f"Failed to process file: {str(e)}")
