# -*- encoding: utf-8 -*-
"""
@File Name      :   test.py    
@Create Time    :   2022/4/4 16:28
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
from weasyprint import HTML
HTML(string="""
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>报告</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #FAFAFA;
            font: 12pt "Tahoma";
        }

        * {
            box-sizing: border-box;
            -moz-box-sizing: border-box;
        }

        .page {
            width: 21cm;
            min-height: 29.7cm;
            padding: 2cm;
            margin: 1cm auto;
            border: 1px #D3D3D3 solid;
            border-radius: 5px;
            background: white;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
        }

        .subpage {
            padding: 1cm;
            border: 2px grey solid;
            height: 256mm;
            outline: 2cm white solid;
        }

        @page {
            size: A4;
            margin: 0;
        }

        @media print {
            .page {
                margin: 0;
                border: initial;
                border-radius: initial;
                width: initial;
                min-height: initial;
                box-shadow: initial;
                background: initial;
                page-break-after: always;
            }
        }

        h1 {
            text-align: center;
            /* font-size: 20px; */
            font-weight: bold;
        }

        b {
            display: block;
        }

        table {
            min-height: 25px;
            line-height: 25px;
            text-align: center;
            border-collapse: collapse;
            padding: 2px;
            align-content: center;
        }

        table, table tr th, table tr td {
            border: 1px solid black;
        }

        p {
            margin: 0;
        {#text-indent: 2em;#} word-break: break-all;
            word-wrap: break-word;
            /*多行对齐*/
            text-align: justify;
        }
    </style>
</head>

<body>
test
</body>
</html>
""").write_pdf('test.pdf')