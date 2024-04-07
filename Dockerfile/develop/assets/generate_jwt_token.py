#!/usr/bin/env python3
from jwt import JWT, jwk_from_pem
import time
import sys

# Get PEM file path
if len(sys.argv***REMOVED*** > 1:
    pem = sys.argv[1***REMOVED***
else:
    pem = input("Enter path of private PEM file: "***REMOVED***

# Get the App ID
if len(sys.argv***REMOVED*** > 2:
    app_id = sys.argv[2***REMOVED***
else:
    app_id = input("Enter your APP ID: "***REMOVED***

# Open PEM
with open(pem, 'rb'***REMOVED*** as pem_file:
    signing_key = jwk_from_pem(pem_file.read(***REMOVED******REMOVED***

payload = {
    # Issued at time
    'iat': int(time.time(***REMOVED******REMOVED***,
    # JWT expiration time (10 minutes maximum***REMOVED***
    'exp': int(time.time(***REMOVED******REMOVED*** + 600,
    # GitHub App's identifier
    'iss': app_id
***REMOVED***

# Create JWT
jwt_instance = JWT(***REMOVED***
encoded_jwt = jwt_instance.encode(payload, signing_key, alg='RS256'***REMOVED***

print(encoded_jwt***REMOVED***
