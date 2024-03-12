class Config:
    extraction_prompt  = """A page text will be passed to you. Extract from it all gazette metadata present in the page. The metadata to be extracted includes the gazette notice number, land holder names, land registration numbers, and land location.
    Do not make up ANY extra information. Only extract the information that is present in the page text. If the information is not present, leave the field empty.
    page_text: {page_text}
    """
    classification_prompt = """A page text will be passed to you. If the page text contains mentions of 'THE LAND REGISTRATION ACT'  , the answer should be true else false.
    The page text **MUST** contain strict mentions of 'THE LAND REGISTRATION ACT' for it to be true. Nothing else can be true if it doesn't contain mentions of 'THE LAND REGISTRATION ACT'

      page_text: {page_text}
      """
    data_folder = "src/data/test"
    output_folder = "src/output"
    sample_sub_filepath = "src/data/sample_submission.csv"