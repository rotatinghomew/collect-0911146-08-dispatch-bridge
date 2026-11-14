import json
import unittest
from callback import verify, signature, KEYS
from callback_probe import CallbackProbe
from fixture_provider import Provider
from tracking_client import fetch_tracking
from local_http import serve, request
from revisions import validate


class BridgeTests(unittest.TestCase):
    def signed(self):
        payload = {'tenant': 'tenant-a', 'delivery': 'd-1', 'shipment': 'WAY-1001', 'revision': 3, 'hint': True}
        raw = json.dumps(payload).encode()
        headers = {'X-Tenant': 'tenant-a', 'X-Key-Id': 'k1', 'X-Timestamp': '1000',
                   'X-Signature': signature(raw, 1000, KEYS['tenant-a']['k1'])}
        return payload, raw, headers

    def test_valid_local_http_callback(self):
        payload, raw, headers = self.signed()
        with serve(CallbackProbe(lambda: 1000)) as base:
            reply = request(base + '/callback', payload, headers)
            self.assertEqual(reply.status, 200)
            self.assertEqual(json.loads(reply.body)['delivery'], 'd-1')

    def test_signature_and_time_window_reject(self):
        payload, raw, headers = self.signed()
        with self.assertRaises(ValueError):
            verify(raw + b' ', headers, 1000)
        with self.assertRaises(ValueError):
            verify(raw, headers, 2000)

    def test_tenant_and_quota_are_observable(self):
        provider = Provider()
        with serve(provider) as base:
            first = fetch_tracking(base, 'tenant-a', 'WAY-1001')
            second = fetch_tracking(base, 'tenant-b', 'WAY-1001')
            self.assertNotEqual(first['status'], second['status'])
            provider.budget = 0
            with self.assertRaises(ValueError):
                fetch_tracking(base, 'tenant-a', 'WAY-1001')

    def test_retraction_has_target(self):
        with self.assertRaises(ValueError):
            validate({'revision': 3, 'status': 'retracted'})
