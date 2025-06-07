"""
Author:SuoLin Zhang
Created:2023
About: String functionality for maya object paths
"""


def generateReprString(cls, name):
    """Generate the string representation for the __repr__ dunder method.

    Args:
        cls(str): the cls.__name__ of the class
        name(str): The node used

    Returns:
        str: The string representation for the __repr__ special method.

    Example:
        __repr__ = generateReprString(
            self.__class__.__name__,
            self.fullpath
        )
        """
    return "{cls}('{node}')".format(cls=cls, node=rootName(name))


def rootName(name):
    """Stripes grouping information from a given full path.

    Args:
        name(str): The name containing group information.

    Returns:
        str: The name without grouping information.

    Example:
        name = "namespace:base_GRP|namespace:sub_GRP|namespace:sphere_GEO"
            rootName(name)
            Output:"namespace:sphere_GEO"
        """
    if not name:
        return name

    return name.split("|")[-1]


def baseName(name):
    """This function will stripe the namespaces and grouping information of a name.
    This is useful when working with full paths but needing the base for naming.

    Args:
        name(str): The name containing group information.

    Returns:
        str: The name without grouping or namespace information.

    Example:
        name = "namespace:base_GRP|namespace:sub_GRP|namespace:sphere_GEO"
            baseName(name)
            Output:"sphere_GEO"
        """
    if not name:
        return name

    return name.split("|")[-1].split(":")[-1]


def namespace(name):
    """This function will return the namespace if any exists.

    Args:
        name(str): The name containing group information.

    Returns:
        str: The namespace.

    Example:
        name = "namespace:base_GRP|namespace:sub_GRP|namespace:sphere_GEO"
            namespace(name)
            Output:namespace
        """
    if not name:
        return name

    if name.find(":") != -1:
        return rootName(name).rsplit(":", 1)[0]
