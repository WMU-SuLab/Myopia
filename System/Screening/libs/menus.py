# -*- encoding: utf-8 -*-
"""
@File Name      :   menus.py    
@Create Time    :   2022/4/27 11:23
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

screening_manage_url = '/screening/manage'

init_json = {
    "homeInfo": {
        "title": "首页",
        "href": screening_manage_url + "/home",
    },
    "logoInfo": {
        # "title": "眼健康管理系统",
        "title": "",
        "image": "/static/Screening/images/manage/logo.png",
        "href": "/screening/manage",
    },
    "menuInfo": [
        {
            "title": "常规管理",
            "icon": "fa fa-address-book",
            "href": "",
            "target": "_self",
            "child": [
                {
                    "title": "首页",
                    "href": screening_manage_url + "/home",
                    "icon": "fa fa-home",
                    "target": "_self",
                },
                {
                    "title": "用户管理",
                    "href": screening_manage_url + "/user",
                    "icon": "fas fa-user",
                    "target": "_self",
                },
                {
                        "title": "项目管理",
                        "href": screening_manage_url + "/project",
                        "icon": "fas fa-tasks",
                        "target": "_self",
                },
                # {
                #     "title": "项目管理",
                #     "href": "",
                #     "icon": "fas fa-tasks",
                #     "target": "_self",
                #     "child": [
                #         {
                #             "title": "温州医科大学近视防控项目",
                #             "href": screening_manage_url + "/project/wmu",
                #             "icon": "fa fa-school",
                #             "target": "_self",
                #         },
                #     ]
                # },
                {
                    "title": "生物仪器数据管理",
                    "href": "",
                    "icon": "fa fa-database",
                    "target": "_self",
                    "child": [
                        {
                            "title": "视力表",
                            "href": screening_manage_url + "/equipments/visual_chart",
                            "icon": "fa fa-eye",
                            "target": "_self",
                        }, {
                            "title": "生物测量仪",
                            "href": screening_manage_url + "/equipments/bio_meter",
                            "icon": "fa fa-ruler",
                            "target": "_self",
                        }, {
                            "title": "电脑验光仪",
                            "href": screening_manage_url + "/equipments/optometry",
                            "icon": "fa fa-laptop",
                            "target": "_self",
                        }, {
                            "title": "眼压计",
                            "href": screening_manage_url + "/equipments/tono_meter",
                            "icon": "fa fa-thermometer-full",
                            "target": "_self",
                        }, {
                            "title": "眼底照",
                            "href": screening_manage_url + "/equipments/eye_ground",
                            "icon": "fa fa-camera",
                            "target": "_self",
                        }, {
                            "title": "测序",
                            "href": screening_manage_url + "/equipments/sequence",
                            "icon": "fa fa-dna",
                            "target": "_self",
                        }, {
                            "title": "知情同意书",
                            "href": screening_manage_url + "/equipments/informed_consent",
                            "icon": "fa fa-file-alt",
                            "target": "_self",
                        }, {
                            "title": "问卷调查",
                            "href": screening_manage_url + "/equipments/questionnaire",
                            "icon": "fa fa-question-circle",
                            "target": "_self",
                        },
                    ]
                },
                {
                    "title": "数据统计分析",
                    "href": screening_manage_url + "/statistics",
                    "icon": "fas fa-chart-pie",
                    "target": "_self",
                },
                {
                    "title": "工具",
                    "href": "",
                    "icon": "fa fa-wrench",
                    "target": "_self",
                    "child": [
                        {
                            "title": "近视风险预测",
                            "href": screening_manage_url + "/tools/myopia_risk_prediction",
                            "icon": "fa fa-eye",
                            "target": "_self",
                        }
                    ]
                },
            ]
        },
    ]
}
