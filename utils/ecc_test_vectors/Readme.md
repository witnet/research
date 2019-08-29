# Usage

The best way to use this code is to create a virtual environment and install the dependencies there.

- sudo apt install virtualenv
- virtualenv -p python3 .
- source bin/activate
- pip install -r requirements.txt
- python generate_test_vectors.py -curve secp256k1

 The output will be a json with the tests of the curve. Currently we support secp256k1, P256(secp256r1), secp224k1, P224(secp224r1), secp192k1, P192(secp192r1), P384 and P512
