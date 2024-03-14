from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

class MetadataOutput(BaseModel):
    """fields to be extracted from the gazette"""
    gazette_notice_number: str = Field(..., description="extract the gazette notice number from the information.")
    land_holder_names: str = Field(..., description="extract comma separated values of the land holder name or names from the information and do not include the ID number and deceased information.")
    land_registration_numbers: str = Field(..., description="What the land is registered as or Known as or leased as.Comma separated values if LR, IR and CR are in the same act.Extract Only the values Don't include the identifiers e.g LR No, IR , CR, Title no , Plot No, Portion No")
    land_location: str = Field(..., description="Where the land is located and comes after situate or situate in. There is only one location. You MUST include the identifiers e.g district of, city of. If none is mentioned return an empty string as the value")

class ExtractionOutput(BaseModel):
    """list of extracted MetadataOutput objects from the gazette"""
    result: List[MetadataOutput]
