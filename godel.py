#!/usr/bin/python
#
# create and decode Godel numbers
#

#import numpy as np
import sys
import unittest

MAX=500
debug=False

class simpleTest(unittest.TestCase):
  def setUp(self):
    pass

  def test_sum(self):
    self.assertEqual( sum(set(5), set(5)), set(10))
    self.assertEqual( sum(set(1), set(1)), set(2))
    self.assertEqual( sum(set(0), set(0)), set(0))
    self.assertEqual( sum(set(0), set(1)), set(1))

  def test_sub(self):
    self.assertEqual( sub( set(2), set(2)) , set(0) )

  def test_mult(self):
    for i in range(10):
      for j in range(10):
        self.assertEqual( set(i*j), mult( set(i), set(j) ) )

  def test_div(self):
    self.assertEqual([10, True], div( set(20), set(2)))
    self.assertEqual([11, False], div( set(21), set(2)))
    self.assertEqual([1, True], div( set(5), set(5)))

  def test_pow(self):
    self.assertEqual( set(2), pow(set(2),set(1)))
    self.assertEqual( set(1), pow(set(2),set(0)))

  def test_ten(self):
    self.assertEqual( 10, ten(set(10)))

  def test_gt(self):
    self.assertTrue( gt(set(5), set(1)) )
    self.assertFalse( gt(set(1), set(5)))

  def test_lt(self):
    self.assertTrue( lt(set(1), set(5)))
    self.assertFalse( lt(set(5), set(1)))

  def test_pad(self):
    self.assertEqual( set(2), pad([1,0]))

  def test_unpad(self):
    self.assertEqual( unpad(set(2)), [1,0])

  def test_fdiv(self):
    self.assertEqual( fdiv(set(10), set(2) )[0], set(5))
    self.assertEqual( fdiv(set(11), set(2) )[2], False)
    self.assertEqual( fdiv(set(12), set(2) )[0], set(6))
    self.assertEqual( fdiv(set(565950), set(2) )[0], set(282975))
    self.assertEqual( fdiv(set(224), set(2) )[0], set(112))

  def test_fmult(self):
    self.assertEqual( fmult(set(10), set(2)), set(20))
    self.assertEqual( fmult(set(15), set(3)), set(45))
    self.assertEqual( fmult(set(0), set(2)), set(0))
    self.assertEqual( fmult(set(99), set(99)), set(9801))



def ten(n):
  m=MAX-1
  z=0
  t=0
  while m >= 0:
    t = t + n[m] * 2**z
    m = m -1
    z = z + 1
  return t

def set(n):
  ret = []
  m=MAX-1
  while m >=0:
    if 2**m <= n:
      ret.append(1)
      n = n - 2**m
    else:
      ret.append(0)
    m = m -1

  return ret

one = set(1)
zero = set(0)

def fmult(b1,b2):

  # get rid of any un-needed leading zeros
  b1 = unpad(b1)
  b2= unpad(b2)

  # if either set is empty it's a zero, so
  # zero times anything is zero, so just
  # return zero
  if b1 == [] or b2 == []:
    return set(0)

  # [:] deep copy
  # we want b2 to be the shorter of the two numbers
  if len(b2) > len(b1):
    b3 = b1[:]
    b1 = b2[:]
    b2 = b3[:]

  # every time you pick a new number from the bottom
  # you move over one
  inc=0

  # the final answer
  runningSum = set(0)

  # while the bottom number still has bits to take
  while len(b2) != 0:

    # grab the current bit from the right
    currentbit = b2.pop()

    # if the bit is 1, then add the right side padding based on
    # what position we are in (determined by inc) and then
    # add that to the running total.  If the bit is 0, then
    # everything works out to be zero, so we don't need to do
    # anything (yay binary math.)
    if currentbit == 1:
      # print "sum of:", unpad(runningSum), " and " , b1 + [0]*inc

      # [0] * inc says, if we are the 2nd number in, then append [0,0]
      # to the current number. so if the current number was [1,0] the
      # final result would be [1,0,0,0]  and that is added to the
      # running sum
      runningSum = sum(runningSum, b1 + [0]*inc)

    # increase the counter by one
    inc = inc + 1

  return runningSum

def sub(b1,b2):
  b1 = pad(b1)
  b2 = pad(b2)

  z = [1,0]
  comp = map(lambda x: z[x], b2)
  return inc(sum(b1, comp))


def sum(b1,b2):
  m = MAX-1
  c = 0
  ret = set(0)

  b1 = pad(b1)
  b2 = pad(b2)

  while m >=0:
    t = b1[m] + b2[m] + c
    if t==0 or t==1:
      ret[m] = t
      c=0
    if t==2:
      ret[m] = 0
      c = 1
    if t==3:
      ret[m] = 1
      c = 1
    m = m - 1

  return ret

def mult(b1,b2):
  tot = set(0)
  while  b2 != zero:
    tot = sum( b1,tot)
    b2 = dec(b2)
  return tot

def pow(b1,b2):

  if b2 == zero:
    return one

  tot = b1[:]
  while b2 != one:
    tot = fmult(tot[:],b1[:])
    # print "tot:", unpad(tot), " b1:", unpad(b1), " b2:" , unpad(b2)
    b2 = dec(b2)
  return tot

def pad(b1):
  while len(b1) != MAX:
    b1.insert(0,0)
  return b1

def unpad(b1):
  if b1 == []:
    return []
  while True:
    if b1[0] == 0:
      b1.pop(0)
      if len(b1) ==0:
        return []
    else:
      return b1

def fdiv(b1,b2):

  if b1==b2:
    return [set(1),[],True]

  b2 = unpad(b2)
  b1 = unpad(b1)
  div = []
  ans = []

  if b1 == []:
    return set(0)
  if b2 == []:
    return set(0)

  while True:
    div.append( b1.pop(0) )
    div = unpad(div)
    if div == b2:
      div = []
      ans.append(1)
      if debug: print "= :", " div:", div, " b2", b2, " ans:", ans
    elif gt(div[:], b2[:]):
      div = unpad( sub(div[:], b2[:]) )
      ans.append(1)
      if debug: print "gt :", " div:", div, " b2", b2, " ans:", ans
    else:
      ans.append(0)
      if debug: print "0 :", " div:", div, " b2", b2, " ans:", ans

    if len(b1) == 0:
      break

  if div == [] or div == [0]:
    return [pad(ans),div,True]
  else:
    return [pad(ans),div,False]


def div(b1,b2):
  if b1 == b2:
    return [1, True]

  c = 1
  t = sub(b1,b2)

  while t[0] != 1:
    c = c + 1
    t = sub(t,b2)
    if t == zero:
      return [c, True]
  return [c,False]

def inc(b1):
  return sum(b1, one)

def dec(b1):
  return sub(b1,one)

# is b1 > b2
def gt(b1,b2):
  b1 = pad(b1)
  b2 = pad(b2)

  i = 0
  while i < MAX:
    if b1 > b2:
      return True
    i = i + 1

  return False

# me lazy
def lt(b1,b2):
  return not gt(b1,b2)

#unittest.main()
#sys.exit()

tab = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
map2 = dict(zip(tab.values(), tab.keys()))

primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149]

make="aabcaccdadcbabccd"

a = set(1)
z = 1

print "creating godel number"
for i in range(len(make)):
  #print primes[i], tab[make[i]]
  z = z * primes[i] ** tab[make[i]]
  # print unpad(a), primes[i], tab[make[i]]
  a =  fmult(a, pow(
            set(primes[i]),
            set(tab[make[i]]
              )))

#print z
#print set(z)
#print a
#print ten(a)

print "writing to file"
myfile = open("out.txt", "w")
myfile.write( ",".join(map(str,unpad(a))) + "\n" )

print "deconstructing number"
i=0
x=0
while a != one:
  t = fdiv(a[:], set(primes[i]))
  if t[2] == False:
    #print ten(a), primes[i]
    print i, map2[x]
    myfile.write( ",".join(map(str,unpad(a))) + "\n" )
    x = 0
    i = i +1
  else:
    a = t[0]
    x = x + 1
    ##print "tic"

print i,map2[x]
myfile.write( ",".join(map(str,unpad(a))) + "\n" )
myfile.close()
