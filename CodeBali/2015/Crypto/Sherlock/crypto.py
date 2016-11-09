#!/usr/bin/python2
import hashlib, string, sys

ROUNDS = 20000

def xor(a, b):
    l = min(len(a), len(b))
    print l
    return ''.join([chr(ord(x) ^ ord(y)) for x, y in zip(a[:l], b[:l])])

def h(x):
    x = hashlib.sha512(x).digest()
    print x[:16]
    x = xor(x[:16], x[16:])
    return x

def verify(x):
    return all([ord(c) < 127 for c in x])

def crypt(msg, passwd):
    k = h(passwd)

    for i in xrange(ROUNDS):
        k = h(k)

    out = ''
    for i in xrange(0, len(msg), 16):
        out += xor(msg[i:i+16], k)
        k = h(k + str(len(msg)))

    return out

def encrypt(msg, passwd):
    msg = crypt(msg, passwd)

    return msg.encode('base64')

def decrypt(msg, passwd):
    msg = crypt(msg.decode('base64'), passwd)

    if verify(msg):
        return msg
    else:
        sys.stderr.write('Looks like a bad decrypt\n')
        sys.exit(1)

if len(sys.argv) < 5 or sys.argv[1] not in ('encrypt', 'decrypt'):
    print 'Usage:\tcrypto.py encrypt <password> <infile> <outfile>'
    print '\tcrypto.py decrypt <password> <infile> <outfile>'
    sys.exit(1)

op, passwd, infile, outfile = sys.argv[1:]

inp = open(infile).read()

if op == 'encrypt':
    ct = encrypt(inp, passwd)
    open(outfile, 'w').write(ct)
elif op == 'decrypt':
    pt = decrypt(inp, passwd)
    open(outfile, 'w').write(pt)
