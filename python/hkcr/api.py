import urllib.request
import urllib.parse
import json
from typing import List
from .types import LocalCompany, ForeignCompany, SearchOptions

BASE_URL = "https://data.cr.gov.hk/cr/api/api/v1/api_builder/json"

def _build_url(endpoint: str, query: str, options: SearchOptions) -> str:
    key1 = "Brn" if options.by_brn else "Comp_name"
    key2 = "equal" if options.by_brn or options.exact else "begins_with"
    params = urllib.parse.urlencode({
        "query[0][key1]": key1,
        "query[0][key2]": key2,
        "query[0][key3]": query,
    })
    return f"{BASE_URL}/{endpoint}/search?{params}"

def _fetch(url: str) -> list:
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode())

def search_local(query: str, options: SearchOptions = None) -> List[LocalCompany]:
    """Search local HK companies by name or BRN."""
    options = options or SearchOptions()
    url = _build_url("local", query, options)
    data = _fetch(url)
    return [LocalCompany.from_api(item) for item in data]

def search_foreign(query: str, options: SearchOptions = None) -> List[ForeignCompany]:
    """Search non-HK registered companies by name or BRN."""
    options = options or SearchOptions()
    url = _build_url("foreign", query, options)
    data = _fetch(url)
    return [ForeignCompany.from_api(item) for item in data]
