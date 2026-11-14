from urllib.parse import urlsplit, parse_qs
from local_http import Reply


class Provider:
    def __init__(self):
        self.records = {
            ('tenant-a', 'WAY-1001'): {'tenant': 'tenant-a', 'shipment': 'WAY-1001', 'revision': 2, 'status': 'in_transit'},
            ('tenant-a', 'WAY-1002'): {'tenant': 'tenant-a', 'shipment': 'WAY-1002', 'revision': 1, 'status': 'created'},
            ('tenant-b', 'WAY-1001'): {'tenant': 'tenant-b', 'shipment': 'WAY-1001', 'revision': 4, 'status': 'delivered'},
        }
        self.budget = 20
        self.calls = []
        self.fail_tenants = set()

    def handle(self, method, path, headers, body):
        parsed = urlsplit(path)
        query = parse_qs(parsed.query)
        tenant = query.get('tenant', [''])[0]
        self.calls.append((parsed.path, tenant, query.get('shipment', [''])[0]))
        if tenant in self.fail_tenants:
            return Reply.json({'error': 'account temporarily unavailable'}, 503)
        if parsed.path == '/active':
            return Reply.json({'shipments': [shipment for owner, shipment in self.records if owner == tenant]})
        if parsed.path == '/tracking':
            if self.budget <= 0:
                return Reply.json({'error': 'quota exhausted'}, 429)
            self.budget -= 1
            record = self.records.get((tenant, query.get('shipment', [''])[0]))
            return Reply.json(record, headers={'X-Quota-Remaining': str(self.budget)}) if record else Reply(404)
        return Reply(404)
