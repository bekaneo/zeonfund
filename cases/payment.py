from hashlib import md5
from random import randint
from decouple import config
from django.utils.crypto import get_random_string
from fund import settings

def create_sig(request, order_id, salt):
    sig = {
        'pg_order_id': str(order_id),
        'pg_merchant_id': str(config('MERCHANT_ID')),
        'pg_amount': str(request.data.get('amount')),
        'pg_description': str(request.data.get('description')),
        'pg_currency': 'KGS',
        'pg_salt': str(salt),
    }
    res = []
    a = sorted(sig)
    for i in a:
        res.append(str(sig[i]))

    res.insert(0, 'init_payment.php')
    res.append('LeFnP16MP6AU6YKc')
    signature = ';'.join(res)

    signature = md5(signature.encode('utf-8')).hexdigest()
    return signature

