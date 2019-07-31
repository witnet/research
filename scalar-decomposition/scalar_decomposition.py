#Scalar decomposition for point multiplication in Elliptic curves.
#
#Given a scalar k in an Group of an Elliptic curve of orden n, this algorithm decompose k in two scalars k_1 and k_2, both having half bit-lentgh than k. 
#More precisely, given an Elliptic curve E, let lambda be a root of the characteristic polynomial of an endomorphism over E, then
#                    k=k_1+k_2*lambda %n
#
#The algorithm is explained with more detail in http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.394.3037&rep=rep1&type=pdf


import math


#The inputs are the order of the group n, lambda, and the scalar we want to decompose k
#example EC secp256k1
n=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
lam=0x5363ad4cc05c30e0a5261c028812645a122e22ea20816678df02967c1b23bd72
print('The scalar k to be decompose')
k=int(input())

#The Euclidean algorithm is used for a=n and b=lambda. This algorithm produces a sequence of equations s_i*n+t_i*lambda=r_i, we make the sequence go while  r_i>=sqrt(n).

def extended_euclid_gcd(a, b):
    s = 0; old_s = 1
    t = 1; old_t = 0
    r = b; old_r = a
    
    while r >= math.sqrt(n):
        quotient = old_r//r 
    
        old_r, r = r, old_r - quotient*r
        old_s, s = s, old_s - quotient*s
        old_t, t = t, old_t - quotient*t
    return [old_r, old_s, old_t,r,s,t]
   
res = extended_euclid_gcd(n, lam)

#Construction of the vectors v_1 and v_2 

a_1=res[3]
b_1=-res[5]
v_1=[a_1,b_1]

#For the vector v_2 we choose the components whose euclidean norm is smaller

a_2=res[0]
b_2=-res[2]
aa_2=int(res[0])-(int(res[0])//a_1)*a_1
bb_2=-(int(res[2])-(int(res[0])//a_1)*int(res[5]))

if (a_2**2+b_2**2)<(aa_2**2+b_2**2):
    v_2=(a_2,b_2)
else:
    v_2=[aa_2,bb_2]



#Constructions of the constants c_1 andc_2

c_1=(v_2[1]*k+n//2)//n
c_2=(-v_1[1]*k+n//2)//n


#Construction of k_1 and k_2, which are the decomposition of k, since k=k_1+k_2*lambda %n

k_1=(k-c_1*a_1-c_2*int(v_2[0]))%n
k_2=(-c_1*b_1-c_2*int(v_2[1]))%n 

if abs(k_1)>n//2:
    k_1=k_1-n

if abs(k_2)>n//2:
    k_2=k_2-n
    

print(k_1,k_2)



