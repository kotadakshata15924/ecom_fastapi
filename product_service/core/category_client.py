import os
import httpx
from uuid import UUID
from exception.product_exception import InvalidCategoryException, CategoryServiceUnavailableException

# base URL of the category_service — set this per environment, e.g.
#   export CATEGORY_SERVICE_URL="http://localhost:8001"
CATEGORY_SERVICE_URL = os.getenv("CATEGORY_SERVICE_URL", "http://localhost:8001")


def verify_category_exists(category_id: UUID) -> None:
    """Calls category_service to confirm the category_id is real.
    Raises InvalidCategoryException if it doesn't exist, or
    CategoryServiceUnavailableException if category_service can't be reached.
    """
    url = f"{CATEGORY_SERVICE_URL}/api/v1/category/{category_id}"
    try:
        response = httpx.get(url, timeout=3.0)
    except httpx.RequestError:
        raise CategoryServiceUnavailableException("category service is unavailable, try again later")

    if response.status_code == 404:
        raise InvalidCategoryException(f"category '{category_id}' does not exist")
    if response.status_code != 200:
        raise CategoryServiceUnavailableException("category service returned an unexpected error")
