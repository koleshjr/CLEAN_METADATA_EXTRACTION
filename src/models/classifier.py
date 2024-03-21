from langchain_core.pydantic_v1 import BaseModel, Field 
class ClassificationOutput(BaseModel):
    """ Tag the information provided with a particular classification"""
    answer: bool = Field(description = "should be true if 'THE LAND REGISTRATION ACT' is mentioned , false if not mentioned" )
