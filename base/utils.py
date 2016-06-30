import json
import time
from datetime import datetime


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return datetime_to_epoch(obj)

        return json.JSONEncoder.default(self, obj)


def parse_request_body(request):
    if not request.body:
        return dict()
    parsed_data = json.loads(request.body)
    return parsed_data


def datetime_to_epoch(dt):
    return int(time.mktime(dt.timetuple()) * 1000)
