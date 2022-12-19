# EasyTl documentation

## source.filehash
`source/filehash.py` is a module, that helps with hashing plugins for auto-update checking

**File: [src/source/filehash.py](../../src/source/filehash.py)**

> #### Functions of the `filehash` module:
> 
>> ##### filehash.get_string_hash -> `str`
>> Calculates the hash of the string. Arguments:
>> - `string` (`str` | `bytes`) - string to be hashed
> 
>> ##### filehash.get_file_hash -> `str`
>> Calculates the file hash. Arguments:
>> - `path` (`str` | `bytes`) - path to the file to be hashed