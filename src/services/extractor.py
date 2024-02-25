from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain.utils.openai_functions import convert_pydantic_to_openai_function

class Extractor:
    def __init__(self, llm, pydantic_model, prompt):
        gazzette_extraction_function = [convert_pydantic_to_openai_function(pydantic_model)]
        self.model = llm.bind(
            functions = gazzette_extraction_function,
            function_call = {"name": "ExtractionOutput"}
        )
        self.custom_prompt = ChatPromptTemplate.from_messages([
            ("system", prompt),
            ("human", "{page_text}")
        ])

    def predict(self, page_text):
        # this assumes that the input is only a single page of text
        chain = self.custom_prompt | self.model | JsonOutputFunctionsParser(key_name = "MetadataOutput")
        return chain.invoke(page_text=page_text)
