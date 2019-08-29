import importlib
import sys
import argparse
import json
from fastecdsa.point import Point

# Known endomorphisms of the curves
endomorphism = {
  "P256" : {
    "lambda" : "",
    "beta" : ""
  },
  "secp256k1" : {
    "lambda" : '0x5363ad4cc05c30e0a5261c028812645a122e22ea20816678df02967c1b23bd72',
    "beta" : '0x7ae96a2b657c07106e64479eac3434e99cf0497512f58995c1396c28719501ee'
  },
  "P192" : {
    "lambda" : "",
    "beta" : ""
  },
  "secp192k1" : {
    "lambda" : '0x3d84f26c12238d7b4f3d516613c1759033b1a5800175d0b1',
    "beta" : '0xbb85691939b869c1d087f601554b96b80cb4f55b35f433c2'
  },
  "P224" : {
    "lambda" : "",
    "beta" : ""
  },
  "secp224k1" : {
    "lambda" : '0x60dcd2104c4cbc0be6eeefc2bdd610739ec34e317f9b33046c9e4788',
    "beta" : '0xfe0e87005b4e83761908c5131d552a850b3f58b749c37cf5b84d6768'
  },
  "P384" : {
    "lambda" : "",
    "beta" : ""
  },
  "P521" : {
    "lambda" : "",
    "beta" : ""
  }
}

# Data structure
data = {}
data['params'] = {}
data['multiplication'] = {'valid' : [], 'invalid' : [] }
data['addition'] = {'valid' : [], 'invalid' : [] }
data['subtraction'] = {'valid' : [], 'invalid' : [] }
data['mulAddMul'] = {'valid' : [], 'invalid' : [] }
data['decomposeScalar'] = {'valid' : [], 'invalid' : [] }
data['simMul'] = {'valid' : [], 'invalid' : [] }

# Parse input arguments
# Commands:
  # -curve :  choose the curve you want to generate the test for
parser = argparse.ArgumentParser(description='Curve for which you want to generate your test vectors')
parser.add_argument('-curve', action="store", choices = ["P256", "secp256k1", "P192", "secp192k1", "P224", "secp224k1"], required=True, type=str,
                    dest = "curve",
                    help='Specify the curve to generate the test vectors, e.g., secp256k1 or P256')

args = parser.parse_args()

# Load curve module dependent on the given argument
curve_module = importlib.import_module("fastecdsa.curve")
target_curve = getattr(curve_module, args.curve)

# Test vectors taken from https://chuckbatson.wordpress.com/2014/11/26/secp256k1-test-vectors/
test_vec = [
      1,
      2,
      3,
      4,
      5,
      6,
      7,
      8,
      9,
      10,
      11, 
      12,
      13,
      14,
      15,
      16,
      17,
      18,
      19,
      20,
      112233445566778899,
      112233445566778899112233445566778899,
      28948022309329048855892746252171976963209391069768726095651290785379540373584,
      57896044618658097711785492504343953926418782139537452191302581570759080747168,
      86844066927987146567678238756515930889628173209306178286953872356138621120752,
      115792089237316195423570985008687907852837564279074904382605163141518161494317,
      115792089237316195423570985008687907852837564279074904382605163141518161494318,
      115792089237316195423570985008687907852837564279074904382605163141518161494319,
      115792089237316195423570985008687907852837564279074904382605163141518161494320,
      115792089237316195423570985008687907852837564279074904382605163141518161494321,
      115792089237316195423570985008687907852837564279074904382605163141518161494322,
      115792089237316195423570985008687907852837564279074904382605163141518161494323,
      115792089237316195423570985008687907852837564279074904382605163141518161494324,
      115792089237316195423570985008687907852837564279074904382605163141518161494325,
      115792089237316195423570985008687907852837564279074904382605163141518161494326,
      115792089237316195423570985008687907852837564279074904382605163141518161494327,
      115792089237316195423570985008687907852837564279074904382605163141518161494328,
      115792089237316195423570985008687907852837564279074904382605163141518161494329,
      115792089237316195423570985008687907852837564279074904382605163141518161494330,
      115792089237316195423570985008687907852837564279074904382605163141518161494331,
      115792089237316195423570985008687907852837564279074904382605163141518161494332,
      115792089237316195423570985008687907852837564279074904382605163141518161494333,
      115792089237316195423570985008687907852837564279074904382605163141518161494334,
      115792089237316195423570985008687907852837564279074904382605163141518161494335,
      115792089237316195423570985008687907852837564279074904382605163141518161494336,
      77059549740374936337596179780007572461065571555507600191520924336939429631266,
      32670510020758816978083085130507043184471273380659243275938904335757337482424    
      ]

# Fix if a is represented as a negative number (some curves do)
if target_curve.a < 0:
  target_curve.a = target_curve.p + target_curve.a

# Write down parameters of the curve
data['params']={
  'gx' : str(hex(target_curve.gx)),
  'gy' : str(hex(target_curve.gy)),
  'pp' : str(hex(target_curve.p)),
  'nn' : str(hex(target_curve.q)),
  'aa' : str(hex(target_curve.a)),
  'bb' : str(hex(target_curve.b)),
  'lambda' : endomorphism[args.curve]['lambda'],
  'beta' : endomorphism[args.curve]['beta']
}

# Generator point
G = Point(target_curve.gx, target_curve.gy, curve=target_curve)

# Generate multiplication test vectors
for item in test_vec:
  R = item * G
  data['multiplication']['valid'].append({
    'description' : "G x" + str(item),
    'input' : {
      'k' : str(item),
      'x' : str(hex(target_curve.gx)),
      'y' : str(hex(target_curve.gy))
    },
    'output' : {
      'x' : str(hex(R.x)),
      'y' : str(hex(R.y))
    }
  })

# Generate small scalar addition vectors
for i in range(0, 19):
  P = test_vec[i] * G
  Q = test_vec[0] * G
  Z = test_vec[i+1] * G
  data['addition']['valid'].append({
    'description' : 'small scalar %s xG plus G' % str(i+1),
    'input' : {
      'x1' : str(hex(P.x)),
      'y1' : str(hex(P.y)),
      'x2' : str(hex(Q.x)),
      'y2' : str(hex(Q.y))
    },
    'output': {
      'x' : str(hex(Z.x)),
      'y' : str(hex(Z.y))
    }
  })

# Generate big scalar addition vectors
P = test_vec[22] * G
Q = test_vec[23] * G
Z = test_vec[24] * G
data['addition']['valid'].append({
  'description' : 'big scalar 1 xG plus big scalar 2 xG',
  'input' : {
    'x1' : str(hex(P.x)),
    'y1' : str(hex(P.y)),
    'x2' : str(hex(Q.x)),
    'y2' : str(hex(Q.y))
  },
  'output': {
    'x' : str(hex(Z.x)),
    'y' : str(hex(Z.y))
  }
})

# Generate big scalar plus small scalar addition vectors
for i in range(0, 19):
  P = test_vec[25] * G
  Q = test_vec[i] * G
  Z = test_vec[25+i+1] * G
  data['addition']['valid'].append({
    'description' : 'small scalar %s xG plus big scalar 4 xG' % str(i+1),
    'input' : {
      'x1' : str(hex(P.x)),
      'y1' : str(hex(P.y)),
      'x2' : str(hex(Q.x)),
      'y2' : str(hex(Q.y))
    },
    'output': {
      'x' : str(hex(Z.x)),
      'y' : str(hex(Z.y))
    }
  })

# Generate subtraction vectors
for i in range(0, 19):
  P = test_vec[i] * G
  Q = test_vec[0] * G
  Z = test_vec[i+1] * G
  data['subtraction']['valid'].append({
    'description' : 'small scalar %s xG minus G' % str(4+i+1),
    'input' : {
      'x1' : str(hex(Z.x)),
      'y1' : str(hex(Z.y)),
      'x2' : str(hex(Q.x)),
      'y2' : str(hex(Q.y))
    },
    'output': {
      'x' : str(hex(P.x)),
      'y' : str(hex(P.y))
    }
  })

if endomorphism[args.curve]['lambda']:
  # Generate kP+ lQ vectors
  Z = test_vec[24] * G
  data['mulAddMul']['valid'].append({
    'description' : 'big scalar 1 xG plus big scalar 2 xG',
    'input' : {
      'k' : str(test_vec[22]),
      'l' : str(test_vec[23]),
      'px' : str(hex(target_curve.gx)),
      'py' : str(hex(target_curve.gy)),
      'qx' : str(hex(target_curve.gx)),
      'qy' : str(hex(target_curve.gy))
    },
    'output': {
      'x' : str(hex(Z.x)),
      'y' : str(hex(Z.y))
    }
  })

  for i in range(0, 19):
    P = test_vec[25+i] * G
    Z = test_vec[25+i+1] * G
    data['mulAddMul']['valid'].append({
      'description' : 'small scalar %s xG plus big scalar 4 xG' % str(i+1),
      'input' : {
        'k' : str(test_vec[25+i]),
        'l' : str(test_vec[0]),
        'px' : str(hex(target_curve.gx)),
        'py' : str(hex(target_curve.gy)),
        'qx' : str(hex(target_curve.gx)),
        'qy' : str(hex(target_curve.gy))
      },
      'output': {
        'x' : str(hex(Z.x)),
        'y' : str(hex(Z.y))
      }
    })

# Additional test vectors in case of secp256k1
if args.curve == 'secp256k1':

  data['decomposeScalar']['valid'].append({
    'description' : 'scalar decomposition of Big Scalar 16',
    'input' : {
      'k' : '115792089237316195423570985008687907852837564279074904382605163141518161494329'
    },
    'output': {
      'k1' : '-8',
      'k2' : '0'
    }
  })

  data['decomposeScalar']['valid'].append({
    'description' : 'scalar decomposition of Big Scalar 1',
    'input' : {
      'k' : '28948022309329048855892746252171976963209391069768726095651290785379540373584'
    },
    'output': {
      'k1' : '-75853609866811635898812693916901439793',
      'k2' : '-91979353254113275055958955257284867062'
    }
  })

  data['decomposeScalar']['valid'].append({
    'description' : 'scalar decomposition of Big Scalar 2',
    'input' : {
      'k' : '57896044618658097711785492504343953926418782139537452191302581570759080747168'
    },
    'output': {
      'k1' : '216210193282829828426210433195336588662',
      'k2' : '-119455732959019993483332865153036025047'
    }
  })

  data['decomposeScalar']['valid'].append({
    'description' : 'scalar decomposition of Big Scalar 21',
    'input' : {
      'k' : '77059549740374936337596179780007572461065571555507600191520924336939429631266'
    },
    'output': {
      'k1' : '-89243190524605339210527649141408088119',
      'k2' : '-53877858828609620138203152946894934485'
    }
  })

  data['decomposeScalar']['valid'].append({
    'description' : 'scalar decomposition of Big Scalar 22',
    'input' : {
      'k' : '32670510020758816978083085130507043184471273380659243275938904335757337482424'
    },
    'output': {
      'k1' : '-185204247857117235934281322466442848518',
      'k2' : '-7585701889390054782280085152653861472'
    }
  })

  data['decomposeScalar']['valid'].append({
    'description' : 'scalar decomposition of small scalar 1',
    'input' : {
      'k' : '1'
    },
    'output': {
      'k1' : '1',
      'k2' : '0'
    }
  })

  data['decomposeScalar']['valid'].append({
    'description' : 'scalar decomposition of small scalar 5',
    'input' : {
      'k' : '5'
    },
    'output': {
      'k1' : '5 ',
      'k2' : '0'
    }
  })

  data['simMul']['valid'].append({
    'description' : 'simultaneous multiplication of big scalar 21 and small scalar 22 times G',
    'input' : {
      'k1' : '-89243190524605339210527649141408088119',
      'k2' : '-53877858828609620138203152946894934485',
      'l1' : '-185204247857117235934281322466442848518',
      'l2' : '-7585701889390054782280085152653861472',
      'px' : str(hex(target_curve.gx)),
      'py' : str(hex(target_curve.gy)),
      'qx' : '0xc6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5',
      'qy' : '0x1ae168fea63dc339a3c58419466ceaeef7f632653266d0e1236431a950cfe52a'
    },
    'output': {
      'x' : '0x7635e27fba8e1f779dcfdde1b1eacbe0571fbe39ecf6056d29ba4bd3ef5e22f2',
      'y' : '0x197888e5cec769ac2f1eb65dbcbc0e49c00a8cdf01f8030d8286b68c1933fb18'
    }
  })

  data['simMul']['valid'].append({
    'description' : 'simultaneous multiplication of big scalar 16 and big scalar 1 times G',
    'input' : {
      'k1' : '-8',
      'k2' : '0',
      'l1' : '1',
      'l2' : '0',
      'px' : str(hex(target_curve.gx)),
      'py' : str(hex(target_curve.gy)),
      'qx' : str(hex(target_curve.gx)),
      'qy' : str(hex(target_curve.gy))
    },
    'output': {
      'x' : '0x5CBDF0646E5DB4EAA398F365F2EA7A0E3D419B7E0330E39CE92BDDEDCAC4F9BC',
      'y' : '0x951435BF45DAA69F5CE8729279E5AB2457EC2F47EC02184A5AF7D9D6F78D9755'
    }
  })

  data['simMul']['valid'].append({
    'description' : 'simultaneous multiplication of big scalar 16 and small scalar 5 times G',
    'input' : {
      'k1' : '-8',
      'k2' : '0',
      'l1' : '5',
      'l2' : '0',
      'px' : str(hex(target_curve.gx)),
      'py' : str(hex(target_curve.gy)),
      'qx' : str(hex(target_curve.gx)),
      'qy' : str(hex(target_curve.gy))
    },
    'output': {
      'x' : '0xF9308A019258C31049344F85F89D5229B531C845836F99B08601F113BCE036F9',
      'y' : '0xC77084F09CD217EBF01CC819D5C80CA99AFF5666CB3DDCE4934602897B4715BD'
    }
  })

  data['simMul']['valid'].append({
    'description' : 'simultaneous multiplication of big scalar 1 and big scalar 2 times G',
    'input' : {
      'k1' : '-75853609866811635898812693916901439793',
      'k2' : '-91979353254113275055958955257284867062',
      'l1' : '216210193282829828426210433195336588662',
      'l2' : '-119455732959019993483332865153036025047',
      'px' : str(hex(target_curve.gx)),
      'py' : str(hex(target_curve.gy)),
      'qx' : str(hex(target_curve.gx)),
      'qy' : str(hex(target_curve.gy))
    },
    'output': {
      'x' : '0xE24CE4BEEE294AA6350FAA67512B99D388693AE4E7F53D19882A6EA169FC1CE1',
      'y' : '0x8B71E83545FC2B5872589F99D948C03108D36797C4DE363EBD3FF6A9E1A95B10'
    }
  })

# Dump to json
with open(args.curve +'.json', 'w') as outfile:
  json.dump(data, outfile, indent=2)
