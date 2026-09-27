from langchain_community.document_loaders import PyPDFLoader

pdf_path = "data/raw/criteria_for_passing_exams.pdf"

loader = PyPDFLoader(pdf_path)
documents = loader.load()

print("Number of pages: ",len(documents))

print("\n--- First page ---")
print(documents[0].page_content)

print("\n--- Metadata ---")
print(documents[0].metadata)