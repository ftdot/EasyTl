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

##### Namespace.values `dict[str, Any]`
Dict with the values.
By default: `{}` (empty) or set from `init\_dict` parameter

#### Methods of the `Namespace`:

##### Namespace.\_setattr()
(System method) Sets the value by key in the `Namespace.values` or if key is already exist in `Namespace` object, it sets it. 
Arguments:
- `self`
- `key` (`str`) - Key to set the value
- `value` (`Any`) - Value to set it
When object is initialized, `Namespace.\_\_setattr\_\_` method is sets to it

##### Namespace.\_\_getattr\_\_()
(System method) Gets the value by key in the `Namespace.values` or if key is already exist in `Namespace` object, it returns it.
Arguments:
- `self`
- `item` (`str`) - Item to get (key)