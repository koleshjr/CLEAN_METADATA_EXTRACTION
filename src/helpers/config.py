class Config:
    extraction_prompt  = """A page text will be passed to you. Extract from it all gazette metadata present in the page. The metadata to be extracted includes the gazette notice number, land holder names, land registration numbers, and land location.
    Do not make up ANY extra information. Only extract the information that is present in the page text. If the information is not present, leave the field empty."""
    classification_prompt = """A page text will be passed to you. Classify the page text as either mentioning the land registration act or the registered land act. If the page text mentions the land registration act or the registered land act, the answer should be true.
      If the page text does not mention the land registration act or the registered land act, the answer should be false."""
    data_folder = "src/data/test"
    output_folder = "src/output"