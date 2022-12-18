
class Namespace:
    """Object, that replaces dict with the sample namespace

    :param init_dict: (Optional) The init dictionary
    :type init_dict: dict | None
    """

    def __init__(self, init_dict: dict | None = None):
        if init_dict is not None:
            for k, v in init_dict.items():
                setattr(self, k, v)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'Namespace({" ".join([f"{attr}={getattr(self, attr)}" for attr in dir(self) if not attr.startswith("__")])})'
