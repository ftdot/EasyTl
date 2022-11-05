
class Namespace:
    """Object, that replaces dict with the sample namespace

    :param init_dict: (Optional) The init dictionary
    :type init_dict: dict | None

    :ivar values: The dict with the values
    :type values: dict
    """

    def __init__(self, init_dict: dict | None = None):
        self.values = init_dict if init_dict is not None else {}  # The dictionary with values

        self.org_setattr = self.__setattr__  # save original __setattr__ method
        self.__setattr__ = self._setattr  # replace original __setattr__ method with our method

    def _setattr(self, key, value):
        if key in dir(self):  # check if the key is a variable in the Namespace object
            self.org_setattr(key, value)  # call original __setattr__ method

        self.values[key] = value

    def __getattr__(self, item):
        if item in self.values:
            return self.values[item]
        else:
            return super().__getattribute__(item)  # call original __getattribute__

    def __dict__(self) -> dict:
        return self.values
