pragma solidity ^0.5.0;

/*Given a scalar k in an Group of an Elliptic curve of orden n, this algorithm decompose k in two scalars k_1 and k_2, both having half bit-lentgh than k. 
More precisely, given an Elliptic curve E, let lambda be a root of the characteristic polynomial of an endomorphism over E, then
                    k=k_1+k_2*lambda %n

The algorithm is explained with more detail in http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.394.3037&rep=rep1&type=pdf*/


contract ScalarDecompose {
// The inputs are the order of the group n and lambda of the EC secp256k1
  uint256 n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141;
  uint256 constant lambda = 0x5363ad4cc05c30e0a5261c028812645a122e22ea20816678df02967c1b23bd72;

// This fuction is needed to multiply two 256-bites-long scalars
  function mul256By256(uint a, uint b)
        internal pure
        returns (uint ab32, uint ab1, uint ab0)
    {
        uint ahi = a >> 128;
        uint alo = a & 2**128-1;
        uint bhi = b >> 128;
        uint blo = b & 2**128-1;
        ab0 = alo * blo;
        ab1 = (ab0 >> 128) + (ahi * blo & 2**128-1) + (alo * bhi & 2**128-1);
        ab32 = (ab1 >> 128) + ahi * bhi + (ahi * blo >> 128) + (alo * bhi >> 128);
        ab1 &= 2**128-1;
        ab0 &= 2**128-1;
    }
// This fuction is needed to divide two 256-bites-long scalars
  function div256_128By256(uint a21, uint a0, uint b)
        internal pure
        returns (uint q, uint r)
    {
        uint qhi = (a21 / b) << 128;
        a21 %= b;

        uint shift = 0;
        while(b >> shift > 0) shift++;
        shift = 256 - shift;
        a21 = (a21 << shift) + (shift > 128 ? a0 << (shift - 128) : a0 >> (128 - shift));
        a0 = (a0 << shift) & 2**128-1;
        b <<= shift;
        (uint256 b1, uint256 b0) = (b >> 128, b & 2**128-1);

        uint rhi;
        q = a21 / b1;
        rhi = a21 % b1;

        uint rsub0 = (q & 2**128-1) * b0;
        uint rsub21 = (q >> 128) * b0 + (rsub0 >> 128);
        rsub0 &= 2**128-1;

        while(rsub21 > rhi || rsub21 == rhi && rsub0 > a0) {
            q--;
            a0 += b0;
            rhi += b1 + (a0 >> 128);
            a0 &= 2**128-1;
        }

        q += qhi;
        r = (((rhi - rsub21) << 128) + a0 - rsub0) >> shift;
    }




function  sqrt(uint x) internal pure returns (uint y) {
    uint z = (x + 1) / 2;
    y = x;
    while (z < y) {
        y = z;
        z = (x / z + z) / 2;
    }
}
function abs(int256 x) internal pure returns (int256) {
    if(x >= 0) return x;
    return -x;
  }


function scalarDecomposition (uint256 k) public returns (int256[2] memory) {
    
// Extended Euclidean Algorithm for n and lambda
    int256 t = 1;
    int256 old_t = 0;
    uint256 r = uint256(lambda);
    uint256 old_r = uint256(n);
    uint256 quotient;


   while (uint256(r) >= sqrt(n)) {
      uint256 quotient = old_r / r;
      (old_r, r) = (r, old_r - quotient*r);
      (old_t, t) = (t, old_t - int256(quotient)*t);
      
      
    }
// the vectors v1=(a1, b1) and v2=(a2,b2)
    int256[4] memory a_b;
    a_b[0] = int256(r);
    a_b[1] = int256(0 - t);
    a_b[2] = int256(old_r);
    a_b[3] = 0-old_t;

   //b2*K
    uint[3] memory test;
    (test[0],test[1], test[2]) = mul256By256(uint(a_b[3]), uint(k));

   //-b1*k
    uint[3] memory test2;
    (test2[0],test2[1], test2[2]) = mul256By256(uint(-a_b[1]), uint(k)); 

    //c1 and c2
    uint[2] memory c1;
    (c1[0],c1[1]) = div256_128By256(uint256 ( uint128 (test[0])) << 128 | uint128 (test[1]), uint256(test[2]) + (n / 2), n);
  
    uint[2] memory c2;
    (c2[0],c2[1]) = div256_128By256(uint256 ( uint128 (test2[0])) << 128 | uint128 (test2[1]), uint256(test2[2]) + (n / 2), n);

    // the decomposition of k in k1 and k2
    int256 k1 = int256((int256(k) - int256(c1[0]) * int256(a_b[0]) - int256(c2[0]) * int256(a_b[2])) % int256(n));
    int256 k2 = int256((-int256(c1[0]) * int256(a_b[1]) - int256(c2[0]) * int256(a_b[3])) % int256(n));
    
    if (uint256(abs(k1)) <= (n / 2)){
      k1 = k1;
    }
    else{
      k1 = int256(uint256(k1) - n);
    }
    if (uint256(abs(k2)) <= (n / 2)){
      k2 = k2;
    }
    else{
      k2 = int256(uint256(k2) - n);
    }

     return [k1, k2];
  }




}