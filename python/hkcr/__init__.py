"""hkcr - Hong Kong Companies Registry Search"""

from .api import search_local, search_foreign
from .types import LocalCompany, ForeignCompany, SearchOptions

__version__ = "0.1.0"
__all__ = ["search_local", "search_foreign", "LocalCompany", "ForeignCompany", "SearchOptions"]
