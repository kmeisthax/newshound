class classproperty(object):
    def __init__(self, f):
        self.f = f
    
    def __get__(self, instance, owner):
        if owner is None:
            owner = type(instance)

        return self.f(owner)
