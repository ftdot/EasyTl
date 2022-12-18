# EasyTl documentation

## source.namespace
`source/namespace.py` is a module with `Namespace` object, that allows to create 

#### Namespace `namespace.Namespace`
Class that helps replace dict with the sample namespace

#### Parameters:

##### Namespace.init\_dict `dict`
Initialize dict with already set values.
It sets to the `Namespace.values`

#### Variables of the `Namespace`:
From **1.4.0** version of EasyTl all variables sets to the object directly.

Example:
```python
from source.namespace import Namespace

n = Namespace()  # creating instance of the Namespace
n.some_value = 'Hello!'  # write some value to the namespace
```

Default variables in instance see here: [Documentation of source/core.py](../core.md#instancenamespace-sourcenamespacenamespace)
