from collections import namedtuple

Vulnerability = namedtuple('Vulnerability', ['param', 'location', 'technique', 'original_value', 'payloads'])