import pdfplumber

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

with pdfplumber.open("./pdf.pdf") as pdf:
    full_text = ""
    for index, page in enumerate(pdf.pages):
        text = page.extract_text()
        full_text += text + "\n"
        if not text:
            print("Warning No  text found")
    texts = getChunks(full_text)
    print(texts)
