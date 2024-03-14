import os
import argparse 
import pandas as pd
import warnings
import re
warnings.filterwarnings("ignore")
from src.services.classifier import Classifier
from src.services.extractor import Extractor
from src.models.classifier import ClassificationOutput
from src.models.extractor import ExtractionOutput
from src.helpers.document_loaders import DocumentLoader
from src.helpers.llms import Llms
from src.helpers.config import Config
from src.helpers.utils import transform_submission

parser = argparse.ArgumentParser(description='process gazette data')
parser.add_argument('--model_provider', type=str, help='model provider')
parser.add_argument('--model_name', type=str, help='model name')
parser.add_argument('--task_type', type=str, help='either classification or extraction')
parser.add_argument('--experiment', type=str, help ='Experiment number')
args = parser.parse_args()

def remove_unwanted(text):
    if text is None or not text.strip():
        return ''

    pattern = re.compile(r'\\ufdd0|[\x00-\x08\x0B\x0C\x0E-\x1F]+|[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]+', flags=re.UNICODE)
    clean_text = pattern.sub('', text)
    clean_text = clean_text.replace('“A”', '"A"')
    clean_text = clean_text.replace('“B”', '"B"')

    return clean_text

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

                    combined_pdf.loc[(combined_pdf['file'] == file) & (combined_pdf['page'] == page_number), 'text'] += "\n\n" + remove_unwanted(page.page_content)
                else:
                    combined_pdf = combined_pdf.append({'file': file, 'page': page_number, 'text': remove_unwanted(page.page_content)}, ignore_index=True)

            # Save the combined_pdf to CSV after processing all files
            combined_pdf.to_csv(output_file_path, index=False, escapechar='\\')
            
    else:
        print("Skipping the preprocessing as combined df already exists")

    combined_pdf = pd.read_csv(output_file_path)
    if args.task_type == 'classification':
        output_file_path = os.path.join(Config.output_folder, 'classified_pdf.csv')
        classifier = Classifier(llm, ClassificationOutput, Config.classification_prompt)
        max_retries = 3 

        for row_index, row in combined_pdf.iterrows():
            retries = 0
            while retries < max_retries:
                try:
                    if row['page'] == 0:
                        combined_pdf.at[row_index, 'classification_prediction'] = False
                        break
                    else:
                        pred = classifier.predict(row['text'])
                        print(row['page'], pred["answer"])
                        combined_pdf.at[row_index, 'classification_prediction'] = pred["answer"]
                        combined_pdf.to_csv(output_file_path, index=False)
                        break  # Exit the retry loop if successful
                except Exception as e:
                    print(f"An exception occurred: {e}")
                    retries += 1
                    print(f"Retrying classification for row {row_index}")
            else:
                print(f"Maximum retries exceeded for row {row_index}. Setting classification_prediction to False.")
                combined_pdf.at[row_index, 'classification_prediction'] = False

        # Save the updated combined_pdf to CSV after processing all rows
        combined_pdf.to_csv(output_file_path, index=False)
        print("Finished classifaction")
                

    elif args.task_type == 'extraction':
        classified_path = "src\output\classified_pdf.csv"
        classified_pdf = pd.read_csv(classified_path)
        output_file_path = os.path.join(Config.output_folder, 'extracted_pdf.csv')
        extractor = Extractor(llm, ExtractionOutput, Config.extraction_prompt)
        max_retries = 3 

        for row_index, row in classified_pdf.iterrows():
            retries = 0
            while retries < max_retries:
                try:
                    if row['classification_prediction'] == False:
                        classified_pdf.at[row_index, 'extraction_prediction'] = ""
                        break
                    else:
                        pred = extractor.predict(row['text'])
                        print(row['page'], pred["result"])
                        classified_pdf.at[row_index, 'extraction_prediction'] = pred["result"]
                        classified_pdf.to_csv(output_file_path, index=False)
                        break  # Exit the retry loop if successful
                except Exception as e:
                    print(f"An exception occurred: {e}")
                    retries += 1
                    print(f"Retrying extraction for row {row_index}")
            else:
                print(f"Maximum retries exceeded for row {row_index}. Setting extraction_prediction to empty string ")
                classified_pdf.at[row_index, 'extraction_prediction'] = ""

        # Save the updated classified_pdf to CSV after processing all rows
        classified_pdf.to_csv(output_file_path, index=False)
        print("Finished extraction")
        final_sub_path = os.path.join(Config.output_folder, f'experiment_{args.experiment}.csv')
        transform_submission(predicted_sub=output_file_path, sample_sub=Config.sample_sub_filepath,output_file_path= final_sub_path)
        print("Finished transformation, final sub generated")

    else:
        raise Exception("Invalid task type we currently support only classification and extraction")

