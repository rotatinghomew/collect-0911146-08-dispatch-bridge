import hashlib
import hmac
import json


KEYS = {'tenant-a': {'k1': b'local-a-one', 'k2': b'local-a-two'},
        'tenant-b': {'k1': b'local-b-one'}}


def signature(body, timestamp, key):
    return hmac.new(key, str(timestamp).encode() + b'.' + body, hashlib.sha256).hexdigest()


def verify(body, headers, now):
    tenant = headers.get('X-Tenant')
    key_id = headers.get('X-Key-Id')
    key = KEYS.get(tenant, {}).get(key_id)
    if not key:
        raise ValueError('未知租户或签名密钥')
    try:
        timestamp = int(headers['X-Timestamp'])
    except (KeyError, ValueError):
        raise ValueError('缺少有效签名时间') from None
    if abs(now - timestamp) > 300:
        raise ValueError('签名超出接收时间窗')
    if not hmac.compare_digest(signature(body, timestamp, key), headers.get('X-Signature', '')):
        raise ValueError('签名不匹配')
    payload = json.loads(body)
    if payload.get('tenant') != tenant:
        raise ValueError('通知租户与签名不一致')
    return payload
