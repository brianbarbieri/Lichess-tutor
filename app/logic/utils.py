from functools import reduce  
import operator

def get_by_path(root, items):
    """Access a nested object in root by item sequence."""
    return reduce(operator.getitem, items, root)

def set_by_path(root, items, value):
    """Set a value in a nested object in root by item sequence."""
    get_by_path(root, items[:-1])[items[-1]] = value

def to_keep_one(dictionary, item):
    """Keeps one key in the dict"""
    keep = dictionary[item]
    dictionary.clear() 
    dictionary[item] = keep
    return dictionary