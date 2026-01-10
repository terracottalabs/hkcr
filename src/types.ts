export interface LocalCompany {
  Brn: string;
  Chinese_Company_Name: string;
  English_Company_Name: string;
  Address_of_Registered_Office: string;
  Company_Type: string;
  Date_of_Incorporation: string;
  "Re-domiciliation_Date"?: string;
}

export interface ForeignCompany {
  Brn: string;
  Corporate_Name: string;
  "Approved_name_for_carrying_on_business_in_H.K._Corporate": string;
  "Other_Corporate_Name_s": string;
  "Approved_name_for_carrying_on_business_in_H.K._Other_Corporate": string;
  "Principal_Place_of_Business_in_H.K.": string;
  Place_of_Incorporation: string;
  Company_Type: string;
  Date_of_Registration: string;
}

export type Company = LocalCompany | ForeignCompany;

export interface SearchOptions {
  foreign: boolean;
  brn: boolean;
  exact: boolean;
  json: boolean;
}
