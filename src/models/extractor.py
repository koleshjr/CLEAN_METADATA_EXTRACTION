from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List
class LandRegistrationAct(BaseModel):
    """fields to be extracted from the gazette"""
    gazette_notice_number: str = Field(..., description="extract the gazette notice number from the information.")
    land_holder_names: str = Field(..., description="extract comma separated land holder names or name from the information and do not include(ID number) and (deceased) information or any number associated with the name.")
    land_registration_numbers: str = Field(..., description="Extract land registration number or Known as or leased as. Extract comma separated values if LR and either IR and CR are in the same act.Extract Only the values Don't include the identifiers e.g LR No, IR , CR, Title no , Plot No, Portion No")
    land_location: str = Field(..., description=" Extract one unique location where the land is situated in and You **MUST** include the identifiers e.g district of, city of if mentioned in the act. If none is mentioned return an empty string as the value")

class ExtractionOutput(BaseModel):
    """list of extracted MetadataOutput objects from the gazette"""
    result: List[LandRegistrationAct]

