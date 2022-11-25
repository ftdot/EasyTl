
class Namespace:
    """Object, that replaces dict with the sample namespace

    :param init_dict: (Optional) The init dictionary
    :type init_dict: dict | None
    """

    def __init__(self, init_dict: dict | None = None):
        if init_dict is not None:
            for k, v in init_dict.items():
                setattr(self, k, v)
