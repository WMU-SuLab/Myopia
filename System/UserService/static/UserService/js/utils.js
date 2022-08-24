/*
-*- encoding: utf-8 -*-
@File Name      :   utils.py    
@Create Time    :   2022/8/24 11:45
@Description    :   
@Version        :   
@License        :   MIT
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :   
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
*/

function downloadFromURL(url, fileName) {
    fetch(url).then(res => res.blob()).then(blob => { // 将链接地址字符内容转变成blob地址
        const a = document.createElement('a')
        a.href = URL.createObjectURL(blob)
        //测试链接console.log(a.href)
        a.download = fileName  // 下载文件的名字
        document.body.appendChild(a)
        a.click()
    })
}