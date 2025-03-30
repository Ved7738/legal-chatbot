# ⚖️ Law-Chatbot

**Law-Chatbot** is a legal advisor AI model designed to answer law-related queries using vector embeddings and an LLM model. This project uses **Pinecone** for vector storage and **Groq's llama3-8b-8192** model for processing responses.

---

## 🚀 **Steps to Set Up and Run**

### ✅ **Step 1: Clone the Repository**
Clone the project from GitHub:
```bash
git clone https://github.com/sameergit0/Law-Chatbot.git
Move into the project directory:
cd Law-Chatbot

✅ Step 2: Create and Activate a Virtual Environment
Create a virtual environment:
python -m venv lawbot

Activate the environment:
Windows:
.\lawbot\Scripts\activate

Linux/macOS:
source lawbot/bin/activate

✅ Step 3: Install Requirements
Install the project dependencies:
pip install -e .

✅ Step 4: Install Sentence Transformer Model
Download the Hugging Face embedding model:
sentence-transformers/all-MiniLM-L6-v2
This model generates 384-dimensional embeddings.

✅ Step 5: Set Up Pinecone for Vector Storage
Go to Pinecone and create an account.
Create a new index with the following configuration:
Dimensions: 384
Metric: cosine
Add your Pinecone API key to the environment variables or config file.

✅ Step 6: Create a Groq Account
Go to Groq and create an account.
Use the llama3-8b-8192 model in your application.
Add your Groq API key to the environment variables or config file.

✅ Step 7: Download the Dataset
Download the dataset from Google Drive:
📂 Dataset Link:
https://drive.google.com/drive/folders/1iwhpGZ__NUcSC1eDyoslQOC5SyJO59-r?usp=drive_link
Place the dataset files into the /data directory.
Ensure that your application reads and processes the dataset correctly.

✅ Step 8: Run the Application
Start the chatbot by running the following command:
python app.py

🛠️ Technologies Used
🐍 Python: Backend and chatbot logic.

🗄️ Pinecone: Vector storage for efficient similarity search.

🤖 Groq: LLM for generating legal responses.

🔥 Hugging Face: Embedding model for creating vector representations.

📌 Contributing
Feel free to submit pull requests or report issues. Contributions are welcome!

⚙️ License
This project is licensed under the MIT License.