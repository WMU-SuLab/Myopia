# -*- encoding: utf-8 -*-
"""
@File Name      :   tgfbi.py
@Create Time    :   2022/11/28 16:06
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

# 如果后续规则较为复杂，数据量较大，可以考虑使用小型SQL数据库或者键值对数据库（如Redis）来存储规则
tgfbi_contract_settings = {
    'JMP': {
        'project_id': 'PSI20220003JMF',
        'product_name': '角膜营养不良检测-基础版',
    },
    # JMF是老的，应该被移除，但是为了兼容旧的数据，暂时保留
    'JMF': {
        'project_id': 'PSI20220003JMF',
        'product_name': '角膜营养不良检测-基础版',
    },
    'JMA': {
        'project_id': 'PSI20220004JMA',
        'product_name': '角膜营养不良检测-基础版',
    }
}
