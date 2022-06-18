# -*- encoding: utf-8 -*-
"""
@File Name      :   boolen.py    
@Create Time    :   2022/6/18 16:16
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


def strtobool(val):
    """Convert a string representation of truth to true (1) or false (0).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ('y', 'yes', 'Yes', 'YES', 't', 'true', 'True', 'TRUE', 'on', '1'):
        return 1
    elif val in ('n', 'no', 'No', 'NO', 'f', 'false', 'False', 'FALSE', 'off', '0'):
        return 0
    else:
        raise ValueError("invalid truth value %r" % (val,))
