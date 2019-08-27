pragma solidity ^0.5.0;

/*Given a scalar k in an Group of an Elliptic curve of orden n, this algorithm decompose k in two scalars k_1 and k_2, both having half bit-lentgh than k. 
More precisely, given an Elliptic curve E, let lambda be a root of the characteristic polynomial of an endomorphism over E, then
                    k=k_1+k_2*lambda %n

The algorithm is explained with more detail in http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.394.3037&rep=rep1&type=pdf*/

/**
 * @title Scalar decompostion in Solidity
 * @dev This algorithm computes the decomposition of an N-bit scalar in two scalars with half bit-length
 * @author Witnet Foundation
 */


contract ScalarDecompose {

  uint256 n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141;
  uint256 constant LAMBDA = 0x5363ad4cc05c30e0a5261c028812645a122e22ea20816678df02967c1b23bd72;

  /// @dev Decomposition of the scalar k in two scalars k1 and k2 with half bit-length, such that k=k1+k2*LAMBDA (mod n)
  /// @param _k the scalar to be decompose
  /// @return k1 and k2  such that k=k1+k2*LAMBDA (mod n)
  function scalarDecomposition (uint256 _k) public view returns (int256[2] memory) {
  // Extended Euclidean Algorithm for n and LAMBDA
    int256 t = 1;
    int256 oldt = 0;
    uint256 r = uint256(LAMBDA);
    uint256 oldr = uint256(n);
    uint256 quotient;

    while (uint256(r) >= sqrt(n)) {
      quotient = oldr / r;
      (oldr, r) = (r, oldr - quotient*r);
      (oldt, t) = (t, oldt - int256(quotient)*t);
    }
  // the vectors v1=(a1, b1) and v2=(a2,b2)
    int256[4] memory ab;
    ab[0] = int256(r);
    ab[1] = int256(0 - t);
    ab[2] = int256(oldr);
    ab[3] = 0-oldt;

  //b2*K
    uint[3] memory test;
    (test[0],test[1], test[2]) = multiply256(uint(ab[3]), uint(_k));

  //-b1*k
    uint[3] memory test2;
    (test2[0], test2[1], test2[2]) = multiply256(uint(-ab[1]), uint(_k));
  //c1 and c2
    uint[2] memory c1;
    (c1[0],c1[1]) = bigDivision(uint256 (uint128 (test[0])) << 128 | uint128 (test[1]), uint256(test[2]) + (n / 2), n);

    uint[2] memory c2;
    (c2[0],c2[1]) = bigDivision(uint256 (uint128 (test2[0])) << 128 | uint128 (test2[1]), uint256(test2[2]) + (n / 2), n);

  // the decomposition of k in k1 and k2
    int256 k1 = int256((int256(_k) - int256(c1[0]) * int256(ab[0]) - int256(c2[0]) * int256(ab[2])) % int256(n));
    int256 k2 = int256((-int256(c1[0]) * int256(ab[1]) - int256(c2[0]) * int256(ab[3])) % int256(n));
    if (uint256(abs(k1)) <= (n / 2)) {
      k1 = k1;
    } else {
      k1 = int256(uint256(k1) - n);
    }
    if (uint256(abs(k2)) <= (n / 2)) {
      k2 = k2;
    } else {
      k2 = int256(uint256(k2) - n);
    }

    return [k1, k2];
  }

  /// @dev Multiplication of a uint256 a and uint256 b. Because in Solidity each variable can not be greater than 256 bits,
  /// this function separates the result of the multiplication in three parts, so the result would be the concatenation of those three
  /// @param _a uint256
  /// @param _b uint256
  /// @return (ab2, ab1, ab0)
  function multiply256(uint256 _a, uint256 _b) internal pure returns (uint256, uint256, uint256) {
    uint256 aM = _a >> 128;
    uint256 am = _a & 2**128-1;
    uint256 bM = _b >> 128;
    uint256 bm = _b & 2**128-1;
    uint256 ab0 = am * bm;
    uint256 ab1 = (ab0 >> 128) + (aM * bm & 2**128-1) + (am * bM & 2**128 - 1);
    uint256 ab2 = (ab1 >> 128) + aM * bM + (aM * bm >> 128) + (am * bM >> 128);
    ab1 &= 2**128 - 1;
    ab0 &= 2**128 - 1;

    return (ab2, ab1, ab0);
  }

  /// @dev Division of an integer of 312 bits by a 256-bit integer
  /// @param _aM the higher 256 bits of the numarator
  /// @param _am the lower 128 bits of the numarator
  /// @param _b the 256-bit denominator
  /// @return q the result of the division and the rest r
  function bigDivision(uint256 _aM, uint256 _am, uint256 _b) internal pure returns (uint256, uint256) {
    uint256 qM = (_aM / _b) << 128;
    uint256 aM = _aM % _b;

    uint256 shift = 0;
    while (_b >> shift > 0) {
      shift++;
    }
    shift = 256 - shift;
    aM = (_aM << shift) + (shift > 128 ? _am << (shift - 128) : _am >> (128 - shift));
    uint256 a0 = (_am << shift) & 2**128-1;
    uint256 b = _b << shift;
    (uint256 b1, uint256 b0) = (b >> 128, b & 2**128-1);

    uint256 rM;
    uint256 q = aM / b1;
    rM = aM % b1;

    uint256 rsub0 = (q & 2**128-1) * b0;
    uint256 rsub21 = (q >> 128) * b0 + (rsub0 >> 128);
    rsub0 &= 2**128-1;

    while (rsub21 > rM || rsub21 == rM && rsub0 > a0) {
      q--;
      a0 += b0;
      rM += b1 + (a0 >> 128);
      a0 &= 2**128-1;
    }

    q += qM;
    uint256 r = (((rM - rsub21) << 128) + _am - rsub0) >> shift;

    return (q, r);
  }

  /// @dev Sqare root of an 256-bit integer
  /// @param _x the integer
  /// @return y the square root of _x
  function  sqrt(uint256 _x) internal pure returns (uint256) {
    uint256 z = (_x + 1) / 2;
    uint256 y = _x;
    while (z < y) {
      y = z;
      z = (_x / z + z) / 2;
    }
    return (y);
  }

  /// @dev Absolute value of a 25-bit integer
  /// @param _x the integer
  /// @return _x if _x>=0 or -_x if not
  function abs(int256 _x) internal pure returns (int256) {
    if (_x >= 0)
    return _x;
    return -_x;
  }
}

