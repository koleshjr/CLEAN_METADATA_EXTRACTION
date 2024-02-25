import os
import argparse 
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
from src.services.classifier import Classifier
from src.services.extractor import Extractor
from src.models.classifier import ClassificationOutput
from src.models.extractor import ExtractionOutput
from src.helpers.document_loaders import DocumentLoader
from src.helpers.llms import Llms
from src.helpers.config import Config

parser = argparse.ArgumentParser(description='process gazette data')
parser.add_argument('--model_provider', type=str, help='model provider')
parser.add_argument('--model_name', type=str, help='model name')
parser.add_argument('--task_type', type=str, help='either classification or extraction')
args = parser.parse_args()

if __name__ == "__main__":
    llm = Llms(model_provider = args.model_provider, model_name = args.model_name).get_chat_model()

    output_file_path = os.path.join(Config.output_folder, 'combined_pdf.csv')
    if not os.path.exists(output_file_path):
        combined_pdf = pd.DataFrame(columns=['file', 'page', 'text'])

        document_loader = DocumentLoader()
        pages_dict = document_loader.load_and_get_pages(Config.data_folder)


        for file, pages in pages_dict.items():
            for page in pages:
                page_number = page.metadata['page']
                existing_rows = combined_pdf[(combined_pdf['file'] == file) & (combined_pdf['page'] == page_number)]
                if not existing_rows.empty:

                    combined_pdf.loc[(combined_pdf['file'] == file) & (combined_pdf['page'] == page_number), 'text'] += "\n\n" + page.page_content
                else:
                    combined_pdf = combined_pdf.append({'file': file, 'page': page_number, 'text': page.page_content}, ignore_index=True)

            # Save the combined_pdf to CSV after processing all files
            combined_pdf.to_csv(output_file_path, index=False, escapechar='\\')
    else:
        print("Skipping the preprocessing as combined df already exists")

    combined_pdf = pd.read_csv(output_file_path)
    if args.task_type == 'classification':
        classification_results = pd.DataFrame(columns=['file', 'page', 'classification'])
        classifier = Classifier(llm, ClassificationOutput, Config.classification_prompt)
        for row in combined_pdf.itertuples():
            print("Start of prediction")
            pred = classifier.predict(row.text)
            print(pred)
            print("End of prediction")
            # combined_pdf['classification_prediction'] = pred
            # combined_pdf.to_csv(output_file_path, index=False)
            break

    elif args.task_type == 'extraction':
        extraction_results = pd.DataFrame(columns=['file', 'page', 'extraction'])
        extractor = Extractor(llm, ExtractionOutput, Config.extraction_prompt)
        for row in combined_pdf.itertuples():
            pred = extractor.predict(row.text)
            print(pred)
            break
            # combined_pdf['extraction_prediction'] = pred
            # combined_pdf.to_csv(output_file_path, index = False)
    else:
        raise Exception("Invalid task type we currently support only classification and extraction")

