from math import gcd
from random import randrange, random
from collections import namedtuple
from math import log
from binascii import hexlify, unhexlify
import pickle

def is_prime(n):
    """
    Miller-Rabin primality test.
 
    A return value of False means n is certainly not prime. A return value of
    True means n is very likely a prime.
    """
    if n!=int(n):
        return False
    n=int(n)
    #Miller-Rabin test for prime
    if n==0 or n==1 or n==4 or n==6 or n==8 or n==9:
        return False
 
    if n==2 or n==3 or n==5 or n==7:
        return True
    s = 0
    d = n-1
    while d%2==0:
        d>>=1
        s+=1
    assert(2**s * d == n-1)
 
    def trial_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2**i * d, n) == n-1:
                return False
        return True  
 
    for i in range(100):
        a = randrange(2, n)
        if trial_composite(a):
            return False
 
    return True  

def randprime(N=10**8):
    p = 1
    while not is_prime(p):
        p = randrange(N)
    return p

def findelement(prime):
	element=random()*(prime-1)	
	b=int(element)
	return b

def keygen(N, public=None):
	prime=randprime(N)
	x=findelement(prime)
	alpha=findelement(prime)
	y=pow(alpha,x,prime)
	return (x,prime),(y,alpha,prime)

def findrandom(prime):
	k=randrange(1,prime-1)
	while(gcd(k,prime-1)!=1):
		k=k+1
	return k

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

def blind(msg,pubkey):
    m = hexlify(msg.encode())
    m = int(m,16)
    k=findrandom(pubkey[2])
    r=pow(pubkey[1],k,pubkey[2])

    h=findrandom(pubkey[2])
    print ("Real Message: " + msg)
  
    blindmsg=(h*m) % (pubkey[2]-1)
    print(f'blindmsg returned is : {blindmsg}')

    return k,r,h,blindmsg

def signature(blindmsg,privkey,k,r):

    #print ("Blinded Message "+ str(msg))
    signedBlind=((blindmsg-privkey[0]*r)*multinv(privkey[1]-1,k)) % (privkey[1]-1)
    print(f'signblind returned is : {signedBlind}')

    return signedBlind

def unblind(msg,pubkey,k,r,h,blindmsg):
	
	#print ("Signed Blinded Message "+ str(msg))
	sdash=msg
	s=((multinv(pubkey[2]-1,h)-1)*blindmsg*multinv(pubkey[2]-1,k)+sdash)% (pubkey[2]-1)
  
	return s

def verefy(msg,signedmsg,pubkey,r):
    print("=========================")
    print(msg)
    print(pubkey[0])
    print(pubkey[1])
    print(pubkey[2])


    print("=========================")

    m= msg
    s= signedmsg
    a=pow(pubkey[1],m,pubkey[2])
    b=(pow(pubkey[0],r,pubkey[2])*pow(r,s,pubkey[2]))%pubkey[2]
    print(f'msg a is : {a}')
    print(f'msg b is : {b}')


if __name__ == '__main__':
	
    
    privkey, pubkey = keygen(2**128)

    """infile = open("keys/elgampub",'wb')
    pickle.dump(pubkey,infile)
    outfile = open("keys/elgampriv","wb")
    pickle.dump(privkey,outfile)
    infile.close()
    outfile.close()
    """


    ifile = open("keys/elgampub","rb")
    pubkey = pickle.load(ifile)
    ifile = open("keys/elgampriv","rb")
    privkey = pickle.load(ifile)
    msg = "8a7e9481cd3a2431eb6efc93695498ad"
    msg2 = "89a4acde0a5aacd2a70e53ca86d0ca32"
    m = int(hexlify(msg.encode()),16)
    

    print(f'm is: {m}')

    print(pubkey[1])
    print(pubkey[2])


    k,r,h,blindmsg=blind(msg,pubkey)
    print(r)
	
    #Alice (Signer) will do the following
    sig = signature(blindmsg,privkey,k,r)

	#Bob receives the blinded signed message and unblinds it
    ubsig = unblind(sig,pubkey,k,r,h,blindmsg)
    print(f'ubsig is : {ubsig}')
    verefy(m,ubsig,pubkey,r)
