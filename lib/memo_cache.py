from copy import deepcopy
import pandas as pd
import pickle

def memo(f):
    f.cache = {}
    def _f(*args, **kwargs):
        key = __get_cache_key__(args, f)
        if key not in f.cache:
             response = f(*args, **kwargs)
             if(response is not None):
                if(isinstance(response, pd.DataFrame)):
                    f.cache[key] = pickle.loads(pickle.dumps(response))
                else:
                    f.cache[key] = deepcopy(response)
             else: 
                return None   
        cache_ret = f.cache[key]
        if(isinstance(cache_ret, pd.DataFrame)):
            pickle.loads(pickle.dumps(cache_ret))
        return deepcopy(cache_ret)
    return _f

def __get_cache_key__(args, f):
    if(len(args) > 0 and hasattr(args[0], f.__name__)):
        return args[1:]
    return args