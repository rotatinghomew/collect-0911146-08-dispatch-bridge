import json
from urllib.parse import urlencode
from local_http import request


def fetch_tracking(base, tenant, shipment):
    reply = request(base + '/tracking?' + urlencode({'tenant': tenant, 'shipment': shipment}))
    if reply.status != 200:
        raise ValueError('详情查询失败：' + str(reply.status))
    return json.loads(reply.body)


def fetch_active(base, tenant):
    reply = request(base + '/active?' + urlencode({'tenant': tenant}))
    if reply.status != 200:
        raise ValueError('活跃清单不可读')
    return json.loads(reply.body)
