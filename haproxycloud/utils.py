import copy

def merge_array_recursive(a, b):
    '''
    Merges the elements of one or more arrays together so that the values of one are appended to 
    the end of the previous one. It returns the resulting array.

    If the input arrays have the same string keys, then the values for these keys are merged together 
    into an array, and this is done recursively, so that if one of the values is an array itself, 
    the function will merge it with a corresponding entry in another array too. If, however, the arrays 
    have the same numeric key, the later value will not overwrite the original value, but will be appended. 
    '''
    if not isinstance(b, dict):
        return b
    result = copy.deepcopy(a)
    for k, v in b.iteritems():
        if k in result and isinstance(result[k], dict):
            result[k] = merge_array_recursive(result[k], v)
        elif k in result and isinstance(result[k], list):
            if len(v) > 0 and len(result[k]) > 0:
                result[k].extend(copy.deepcopy(v))
            if len(v) > 0 and len(result[k]) == 0:
                result[k] = copy.deepcopy(v)
        #elif k in result and k is not None and k is not '':
        #    result[k] = result[k] + copy.deepcopy(v)
        else:
            result[k] = copy.deepcopy(v)
    return result