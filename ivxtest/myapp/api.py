import datetime
import logging
import os
import requests
from django.utils import timezone

logger = logging.getLogger(__name__)


class ApiResult:
    def __init__(
            self,
            image_path: str,
            request_timestamp: datetime.datetime,
            response_timestamp: datetime.datetime,
            res: dict,
    ):
        self.image_path = image_path
        self.request_timestamp = request_timestamp
        self.response_timestamp = response_timestamp
        self.success = res['success']
        self.message = res['message']
        if self.success:
            self.clazz = res['estimated_data']['class']
            self.confidence = res['estimated_data']['confidence']
        else:
            self.clazz = None
            self.confidence = None


class ApiErrorResult:
    def __init__(
            self,
            image_path: str,
            request_timestamp: datetime.datetime,
            response_timestamp:
            datetime.datetime, response_code,
    ):
        self.image_path = image_path
        self.request_timestamp = request_timestamp
        self.response_timestamp = response_timestamp
        self.response_code = response_code


class ApiTimeoutResult:
    def __init__(
            self,
            image_path: str,
            request_timestamp: datetime.datetime,
            response_timestamp: datetime.datetime,
    ):
        self.image_path = image_path
        self.request_timestamp = request_timestamp
        self.response_timestamp = response_timestamp


class ApiClient:
    def __init__(self):
        self.api_url = os.environ['API_URL']
        timeout = os.getenv('API_TIMEOUT')
        self.timeout = int(timeout) if timeout is not None else None

    def post(self, image_path: str) -> ApiResult | ApiErrorResult | ApiTimeoutResult:
        request_timestamp = timezone.now()
        try:
            res = requests.post(self.api_url, data={'image_path': image_path}, timeout=self.timeout)
            response_timestamp = timezone.now()
            if res.status_code != requests.codes.ok:
                logger.warning('API response code is not OK but {}'.format(res.status_code))
                return ApiErrorResult(image_path, request_timestamp, response_timestamp, res.status_code)

            return ApiResult(image_path, request_timestamp, response_timestamp, res.json())
        except requests.exceptions.Timeout:
            logger.warning('API timed out')
            return ApiTimeoutResult(image_path, request_timestamp, timezone.now())
