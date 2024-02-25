from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain.utils.openai_functions import convert_pydantic_to_openai_function

class Classifier:
    def __init__(self, llm, pydantic_model, prompt):
        gazzette_tagging_function = [convert_pydantic_to_openai_function(pydantic_model)]
        self.model = llm.bind(
            functions = gazzette_tagging_function,
            function_call = {"name": "ClassificationOutput"}
        )
        self.custom_prompt = ChatPromptTemplate.from_messages([
            ("system", prompt),
            ("human", "{page_text}")
        ])

    def predict(self, page_text):
        chain = self.custom_prompt | self.model | JsonOutputFunctionsParser
        return chain.invoke(page_text=page_text)