import random

# get order of magnitude of a number
def magnitude(number):
	res = 0
	while number > 0:
		res += 1
		number //= 10
	return res

# generate RSA key pair
def generateKeys():
    #Generate private and public keys

	f = open("../primes/primes7dig.txt")
	goodPrimes = f.readlines()
	f.close()

	f = open("../primes/primes.txt")
	primes = f.readlines()
	f.close()

	p, q, N = 0, 0, 0
	while (q == p or str(N)[0]!= "9"):
		p, q = int(random.choice(goodPrimes)[:-1]), int(random.choice(goodPrimes)[:-1])
		N = p*q
	
	d = (p-1)*(q-1)
	
	e = d
	mdc = 0

	while not(e < d and mdc==1):
		e = int(random.choice(primes)[:-1])
		if (e < d):
			saund = saunderson(d, e)
			mdc = saund[0]
			revE = saund[2]%d

	privateKey = (N, revE)
	mypublicKey = (N, e)
	
	return(privateKey, mypublicKey)

# find correspondent key
def crackKey(key):
	N = key[0]
	e = key[1]

	f = open("../primes/primes.txt")
	primes = f.readlines()
	f.close()

	for line in primes:
		a = int(line[:-1])
		if N%a == 0:
			p = a
			q = N / a
	
	d = (p-1)*(q-1)
	revE = int(saunderson(d, e)[2] % d)
	private = (N, revE)
	return private

# Find GCD and Bezout coefficients
def saunderson(bigger, smaller):
	# out: (GCD, Bezout bigger, Bezout smaller)
	if smaller > bigger:
		print("saunderson: invalid arguments.")
		return (0, 0, 0)

    #first iteration
	saund = [
		(bigger, 0, 1, 0),
		(smaller, bigger//smaller, 0, 1)
	]

	currIndx = 2
	nextRemainder = saund[currIndx-2][0] % saund[currIndx-1][0]

	while(nextRemainder != 0):
		quotient = saund[currIndx-1][0] // nextRemainder
		bezoutB  = saund[currIndx-2][2] - (saund[currIndx-1][1]*saund[currIndx-1][2])
		bezoutS  = saund[currIndx-2][3] - (saund[currIndx-1][1]*saund[currIndx-1][3])

		newLine = (nextRemainder, quotient, bezoutB, bezoutS)
		saund += [newLine]

		currIndx += 1
		prevRemainder = nextRemainder
		nextRemainder = saund[currIndx-2][0] % saund[currIndx-1][0]

	return (prevRemainder, bezoutB, bezoutS)

# decompose in powers of two
def powerOfTwo(number, factors):
	if number == 0:
		return factors
	else:
		prev = 1
		test = 2
		#Find greatest power of 2 that is lesser than number
		while test <= number:
			prev = test
			test *= 2

		return powerOfTwo(number-prev, [prev] + factors)

# apply RSA algorithm
def RSA(value, key):
	mod = key[0]
	exp = key[1]

	pot2 = powerOfTwo(exp, [])

	ind = 1
	res = 1
	currPot = value

	while ind <= pot2[len(pot2)-1]:
		if ind in pot2:
			res = (res*currPot)%mod
		ind *= 2
		currPot = (currPot*currPot)%mod

	return res
