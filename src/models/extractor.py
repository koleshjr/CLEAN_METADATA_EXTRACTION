from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

class MetadataOutput(BaseModel):
    """fields to be extracted from the gazette"""
    gazette_notice_number: str = Field(..., description="extract the gazette notice number from the information.")
    land_holder_names: str = Field(..., description="extract the land holder name or names from the information.")
    land_registration_numbers: str = Field(..., description="extract the land registration number or numbers from the information.")
    land_location: str = Field(..., description="extract the land location from the information.")

class ExtractionOutput(BaseModel):
    """list of extracted MetadataOutput objects from the gazette"""
    result: List[MetadataOutput]
