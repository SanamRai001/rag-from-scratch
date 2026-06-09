import pdfplumber
from sentence_transformers import SentenceTransformer

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
print(embeddings)