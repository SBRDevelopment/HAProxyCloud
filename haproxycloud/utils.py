import copy
import yaml
import yaml.constructor
 
try:
    # included in standard lib from Python 2.7
    from collections import OrderedDict
except ImportError:
    # try importing the backported drop-in replacement
    # it's available on PyPI
    from ordereddict import OrderedDict
 
class OrderedDictYAMLLoader(yaml.Loader):
    """
    A YAML loader that loads mappings into ordered dictionaries.
    """
 
    def __init__(self, *args, **kwargs):
        yaml.Loader.__init__(self, *args, **kwargs)
 
        self.add_constructor(u'tag:yaml.org,2002:map', type(self).construct_yaml_map)
        self.add_constructor(u'tag:yaml.org,2002:omap', type(self).construct_yaml_map)
 
    def construct_yaml_map(self, node):
        data = OrderedDict()
        yield data
        value = self.construct_mapping(node)
        data.update(value)
 
    def construct_mapping(self, node, deep=False):
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)
        else:
            raise yaml.constructor.ConstructorError(None, None,
                'expected a mapping node, but found %s' % node.id, node.start_mark)
 
        mapping = OrderedDict()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError, exc:
                raise yaml.constructor.ConstructorError('while constructing a mapping',
                    node.start_mark, 'found unacceptable key (%s)' % exc, key_node.start_mark)
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping

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