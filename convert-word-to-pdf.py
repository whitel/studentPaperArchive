# -*- coding: utf8 -*-

import os, sys
from win32com.client import Dispatch, constants
import comtypes.client

"""
获取所有的docx文档
"""
def fetchAllFile(path):
    files = []
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            ext = os.path.splitext(file)[1].lower()
            if ext == '.docx' or ext == '.doc':
                fullpath = os.path.join(dirpath, file)
                files.append(fullpath)
    return files

"""
将WORD文档转换为PDF文件
"""
def convertWordToPdf(docxPath, pdfPath):
    flag = False
    try:
        wdFormatPDF = 17
        word = comtypes.client.CreateObject('Word.Application')
        doc = word.Documents.Open(docxPath)
        doc.SaveAs(pdfPath, FileFormat=wdFormatPDF)
        doc.Close()
        word.Quit()
    except Exception as e:
        flag = True
        print(e)
    if(flag == False):
        os.remove(doc)
        
def main(src, dest):
    docPath = src
    if not os.path.exists(docPath):
        print("path not exists")
        return
    pdfPath = dest
    if not os.path.exists(pdfPath):
        os.makedirs(pdfPath)
    files = fetchAllFile(docPath)
    for file in files:
        identifier = file.split('\\')[-2]
        fileName = os.path.splitext(os.path.basename(file))[0] + '.pdf'
        if not os.path.exists(os.path.join(pdfPath, identifier)):
            os.mkdir(os.path.join(pdfPath, identifier))
        savePath = os.path.join(pdfPath, identifier, fileName)
        if not os.path.exists(savePath):
            print("转换文件：", file, savePath)
            convertWordToPdf(file, savePath)
        else:
            print("文件已经存在，无需转换")
        
if __name__=='__main__':
    main('D:\\学生工作\\2015年之前数据\\3\\test', 'D:\\学生工作\\2015年之前数据\\3\\test')
