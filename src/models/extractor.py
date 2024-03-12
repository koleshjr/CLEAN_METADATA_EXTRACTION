from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

class MetadataOutput(BaseModel):
    """fields to be extracted from the gazette"""
    gazette_notice_number: str = Field(..., description="extract the gazette notice number from the information.")
    land_holder_names: str = Field(..., description="extract comma separated values of the land holder name or names from the information and do not include the ID number and deceased information.")
    land_registration_numbers: str = Field(..., description="extract the land registration number or comma separated numbers if both LR and IR or LR and CR are present from the information. Don't include the identifiers e.g LR No IR , CR, Title no , Plot No just the values")
    land_location: str = Field(..., description="extract the full land location as mentioned in the information including the keys district of, city of if mentioned in the information")

class ExtractionOutput(BaseModel):
    """list of extracted MetadataOutput objects from the gazette"""
    result: List[MetadataOutput]
