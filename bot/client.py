import hmac
import hashlib
import time
import requests
import logging
from urllib.parse import urlencode

logger = logging.getLogger("BinanceClient")

class BinanceFuturesClient:
    BASE_URL = "https://demo-fapi.binance.com"

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def _generate_signature(self, query_string):
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def post_order(self, params):
        """
        Signs and sends a POST request to the Binance Futures API.
        """
        endpoint = "/fapi/v1/order"
        url = f"{self.BASE_URL}{endpoint}"
        
        # Get server time to synchronize
        try:
            time_res = requests.get(f"{self.BASE_URL}/fapi/v1/time")
            server_time = time_res.json().get('serverTime')
            params['timestamp'] = server_time if server_time else int(time.time() * 1000)
        except:
            params['timestamp'] = int(time.time() * 1000)
        
        # Create query string and signature
        query_string = urlencode(params)
        signature = self._generate_signature(query_string)
        query_string += f"&signature={signature}"
        
        headers = {
            "X-MBX-APIKEY": self.api_key
        }

        logger.info(f"Sending Order Request: {params['type']} {params['side']} {params['symbol']}")
        
        try:
            response = requests.post(f"{url}?{query_string}", headers=headers, timeout=10)
            response_json = response.json()
            
            if response.status_code == 200:
                logger.info("API Response: Success")
                return True, response_json
            else:
                error_msg = response_json.get('msg', 'Unknown Error')
                logger.error(f"API Response: Failure ({response.status_code}) - {error_msg}")
                return False, response_json
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error: {str(e)}")
            return False, {"msg": f"Network/Connection Error: {str(e)}"}
