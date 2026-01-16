import requests
from config.settings.base import API_QUERY_HOST


def get_ip_data(ip: str = "") -> dict:
    r = requests.get(f"{API_QUERY_HOST}{ip}", timeout=10)
    r.raise_for_status()
    data = r.json()

    if data.get("status") != "success":
        return {}

    return {
        "ip_address": data.get("query"),
        "country": data.get("country"),
        "country_code": data.get("countryCode", -1),
        "region": data.get("regionName"),
        "city": data.get("city"),
        "lat": data.get("lat"),
        "lon": data.get("lon"),
        "isp": data.get("isp"),
        "org": data.get("org"),
        "asn": data.get("as"),
    }

__all__: list[str] = "get_ip_data",