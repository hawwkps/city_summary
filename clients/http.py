import time

import requests

from clients.exceptions import ExternalServiceError

TIMEOUT = 2
MAX_ATTEMPTS = 3

def get_json(url: str, params: dict | None = None) -> dict:
    for attempt in range(1, MAX_ATTEMPTS+1):
        try:
            response = requests.get(url,params=params, timeout=TIMEOUT*attempt)
            response.raise_for_status()
            data = response.json()
            return data
            
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):

            if attempt < MAX_ATTEMPTS:
                time.sleep(attempt*TIMEOUT) 
                continue
            else:
                raise ExternalServiceError("Service unavailable")
            
        except requests.exceptions.HTTPError as error:

            status = error.response.status_code

            if status in (400,404,422):
                raise ExternalServiceError("Service unavailable")
            elif status >= 500:
                if attempt < MAX_ATTEMPTS:
                    time.sleep(attempt*TIMEOUT)
                    continue
                else:
                    raise ExternalServiceError("Service unavailable")
            elif status == 429:
                if attempt < MAX_ATTEMPTS:
                    retry_after = error.response.headers.get("Retry-After")
                    if retry_after is not None:
                        time.sleep(int(retry_after))
                        continue
                    else:
                        time.sleep(2*attempt)
                        continue
                else:
                    raise ExternalServiceError("Service unavailable")