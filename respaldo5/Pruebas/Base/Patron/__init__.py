class FlyWeight(type):
    def __init__(cls, name, bases, dct):
        cls.__instances = {}
        type.__init__(cls, name, bases, dct)
 
    def __call__(cls, key, *args, **kw):
        instance = cls.__instances.get(key)
        if instance is None:
            instance = type.__call__(cls, key, *args, **kw)
            cls.__instances[key] = instance
        return instance
        
class Singleton(type):
    def __init__(cls, name, bases, dct):
        cls.__instance = None
        type.__init__(cls, name, bases, dct)
 
    def __call__(cls, *args, **kw):
        if cls.__instance is None:
            cls.__instance = type.__call__(cls, *args,**kw)
        return cls.__instance