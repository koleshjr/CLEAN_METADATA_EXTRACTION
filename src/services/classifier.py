from operator import itemgetter
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.utils.function_calling import convert_to_openai_function

class Classifier:
    def __init__(self, llm, pydantic_model, prompt):
        gazzette_tagging_function = [convert_to_openai_function(pydantic_model)]
        self.model = llm.bind(
            functions = gazzette_tagging_function,
            function_call = {"name": "ClassificationOutput"}
        )
        self.custom_prompt = PromptTemplate(template = prompt, 
                                           input_variables = ["page_text"],
                                           
        )

    def predict(self, page_text):
        chain = (
            {"page_text": itemgetter("page_text")}
            | self.custom_prompt
            | self.model 
            | JsonOutputFunctionsParser()
        )
        
        return chain.invoke({"page_text": page_text})
    