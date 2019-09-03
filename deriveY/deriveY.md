# `deriveY` and quadratic residue

Suppose we have an elliptic curve *E* over *Z<sub>P</sub>*, with *P* a prime, given by the equation *y<sup>2</sup>=x<sup>3</sup>+ax<sup>2</sup>+b*. Then knowing *x* there are two results from the equation of the curve, *y* and *-y*. The parity byte of *y*, 0x02 even, 0x03 odd, is enough to know which of the two results is the *y* we need. This is what the `deriveY` function does, revels *y* having as inputs the compressed form of *y* and *x*. 
The main part of the function relies on computing the quadratic residue modulus *P*, this is resolving something like *y<sup>2</sup> = n mod (P)*. This can be done using different algorithms, the library `EllipticCurve.sol` uses the computation of *n<sup>(p + 1)/4</sup>*, but this only works for Elliptic Curves having  `P = 3 mod(4)`.

```solidity
pragma solidity ^0.5.0;

import "./EllipticCurve.sol";

contract Secp256k1 is EllipticCurve {

    function deriveY(
    uint8 prefix,
    uint256 x,
    uint256 a,
    uint256 b,
    uint256 pp)
  public pure returns (uint256 y)
  {
    // x^3 + ax + b
    uint256 y2 = addmod(mulmod(x, mulmod(x, x, pp), pp), addmod(mulmod(x, a, pp), b, pp), pp);
    uint256 y_ = expMod(y2, (pp + 1) / 4, pp);
    // uint256 cmp = yBit ^ y_ & 1;
    y = (y_ + prefix) % 2 == 0 ? y_ : pp - y_;
  }
}
```

## Case `p=1(4)`

For Elliptic Curves in which `P=1(4)` there are others algorithms that compute the modular square root. In fact they are more general algorithms so they could be implemented for all the Elliptic Curves the library supports, but the computational costs are higher than for the current function `deriveY`.

The most commun algorithms for computing the *n* square root module *P*  are the *Tonelli-Shanks* and the *Cipolla*'s algorithm. Because in the `EllipticCurve.sol` library the only curve that satisfies `P= 1 mod 4` is `Secp224r1` we will focus on its characteristics. In this curve the value of *P* is 2<sup>224</sup> -2<sup>96</sup>+1, so *P = 1 (4)*.
The computational cost of the algortihms depends on the relation between the bit-length *m* of the prime *P* and *S*, being *S* the biggest exponent such that *p-1=Q2<sup>S</sup>*, where *Q* is odd. More preciscely the *Cipolla*'s algorithm is more efficient than the *Tonelli-Shanks* if and only if *S(S-1)>mP+20*. 
For `Secp224r1` we have *S=96* and *m=256*, making the *Cipolla*'s algorithm the best option. More ditails can be found in [*Square Root Modulo P*][link-post2].

## Idea of the Cipolla's algorithm

Suppose we want to compute the modular square root *r<sup>2</sup> = n mod(p)*. We first need to know that the *Legendre*'s symbol states if an element is a square or if its not by applying the *Euler*'s criterion which states that an element *a<sup>(p-1)/2* is equal to 1 if *a* is quadratic residue modulus *P* and is equal to -1 if it's not.

There are two main steps in the algorithm:

1) First we nedd to find an element *a* of *Z<sub>p</sub>* such that *a<sup>2</sup> - n* is not a square. This can easly be done by applying the *Legendre*'s symbol. In fact half of the elements of *Z<sub>P</sub>* are nonquadratic residue.
2) Second we compute *x= (a + (a<sup>2</sup>-n)<sup>1/2</sup>)<sup><sup>(p+1)/2</sup></sup>*  in the field extention *F<sub>P</sub>(( a<sup>2</sup>-n)<sup>1/2</sup>)*. The resulting *x* will satisfy *x<sup>2</sup>=n mod(p)*.

After finding *a*, the number of operations required for the algorithm is *4m+2k-4* multiplications,  *4m-2* sums, where *m* is the number of digits in the binary representation of *P* and *k* is the number of ones in this representation.

A code in Python for the algorithm can be found in this [*post*][link-post].

## Conclusion

The computational cost of the algorithm is a big disadvantage for the `deriveY` function for curves having *P = 1 mod 4*, the cumbersome extension field arithmetic needed make the implementation in Solidity difficoult to achive.
As mentioned above, the Elliptic Curve library has been tested for serveral curves and just the `Secp224r1` satisfies this condition, so for now we will keep using the `deriveY` function as it is. Note that `deriveY` is just an auxiliary function, and thus does not limit the functionality of curve arithmetic operations.


[link-post]: https://rosettacode.org/wiki/Cipolla%27s_algorithm
[link-post2]:http://www.cmat.edu.uy/~tornaria/pub/Tornaria-2002.pdf