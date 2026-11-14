from revisions import validate


def display_detail(record):
    validate(record)
    return {'tenant': record['tenant'], 'shipment': record['shipment'],
            'revision': record['revision'], 'status': record['status'],
            'retracts': record.get('retracts')}
