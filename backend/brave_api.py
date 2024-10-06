import requests
from requests.structures import CaseInsensitiveDict


def get_compare_image(initial_hypothesis):
    print(initial_hypothesis, "hypothesis")
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Accept-Encoding"] = "gzip"
    headers["X-Subscription-Token"] = "BSAXYZFwgCtVk6qB8WOZ5TiO3tDlNCM"

    request_url = "https://api.search.brave.com/res/v1/images/search"
    params = {"q": f"{initial_hypothesis}"}
    response = requests.get(request_url, params=params, headers=headers)
    print(response.json())
    try:
        result = response.json()["results"][0]["properties"]["url"]
        return result
    except:
        print("Error - No relevant results")


# get_compare_image("broken femur xray")
