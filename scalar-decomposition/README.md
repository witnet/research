# Scalar decomposition for point-multiplication on Elliptic Curves

This algorithm computes the decomposition of an N-bit scalar in two scalars with half bit-length. The implementation of it helps to speed up the elliptic curve point multiplication.

## Motivation

The idea of using this algorithm for accelerating point multiplication is given in [*Guide to Elliptic Curve Cryptography*][link-book]. 
Given an Elliptic Curve *E*, let *&lambda;* be the root of the characteristic polynomial of an Endomorphism over *E*, and let *n* be the order of the Group of the curve. If *k* is a constant in in [0,...,n-1], then there exist *k<sub>1* and *k<sub>2* in [0,...,n-1] such that
*k=k<sub>1</sub>+k<sub>2</sub>&lambda;* mod*n*. The components *k<sub>1* and *k<sub>2* are half bit-long than *k*, making the point multiplication in *E* faster, since for every *P* in *E* we have
*kP=k<sub>1</sub> P+k<sub>2</sub>&lambda;P* mod *n*.

### Algorithm step-by-step

The goal of the algorithm is to find a vector *u=(k<sub>1</sub>,k<sub>2</sub>)* such that *f(u)=k* mod*n*, where *f* is the fuction in the integers *f(k<sub>1</sub>,k<sub>2</sub>)=k<sub>1</sub>+k<sub>2</sub>&lambda;* mod *n*.

The inputs of the algorithm are the order of the group *n*, *&lambda;* and the scalar *k* we want to decompose. In the script we use as an example the curve  `secp256k1`, and as inputs

```python
n=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
Lambda=0x5363ad4cc05c30e0a5261c028812645a122e22ea20816678df02967c1b23bd72
k=86844066927987146567678238756515930889628173209306178286953872356138621120752

```
 The first thing computed is the *extended Euclidean algorithm*, described in Section 2.2.5 of  [*Guide to Elliptic Curve Cryptography*][link-book], for *n* and *&lambda;*, which  produces a sequence of equations s<sub>i</sub>*n+t<sub>i</sub>*&lambda;=r<sub>i</sub>.  We make the sequence run while  r<sub>i</sub>&ge;&radic;n.

```python
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
```

From this sequence we take out two vectors, *v<sub>1</sub>* and *v<sub>2</sub>* such that *f(v<sub>1</sub>)=f(v<sub>2</sub>)=0*. For the vector *v<sub>2* we have two options and we will pick the one with the smallest Euclidean norm.

```python
a_1=res[3]
b_1=-res[5]
v_1=[a_1,b_1]

a_2=res[0]
b_2=-res[2]
aa_2=int(res[0])-(int(res[0])//a_1)*a_1
bb_2=-(int(res[2])-(int(res[0])//a_1)*int(res[5]))

if (a_2**2+b_2**2)<(aa_2**2+b_2**2):
    v_2=(a_2,b_2)
else:
    v_2=[aa_2,bb_2]

```

The next step is to take two constants *c<sub>1</sub>* and *c<sub>2</sub>*. The idea is that the vector *u=(k<sub>1</sub>,k<sub>2</sub>)*  will be given by the equation *u=(k,0)-c<sub>1</sub>v<sub>1</sub>-c<sub>2</sub>v<sub>2</sub>*.

```python
c_1=(v_2[1]*k+n//2)//n

c_2=(-v_1[1]*k+n//2)//n
```

Finally we construct the constants *k<sub>1</sub>* and *k<sub>2</sub>*.

```python
k_1=(k-c_1*a_1-c_2*int(v_2[0]))%n
k_2=(-c_1*b_1-c_2*int(v_2[1]))%n 
k11=str(k_1)
k22=str(k_2)


if abs(k_1)>n//2:
    k_1=k_1-n

if abs(k_2)>n//2:
    k_2=k_2-n

```

## Deployment

To Deploy the algorithm you just need to run the script in Python3. In this case we have already written the inputs for the Elliptic Curve `secp256k1`.

## Example

For the Elliptic Curve `P-160`, given the inputs

```python
n=1461501637330902918203687013445034429194588307251
lam=903860042511079968555273866340564498116022318806
k=965486288327218559097909069724275579360008398257

```

the decomposition of *k* turns out to be

```python
k_1= -98093723971803846754077
k_2= 381880690058693066485147

```

## License

Witnet research documentation is published under the [GNU Free Documentation License v1.3][license].

Witnet research software is published under the [GNU General Public License v3.0][license-gpl].

[license]: https://github.com/witnet/research/blob/master/LICENSE
[license-gpl]: https://github.com/witnet/research/blob/master/LICENSE-GPL
[reputation]: https://github.com/witnet/research/blob/master/reputation/index.md
[link-book]: http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.394.3037&rep=rep1&type=pdf
