from dataclasses import dataclass
from typing import Optional

@dataclass
class LocalCompany:
    brn: str
    english_name: str
    chinese_name: str
    address: str
    company_type: str
    date_of_incorporation: str
    redomiciliation_date: Optional[str] = None

    @classmethod
    def from_api(cls, data: dict) -> "LocalCompany":
        return cls(
            brn=data.get("Brn", ""),
            english_name=data.get("English_Company_Name", ""),
            chinese_name=data.get("Chinese_Company_Name", ""),
            address=data.get("Address_of_Registered_Office", ""),
            company_type=data.get("Company_Type", ""),
            date_of_incorporation=data.get("Date_of_Incorporation", ""),
            redomiciliation_date=data.get("Re-domiciliation_Date"),
        )

@dataclass
class ForeignCompany:
    brn: str
    corporate_name: str
    hk_name: str
    other_names: str
    hk_other_name: str
    address: str
    place_of_incorporation: str
    company_type: str
    date_of_registration: str

    @classmethod
    def from_api(cls, data: dict) -> "ForeignCompany":
        return cls(
            brn=data.get("Brn", ""),
            corporate_name=data.get("Corporate_Name", ""),
            hk_name=data.get("Approved_name_for_carrying_on_business_in_H.K._Corporate", ""),
            other_names=data.get("Other_Corporate_Name_s", ""),
            hk_other_name=data.get("Approved_name_for_carrying_on_business_in_H.K._Other_Corporate", ""),
            address=data.get("Principal_Place_of_Business_in_H.K.", ""),
            place_of_incorporation=data.get("Place_of_Incorporation", ""),
            company_type=data.get("Company_Type", ""),
            date_of_registration=data.get("Date_of_Registration", ""),
        )

@dataclass
class SearchOptions:
    by_brn: bool = False
    exact: bool = False
