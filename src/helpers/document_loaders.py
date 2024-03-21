import os 
from langchain_community.document_loaders import PyPDFLoader
class DocumentLoader:
    def __init__(self):
        pass 
    def load_and_get_pages(self, folder_path: str):
        res = {}

        for file in os.listdir(folder_path):
            try:
                if file.endswith('pdf'):
                    filepath = os.path.join(folder_path, file)
                    loader = PyPDFLoader(filepath)
                    pages = loader.load_and_split()
                    res[file] = pages 
            except Exception as e:
                print(f"Error loading file {file} with error {e}")

        return res