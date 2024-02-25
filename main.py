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
    document_loader = DocumentLoader()
    pages_dict = document_loader.load_and_get_pages(Config.data_folder)
    print(pages_dict.keys())
    # print(pages_dict['2022_VOL252.pdf'][12].metadata['page'])
    combined_pdf = pd.DataFrame(columns=['file', 'page', 'text'])
    for file, pages in pages_dict.items():
        for page in pages:
            if page.metadata['page'] in combined_pdf['page'].values:
                combined_pdf.loc[combined_pdf['page'] == page.metadata['page'], 'text'] = combined_pdf.loc[combined_pdf['page'] == page.metadata['page'], 'text'] + "/n/n" + page.page_content
            else:
                combined_pdf = combined_pdf.append({'file': file, 'page': page.metadata['page'], 'text': page.page_content}, ignore_index=True)
    
    combined_pdf.to_csv(Config.output_folder + '/combined_pdf.csv', index=False, escapechar='\\')

    # if args.task_type == 'classification':
    #     classification_results = pd.DataFrame(columns=['file', 'page', 'classification'])
    #     classifier = Classifier(llm, ClassificationOutput, Config.classification_prompt)
    #     for file, pages in pages_dict.items():
    #         for i, page in enumerate(pages):
    #             print(classifier.predict(page))
    #             classification_results = classification_results.append({'file': file, 'page': i, 'classification': classifier.predict(page)}, ignore_index=True)
    #             classification_results.to_csv(Config.output_folder + '/classification_results.csv', index=False)
    # elif args.task_type == 'extraction':
    #     extraction_results = pd.DataFrame(columns=['file', 'page', 'extraction'])
    #     extractor = Extractor(llm, ExtractionOutput, Config.extraction_prompt)
    #     for file, pages in pages_dict.items():
    #         for i, page in enumerate(pages):
    #             print(extractor.predict(page))
    #             extraction_results = extraction_results.append({'file': file, 'page': i, 'extraction': extractor.predict(page)}, ignore_index=True)
    #             extraction_results.to_csv(Config.output_folder + '/extraction_results.csv', index=False)
    # else:
    #     raise Exception("Invalid task type we currently support only classification and extraction")




    # # if args.task_type == 'classification':
    # #     classifier = Classifier(llm, ClassificationOutput, Config.classification_prompt)
    # #     page_text = document_loader.get_page_text()
    # #     print(classifier.predict(page_text))
    # # elif args.task_type == 'extraction':
    # #     extractor = Extractor(llm, ExtractionOutput, Config.extraction_prompt)
    # #     page_text = document_loader.get_page_text()
    # #     print(extractor.predict(page_text))
    # # else:
    # #     raise Exception("Invalid task type we currently support only classification and extraction")