import importlib.util
from pathlib import Path

_module_path = Path(__file__).with_name("06_sales_tools.py")
_spec = importlib.util.spec_from_file_location("_sales_tools_legacy", _module_path)
if _spec is None or _spec.loader is None:
    raise ImportError(f"Could not load sales tool module from {_module_path}")

_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)

load_clean_sales = _module.load_clean_sales
get_total_revenue = _module.get_total_revenue
get_top_products = _module.get_top_products
get_region_revenue = _module.get_region_revenue

__all__ = [
    "load_clean_sales",
    "get_total_revenue",
    "get_top_products",
    "get_region_revenue",
]
