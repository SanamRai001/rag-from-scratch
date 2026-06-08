import pdfplumber

with pdfplumber.open("./pdf.pdf") as pdf:
    for index, page in enumerate(pdf.pages):
        print(f"page {index + 1}")
        text = page.extract_text()
        if(text):
            print(text)
        else:
            print("Warning No  text found")