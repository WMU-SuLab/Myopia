# -*- encoding: utf-8 -*-
"""
@File Name      :   decorator.py    
@Create Time    :   2022/4/19 15:24
@Description    :   
@Version        :   
@License        :   MIT
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :   
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
"""
__auth__ = 'diklios'


def for_all_methods(decorator):
    """
    Use like this:
    @for_all_methods(mydecorator)
    class C(object):
        def m1(self): pass
        def m2(self, x): pass
    ...
    """
    def decorate(cls):
        for attr in cls.__dict__:  # there's propably a better way to do this
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return decorate
