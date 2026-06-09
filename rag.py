import pdfplumber
from sentence_transformers import SentenceTransformer
import chromadb
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client_ai = genai.Client()

client = chromadb.PersistentClient(path="./my_chorma_db")
collection = client.get_or_create_collection(name="knowledge_base")
def getChunks(text):
    chunks = []
    chunk = text.split(". ")
    current_chunk = ""
    for sentence in chunk:
        if( (len(current_chunk) + len(sentence)) < 300):
            current_chunk += sentence + ". "
        else:  
            chunks.append(current_chunk)
            current_chunk = sentence + ". "
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

with pdfplumber.open("./pdf.pdf") as pdf:
    full_text = ""
    for index, page in enumerate(pdf.pages):
        text = page.extract_text()
        if not text:
            print("Warning No  text found")
            continue
        full_text += text + "\n"

texts = getChunks(full_text)

embeddings = model.encode(texts)
print(f"Number of chunks: {len(texts)}")
print(f"Embeddings shape: {embeddings.shape}")
print(f"First embedding (first 5 numbers): {embeddings[0][:5]}")

ids = [f"id_{i}" for i in range(len(texts))]

if collection.count() == 0:
    collection.add(
        embeddings=embeddings.tolist(),
        documents=texts,
        ids=ids
    )
    print(f"Stored {collection.count()} chunks")
else:
    print(f"Already stored {collection.count()} chunks, skipping")
query_text = "sanam rai"
query_embedding = model.encode(query_text).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)

retrieved_chunks = results['documents'][0]
context = "\n\n".join(retrieved_chunks)

prompt = f"""
You are a helpful assistant. Use the following pieces of context extracted from a PDF to answer the user's question accurately. 
If you do not know the answer based on the context, say "I cannot find that information in the document."

--- CONTEXT ---
{context}

--- QUESTION ---
{query_text}

--- ANSWER ---
"""
response = client_ai.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)
print(response.text)