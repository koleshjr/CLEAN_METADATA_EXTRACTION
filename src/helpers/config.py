class Config:
    extraction_prompt  = """A page text will be passed to you. Extract from it all gazette metadata present in the page. The metadata to be extracted includes the gazette notice number, land holder names, land registration numbers, and land location.
    Do not make up ANY extra information. Only extract the information that is present in the page text. If the information is not present, leave the field empty.
    page_text: {page_text}
    """
    classification_prompt = """A page text will be passed to you. If the page text mentions 'THE LAND REGISTRATION ACT' , the answer should be true.
      If the page text does not mention 'THE LAND REGISTRATION ACT' the answer should be false. The page text should strictly mention the full phrase 'THE LAND REGISTRATION ACT' for it to be true.
      page_text: {page_text}
      """
    data_folder = "src/data/test"
    output_folder = "src/output"
    sample_sub_filepath = "src/data/sample_submission.csv"