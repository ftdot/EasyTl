import hashlib


def get_string_hash(string: str | bytes) -> str:
    """Calculates the hash of the string

    :param string: String that will be hashed
    :type string: str | bytes

    :returns: Hashed string
    :rtype: str
    """

    return hashlib.sha256(string.encode() if isinstance(string, str) else string).hexdigest()


def get_file_hash(path: str | bytes) -> str:
    """Calculates file hash

    :param path: Path to the file
    :type path: str | bytes

    :returns: String with hash of the file
    :rtype: str
    """

    sha256_hash = hashlib.sha256()  # create the sha256 hash object
    with open(path, "rb") as f:  # open file to be hashed
        for byte_block in iter(lambda: f.read(4096), b""):  # read the file by the byte blocks
            sha256_hash.update(byte_block)  # update the sha256 hash object by the byte block
    return sha256_hash.hexdigest()  # return hex digest of the hash
