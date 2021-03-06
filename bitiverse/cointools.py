import hashlib
import pybitcointools
import os

b58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
subkey_complexity = 32

def base58encode(n):
    result = ''
    while n > 0:
        result = b58[n%58] + result
        n /= 58
    return result

def base58decode(s):
    n = 0
    r = 0
    for x in s[::-1]:
        m = b58.index(x)
        n = n + m * 58**r
        r = r + 1
    return hex(n)

def address_to_oa(addr):
    m = str(base58decode(addr))
    m = '0'+m[2:len(m)-9]
    m = '0x130'+m
    return hex(int(m, 16))

def base256encode(x):
    s = ''
    while x > 0:
        r = x % 256
        s += chr(r)
        x -= r
        x = x / 256
    return s

def base256decode(s):
    result = 0
    for c in s:
        result = result * 256 + ord(c)
    return result

def countLeadingChars(s, ch):
    count = 0
    for c in s:
        if c == ch:
            count += 1
        else:
            break
    return count

# https://en.bitcoin.it/wiki/Base58Check_encoding
def base58CheckEncode(version, payload):
    s = chr(version) + payload
    checksum = hashlib.sha256(hashlib.sha256(s).digest()).digest()[0:4]
    result = s + checksum
    leadingZeros = countLeadingChars(result, '\0')
    return '1' * leadingZeros + base58encode(base256decode(result))

def privateKeyToWif(key_hex):
    return base58CheckEncode(0x80, key_hex.decode('hex'))

def pair(complexity=512):
    se = hashlib.sha256(os.urandom(complexity)).hexdigest()
    priv = privateKeyToWif(se)
    pub = pybitcointools.privtopub(priv)
    addr = pybitcointools.pubtoaddr(pub)
    return priv, pub, addr
