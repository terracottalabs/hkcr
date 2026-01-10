import type { LocalCompany, ForeignCompany } from "./types";

const BASE_URL = "https://data.cr.gov.hk/cr/api/api/v1/api_builder/json";

interface QueryParams {
  query: string;
  byBrn: boolean;
  exact: boolean;
}

function buildUrl(endpoint: "local" | "foreign", params: QueryParams): string {
  const key1 = params.byBrn ? "Brn" : "Comp_name";
  const key2 = params.byBrn || params.exact ? "equal" : "begins_with";
  const searchParams = new URLSearchParams({
    "query[0][key1]": key1,
    "query[0][key2]": key2,
    "query[0][key3]": params.query,
  });
  return `${BASE_URL}/${endpoint}/search?${searchParams}`;
}

export async function searchLocal(params: QueryParams): Promise<LocalCompany[]> {
  const url = buildUrl("local", params);
  const res = await fetch(url);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function searchForeign(params: QueryParams): Promise<ForeignCompany[]> {
  const url = buildUrl("foreign", params);
  const res = await fetch(url);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}
