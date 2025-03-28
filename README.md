# Law-Chatbot

### Steps:

### Step 1:
1) Clone the repository
https://github.com/sameergit0/Law-Chatbot.git

### Step 2:
2) Create and activate virtual environment
python -m venv lawbot
.\lawbot\Scripts\activate

### Step 3:
3) Install the requirements
pip install -r requirements.txt


### Step 4:
4) Install embedding model from hugging face
sentence-transformers/all-MiniLM-L6-v2 (This model will generate 384 dimensional embedding)

### Step 5:
5) Create pinecone account to store vector embeddings (here we set 384 dimensions)

### Step 6:
6) Create groq account to use llm (we are using llama3-8b-8192 model)