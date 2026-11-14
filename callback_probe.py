import time
from callback import verify
from local_http import Reply


class CallbackProbe:
    def __init__(self, clock=time.time):
        self.clock = clock

    def handle(self, method, path, headers, body):
        if method != 'POST' or path != '/callback':
            return Reply(404)
        try:
            payload = verify(body, headers, int(self.clock()))
            return Reply.json({'valid': True, 'delivery': payload.get('delivery'), 'hint': payload})
        except (ValueError, KeyError) as error:
            return Reply.json({'valid': False, 'reason': str(error)}, 400)
