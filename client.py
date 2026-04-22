import time
import logging
import hmac
import hashlib
import requests
from config import API_KEY,SECRET_KEY,BASE_URL
from urllib.parse import urlencode
class bc:
    def __init__(self):
        self.base_url=BASE_URL
        self.session=requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY":API_KEY
        })
    def _sign_params(self, params: dict) -> dict:
        query_string=urlencode(params)
        signature=hmac.new(
            SECRET_KEY.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ) .hexdigest()
        params["signature"]=signature
        return params
    def public_requests(self,method:str,endpoint:str,params:dict|None=None):
        params=params or {}
        url=f"{self.base_url}{endpoint}"
        response=self.session.request(method=method,url=url,params=params,timeout=15)
        response.raise_for_status()
        return response.json()
    def signed_request(self,method: str,endpoint: str, params: dict |None=None):
        logging.info(f"Request: {params}")
        params= params or {}
        params["timestamp"]= int(time.time()*1000)
        params= self._sign_params(params)
        url=f"{self.base_url}{endpoint}"
        response=self.session.request(method=method,url=url,params=params,timeout=15)
        try:
            logging.info(f"Response:{response.text}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError:
            logging.error(f"Error{response.text}")
            print("Error Response:", response.text)
            raise
    def get_server_time(self):
        return self.public_requests("GET","/fapi/v1/time")
    def get_account(self):
        return self.signed_requests("GET","/fapi/v2/account")
    def get_price(self,symbol):
        data=self.public_requests("GET","/fapi/v1/ticker/price",{"symbol":symbol})
        return float(data["price"])
