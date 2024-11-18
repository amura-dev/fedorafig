class PathError(Exception):
    """Exception for when a required file or directory is missing"""
    pass


class SyntaxError(Exception):
    """Exception for when the syntax of a configuration file is incorrect"""
    pass
