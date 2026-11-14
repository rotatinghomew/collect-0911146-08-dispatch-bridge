import json
from local_http import serve, request
from fixture_provider import Provider
from callback_probe import CallbackProbe
from callback import signature, KEYS
from tracking_client import fetch_tracking
from dispatch_view import display_detail


def main():
    payload = {'tenant': 'tenant-a', 'delivery': 'delivery-1', 'shipment': 'WAY-1001', 'revision': 3, 'hint': True}
    raw = json.dumps(payload).encode()
    with serve(Provider()) as provider, serve(CallbackProbe(clock=lambda: 1000)) as receiver:
        headers = {'X-Tenant': 'tenant-a', 'X-Key-Id': 'k1', 'X-Timestamp': '1000',
                   'X-Signature': signature(raw, 1000, KEYS['tenant-a']['k1'])}
        reply = request(receiver + '/callback', payload, headers)
        print(json.dumps({'callback_probe': json.loads(reply.body),
            'detail': display_detail(fetch_tracking(provider, 'tenant-a', 'WAY-1001'))}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
