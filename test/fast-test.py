
class RateLimitException(Exception):
    pass

data = {'status': 429}
if ('status' in data) and (data['status'] == 429):
    raise RateLimitException()