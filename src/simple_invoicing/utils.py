import hashlib

# https://kevingal.com/blog/collisions.html#fnref:unique    Interesting explaination about hash collisions
# https://kevingal.com/apps/collision.html                Collision calculator
# https://docs.python.org/3/reference/datamodel.html#object.__hash__    Python hash function particularities

def custom_hash(string: bytes|str) -> int:
    if isinstance(string, str):
        string = string.encode('utf-8')
    return int.from_bytes(hashlib.md5(string).digest()[:8], byteorder='big', signed=True)