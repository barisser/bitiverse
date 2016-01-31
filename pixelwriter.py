import requests
import messaging
import ownership as o
import reader as r

requests.packages.urllib3.disable_warnings()

version = 0
universe_width = 1920
universe_height = 1080
OP_RETURN_MAX_LENGTH = 80

def compress_coords(coords_set):
    n = 0
    m = 1
    for x in coords_set:
        for y in x:
            n += y * m
            m = m * (universe_width)
    return n

def decompress_coords(n):
    d = []
    odd = True
    r = []
    while n > 0:
        a = n % (universe_width)
        n = n - a
        n = n / (universe_width)
        if odd:
            r = [a]
            odd = False
        else:
            r.append(a)
            d.append(r)
            odd = True
            r = []
    assert len(d) % 2 == 0
    return d

def transfer_message(coords_set):
    return str(compress_coords(coords_set))

def get_safe_unspents(address, ownerlist):
    txs = r.get_address_txs(address)
    unsafe = ownerlist.keys()
    outputs = []
    for tx in txs:
        for output in tx['out']:
            if not output['spent'] and output['value'] > 0 and output['addr'] == address:
                h = str(tx['hash']) + str(":") + str(output['n'])
                if h in unsafe:
                    print str(h) + " is not a safe output to spend"
                else:
                    v = output['value']
                    q = {}
                    q['value'] = v
                    q['output'] = h
                    outputs.append(q)
    return q

def write_transfer_tx(from_address, coords_set, destination, private_key,
                      predecessor_inputs, push=False, fee=messaging.default_fee, sign=True):
    message = transfer_message(coords_set)

    sum_in = 0
    for x in predecessor_inputs:
        sum_in += x['value']
    amounts_array = []
    amounts_array.append(messaging.dust) # satoshi for recipient
    amounts_array.append(messaging.dust) # satoshi for change for me
    amounts_array.append(sum_in - messaging.dust * 2 - fee)
    destinations_array = []
    destinations_array.append(destination)
    destinations_array.append(from_address)
    destinations_array.append(from_address)

    tx = messaging.make_raw_transaction_from_specific_inputs_arrays(from_address,
                amounts_array, destinations_array, predecessor_inputs, fee=fee)
    tx = messaging.add_op_return(tx, message)
    if sign:
        tx = messaging.sign_tx(tx, private_key)
    if push and sign:
        tx_hash = messaging.pushtx(tx)
        return tx_hash
    else:
        return tx

def content_message(coords_set, content_url):
    d = "C/"+str(compress_coords(coords_set)) + "/" + str(content_url)
    assert len(d) <= OP_RETURN_MAX_LENGTH
    return d

def content_tx(from_address, coords_set, content_url, private_key, ownerlist, push=False, fee=messaging.default_fee):
    message = content_message(coords_set, content_url)
    inputs = [x for x in messaging.unspents(from_address) if not x['output'] in ownerlist.keys()]
    destination = from_address
    tx = messaging.make_unsigned_op_return_tx_with_specific_inputs(from_address, destination, message, inputs, fee=fee)
    tx = messaging.sign_tx(tx, private_key)
    if push:
        txhash = messaging.pushtx(tx)
        return txhash
    else:
        return tx
