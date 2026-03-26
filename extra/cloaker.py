import base64
import random

def obfuscate_payload(payload, method='base64'):
    if method == 'base64':
        return base64.b64encode(payload.encode()).decode()
    elif method == 'hex':
        return payload.encode().hex()
    elif method == 'reverse':
        return payload[::-1]
    return payload