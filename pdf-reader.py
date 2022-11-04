import PyPDF2
import os

"""
获取所有的pdf文档
"""
def fetchAllFile(path):
    files = []
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            ext = os.path.splitext(file)[1].lower()
            if ext == '.pdf':
                fullpath = os.path.join(dirpath, file)
                files.append(fullpath)
    return files

"""
提取学号并重命名文件
"""
def extractNumber(filePath):
    file = open(filePath, 'rb')
    fileReader = PyPDF2.PdfFileReader(file)
    page = fileReader.pages[0]
    text = page.extract_text(0)
    numberIndex = text.find("号：\n") + 3
    
    if(numberIndex == 2):
        print("error finding number")
        return -1
    else:
        print(text[numberIndex : numberIndex + 10])
        return text[numberIndex : numberIndex + 10]

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
            print("文件：", file)
            number = extractNumber(file)
            os.rename(file, number + '.pdf')
        else:
            print("文件已经存在，无需转换")
        
if __name__=='__main__':
    main('./data', './data/result')
