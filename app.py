from flask import Flask, request, jsonify, render_template
from src.helper import download_hugging_face_embeddings, process_uploaded_file, text_split
from src.prompt import system_prompt
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from werkzeug.utils import secure_filename
from langchain_google_genai import ChatGoogleGenerativeAI
import traceback
import os

# Environment Configuration
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ["UNSTRUCTURED_HI_RES_MODEL_NAME"] = "yolox"
os.environ["UNSTRUCTURED_HI_RES_MODEL_CACHE_DIR"] = "./model-cache"
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Tesseract-OCR'
os.environ["POPPLER_HOME"] = r'C:\Users\intern\Downloads\Release-24.08.0-0 (1)\poppler-24.08.0\Library'

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB limit
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Pinecone Initialization
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = 'legalbot'

try:
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=384,
            metric='cosine',
            spec=ServerlessSpec(cloud='aws', region='us-east-1')
        )
except Exception as e:
    print(f"Error initializing Pinecone: {str(e)}")
    raise

embeddings = download_hugging_face_embeddings()
docsearch = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embeddings)
retriever = docsearch.as_retriever(search_type='similarity', search_kwargs={"k": 3})

llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash-latest",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.4
)

prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{input}")])
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

@app.route("/")
def home():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message")
        response = rag_chain.invoke({"input": user_input})
        return jsonify({"reply": response['answer']})
    except Exception as e:
        app.logger.error(f"Chat error: {traceback.format_exc()}")
        return jsonify({"error": "Chat processing failed"}), 500

@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        # Save to a temp path only during processing
        filename = secure_filename(file.filename)
        temp_path = os.path.join("/tmp", filename)  # Do not store permanently
        file.save(temp_path)

        # Document processing
        raw_docs = process_uploaded_file(temp_path)
        chunks = text_split(raw_docs)

        # Update Pinecone
        PineconeVectorStore.from_documents(
            documents=chunks,
            embedding=embeddings,
            index_name=index_name
        )

        # Refresh retriever
        global docsearch, rag_chain
        docsearch = PineconeVectorStore.from_existing_index(index_name, embeddings)
        retriever = docsearch.as_retriever(search_kwargs={"k": 3})
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)

        # Delete file after use to avoid confusion
        os.remove(temp_path)

        return jsonify({"message": "File processed successfully"})

    except Exception as e:
        app.logger.error(f"Upload error: {traceback.format_exc()}")
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
