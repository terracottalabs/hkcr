# hkcr

Search the Hong Kong Companies Registry.

![Demo](https://vhs.charm.sh/vhs-4ieVtxA6xxvAySbH7G99SN.gif)

This repo provides both a **TypeScript/Bun CLI** and a **Python SDK** for searching company information from the [HK Companies Registry](https://data.gov.hk/en-data/dataset/hk-cr-crdata-list-addr).

## Features

- Search local HK companies by name or BRN
- Search registered non-HK (foreign) companies
- Pretty table output or JSON
- Zero external dependencies

## TypeScript CLI

### Install

```bash
# Build from source
bun install
bun run build

# Add to PATH
cp dist/hkcr /usr/local/bin/
```

### Usage

```bash
hkcr "China"           # Search local companies
hkcr -f "HSBC"         # Search foreign companies
hkcr -b C1572528       # Search by BRN
hkcr "China" -j        # JSON output
hkcr -h                # Help
```

## Python SDK

### Install

```bash
cd python
pip install -e .
```

### CLI Usage

```bash
hkcr "China"           # Search local companies
hkcr -f "HSBC"         # Search foreign companies
hkcr -b C1572528       # Search by BRN
hkcr "China" -j        # JSON output
```

### Library Usage

```python
from hkcr import search_local, search_foreign, SearchOptions

# Search by company name
companies = search_local("China")
for co in companies:
    print(f"{co.brn}: {co.english_name}")

# Search by BRN (exact match)
results = search_local("C1572528", SearchOptions(by_brn=True))

# Search foreign companies
foreign = search_foreign("HSBC")
```

## API Reference

### Endpoints

| Type | Endpoint |
|------|----------|
| Local | `https://data.cr.gov.hk/cr/api/api/v1/api_builder/json/local/search` |
| Foreign | `https://data.cr.gov.hk/cr/api/api/v1/api_builder/json/foreign/search` |

### Query Parameters

| Parameter | Values |
|-----------|--------|
| `query[0][key1]` | `Brn` or `Comp_name` |
| `query[0][key2]` | `equal` or `begins_with` |
| `query[0][key3]` | Search value |

## Data Source

Data provided by the [Companies Registry, HKSAR](https://data.gov.hk/en-data/dataset/hk-cr-crdata-list-addr/resource/1214e348-7069-440e-8144-6483fc944090). Updated daily.

## License

MIT
