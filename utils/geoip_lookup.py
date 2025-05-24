import requests

def get_geoip_info(ip):
    try:
        url = f"https://ipinfo.io/{ip}/json"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            city = data.get("city", "Unknown")
            country = data.get("country", "Unknown")
            return f"{city}, {country}"
    except Exception:
        pass
    return None
