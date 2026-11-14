ALLOWED = {'created', 'in_transit', 'delivered', 'retracted'}


def validate(record):
    if record['status'] not in ALLOWED or not isinstance(record['revision'], int):
        raise ValueError('运单修订格式无效')
    if record['revision'] < 1:
        raise ValueError('修订号应为正数')
    if record['status'] == 'retracted' and record.get('retracts') is None:
        raise ValueError('撤回记录需指出被撤回的修订')
    return record
