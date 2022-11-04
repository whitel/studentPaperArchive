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
清理数据，组装成一个dict
"""
def cleanData(text):
    text = text.replace(' ', '')
    text = text.replace('\n\n\n\n\n', '\n')
    text = text.replace('\n\n\n\n', '\n')
    text = text.replace('\n\n\n', '\n')
    text = text.replace('\n\n', '\n')
    text = text.replace('姓\n名：\n', '姓名：')
    text = text.replace('学\n号：\n', '学号：')
    text = text.replace('导\n师：\n', '导师：')
    text = text.replace('学\n院：\n', '学院：')
    text = text.replace('题\n目：\n', '题目：')
    text = text.replace('\n年', '年')
    text = text.replace('\n月', '月')
    text = text.replace('\n日', '日')

    lines = []
    for line in text.splitlines():
        if(line == '' or line.find('保密期限') != -1):
            continue
        lines.append(line)

    result = {}
    for line in lines:
        if(line.find('：') != -1):
            temp = line.split('：')
            result[temp[0]] = temp[1]
        elif(line.find('年') != -1 and line.find('月') != -1 and line.find('日') != -1):
            result["日期"] = line

    return result

def getNumber(filePath):
    file = open(filePath, 'rb')
    fileReader = PyPDF2.PdfFileReader(file)
    page = fileReader.pages[0]
    text = page.extract_text(0)
    d = cleanData(text)
    return d['学号']

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
        identifier = file.split('/')[-2]
        fileName = os.path.splitext(os.path.basename(file))[0] + '.pdf'
        if not os.path.exists(os.path.join(pdfPath, identifier)):
            os.mkdir(os.path.join(pdfPath, identifier))
        savePath = os.path.join(pdfPath, identifier, fileName)
        if not os.path.exists(savePath):
            print("文件：", file)
            number = getNumber(file)
            os.rename(file, src + '/' + str(number) + '.pdf')
        else:
            print("文件已经存在，无需转换")
        
if __name__=='__main__':
    main('./test', './test/result/')
