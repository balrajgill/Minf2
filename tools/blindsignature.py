from random import randrange, random
from collections import namedtuple
from math import log, gcd
from binascii import hexlify, unhexlify
import pickle
def is_prime(n, k=30):
    if n <= 3:
        return n == 2 or n == 3
    neg_one = n - 1

    s, d = 0, neg_one
    while not d & 1:
        s, d = s+1, d>>1
    assert 2 ** s * d == neg_one and d & 1

    for i in range(k):
        a = randrange(2, neg_one)
        x = pow(a, d, n)
        if x in (1, neg_one):
            continue
        for r in range(1, s):
            x = x ** 2 % n
            if x == 1:
                return False
            if x == neg_one:
                break
        else:
            return False
    return True

def randprime(N=10**8):
    p = 1
    while not is_prime(p):
        p = randrange(N)
    return p

def multinv(modulus, value):
    x, lastx = 0, 1
    a, b = modulus, value
    while b:
        a, q, b = b, a // b, a % b
        x, lastx = lastx - q * x, x
    result = (1 - lastx * modulus) // value
    if result < 0:
        result += modulus
    assert 0 <= result < modulus and value * result % modulus == 1
    return result

KeyPair = namedtuple('KeyPair', 'public private')
Key = namedtuple('Key', 'exponent modulus')

def keygen(N, public=None):
    prime1 = randprime(N)
    prime2 = randprime(N)
    composite = prime1 * prime2
    totient = (prime1 - 1) * (prime2 - 1)
    if public is None:
        while True:
            private = randrange(totient)
            if gcd(private, totient) == 1:
                break
        public = multinv(totient, private)
    else:
        private = multinv(totient, public)
    assert public * private % totient == gcd(public, totient) == gcd(private, totient) == 1
    assert pow(pow(1234567, public, composite), private, composite) == 1234567
    return KeyPair(Key(public, composite), Key(private, composite))

def signature(msg, privkey):

    coded = pow(int(msg), *privkey)% privkey[1]  #basically implement this in smart contract
    print(privkey)
    #coded1 = pow(int(msg), *privkey)
    #coded2 = pow(int(msg), privkey[0], privkey[1])
    print("-------")
    #print(str(coded)[0:100])
    #print(str(coded1)[0:100])
    #print(str(coded2)[0:100])
    
    #print(coded==coded1)
    #print(coded==coded2)
    #print()
    #print("-------")
    return coded


def blindingfactor(N):
    b=random()*(N-1)
    r=int(b)
    while (gcd(r,N)!=1):
        r=r+1
    return r

def blind(msg,pubkey):
    
    r = blindingfactor(pubkey[1])
    m = hexlify(msg.encode())
    m = int(m,16)
    blindmsg=(pow(r,*pubkey)*m)% pubkey[1]
 

    return (r,blindmsg)

def unblind(msg,r,pubkey):

    bsm=int(msg)
    ubsm=(bsm*multinv(pubkey[1],r))% pubkey[1]
    
    return ubsm
	

def verify(msg,r,pubkey):
    #print ("Message After Verification")
    #print(str(pow(int(msg),*pubkey)%pubkey[1]))
    return pow(int(msg),*pubkey)%pubkey[1]

if __name__ == '__main__':
    
    #pubkey, privkey = keygen(2 ** 512)
    
    ifile = open("pub","rb")
    pubkey = pickle.load(ifile)
    ifile = open("priv","rb")
    privkey = pickle.load(ifile)
    
    
    """infile = open("keys/pub1",'wb')
    pickle.dump(pubkey,infile)
    outfile = open("keys/priv1","wb")
    pickle.dump(privkey,outfile)
    infile.close()
    outfile.close()"""


    
    msg = "testing"
    r,blindmsg=blind(msg,pubkey)

    #Alice receives the blind message and signs it
    
    sig = signature(blindmsg, privkey)

    #Bob recieves the signed message and unblinds it
    ubsig = unblind(sig,r,pubkey)
    
    #verifier verefis the message
    
    ver = verify(ubsig,r,pubkey)

    msg2 = bytes.fromhex(hex(ver)[2:])
    m = int(hexlify(msg.encode()),16)
    print(f'msg is : {m}')
    print(f'blindmsg is: {blindmsg}')
    print(f'sig is: {sig}')
    print(f'ubsig is: {ubsig}')
    print(f'ver is: {ver}')
    