# hkcr

Hong Kong Companies Registry Search SDK

## Installation

```bash
pip install hkcr
```

## CLI Usage

```bash
# Search local companies by name
hkcr "China"

# Search foreign companies
hkcr -f "HSBC"

# Search by BRN
hkcr -b C1572528

# JSON output
hkcr "China" -j
```

## Python Usage

```python
from hkcr import search_local, search_foreign, SearchOptions

# Search local companies
companies = search_local("China")
for co in companies:
    print(f"{co.brn}: {co.english_name}")

# Search by BRN
results = search_local("C1572528", SearchOptions(by_brn=True))

# Search foreign companies
foreign = search_foreign("HSBC")
```
