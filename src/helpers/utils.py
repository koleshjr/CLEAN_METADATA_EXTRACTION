import ast
import re
import pandas as pd
import numpy as np

def preprocess_name(name):
    try:
        name = str(name)
        # Convert to lowercase and remove extra whitespaces
        name = re.sub(r'\s+', '', name.lower().strip())

        # Handle names separated by comma
        if ',' in name:
            names = name.split(',')
            names = [re.sub(r'[^a-zA-Z0-9\s/]', '', n) for n in names]
            return ','.join(names)

        # Remove special characters
        name = re.sub(r'[^a-zA-Z0-9\s/]', '', name)
        return name
    except:
        return name
def clean_predictions(df):
    strings_to_remove = ['lr', 'cr', 'deceased', 'titleno', 'plotno', 'portionno', 'lrno', 'crno', 'irno']
    for s in strings_to_remove:
        df['pred'] = df['pred'].str.replace(s, '')
    return df

def transform_submission(predicted_sub: str, sample_sub: str, output_file_path):
    sub = pd.read_csv(predicted_sub)
    sample_sub = pd.read_csv(sample_sub)
    sub = sub.dropna(subset = ['extraction_prediction']).reset_index(drop=True)
    new_data = []

    for index, row in sub.iterrows():
        filename = row['file'].split('.')[0]
        extraction_predictions = ast.literal_eval(row['extraction_prediction'])
        extraction_predictions = eval(row['extraction_prediction'])

        for extraction in extraction_predictions:

            if isinstance(extraction, dict):

                notice_number =extraction.get('gazette_notice_number', '')

                for key, value in extraction.items():
                    if key != 'gazette_notice_number':
                        if key == 'land_holder_names':
                            key = 'name of the holder'
                        elif key == 'land_registration_numbers':
                            key = 'Registration numbers'
                        elif key == 'land_location':
                            key = 'Land location'

                        id = f"{filename}_{notice_number}_{key}"
                        id = id.replace("2022_VOL252", "2022_252")
                        pred = value
                        new_data.append({'id': id, 'pred': pred})
            else:
                print("Invalid")
                print(extraction)
    new_df = pd.DataFrame(new_data)
    final_sub = pd.merge(sample_sub[['id']], new_df, how ="left", on ="id")
    final_sub.pred = final_sub['pred'].apply(lambda x: preprocess_name(x))
    final_sub = clean_predictions(final_sub)
    final_sub.drop_duplicates(subset = ['id'], inplace=True)

    final_sub.to_csv(output_file_path, index=False)
