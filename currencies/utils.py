import httpx

from currencies.constants import BATCH_SIZE


def get_currencies_info_all(url):
    with httpx.Client() as client:
        response = client.get(url=url)
        response.raise_for_status()
        data = response.json()

        return data[:BATCH_SIZE]
