import os
import re
import socket
import time
from urllib.request import urlretrieve

socket.setdefaulttimeout(30)  # 设置默认超时时间是 30s

exp = r'(?:!\[(.*?)\]\((.*?)\))'

"""
经过分析，博客 MD 文件的图片主要有以下几个类别：

1. 以 https://cdn.jsdelivr.net/gh/wmyskxz 开头，上传到 Github 上的图
  
  这一类直接用开头分开，后边就是路径和图片名字，很好处理
  
2. 以 https://gitee.com/wmyskxz/pic/raw/master 开头，上传到 Gitee 上的图

  这一类跟上面的同样的方法，直接下载到指定文件夹就可以
  
3. 以 https://files.mdnice.com/user/4774 开头的，上传到 Mdnice 自带图床的图

  一样的逻辑，直接创建 user/4774 的文件夹放进去就 OK


转换之后的格式：
![](https://wmyskxz-blog.oss-cn-chengdu.aliyuncs.com/img202210052341810.png)

"""


def CreatePicDirAndRetFinalPath(path):
    path = str(path)
    if path.startswith('https://cdn.jsdelivr.net/gh/wmyskxz'):
        # eg: https://cdn.jsdelivr.net/gh/wmyskxz/BlogImage02/2021-2-21/1613872075026-image.png
        return ''
        # dirAndName = path.split("https://cdn.jsdelivr.net/gh/wmyskxz/")[-1].split("/")
        # dirAndName 这里出来是一个列表：['BlogImage02', '2021-2-21', '1613872075026-image.png']

    if path.startswith("https://gitee.com/wmyskxz/pic/raw/master"):
        # eg: https://gitee.com/wmyskxz/pic/raw/master/20220306210249.png

        name = path.split("/")[-1]
        dirAndName = ['pic', 'raw', 'master', name]

    elif path.startswith('https://files.mdnice.com/user/4774'):
        # eg: https://files.mdnice.com/user/4774/be44f336-e8cd-4c26-9a0a-c5047979e340.png

        name = path.split("/")[-1]
        dirAndName = ['gitee', name]
    else:
        print('!---------失败 path:', path)
        return ''

    tempPath = ''
    try:
        for dirOrName in dirAndName:
            tempPath += dirOrName
            if dirOrName != dirAndName[-1]:
                # 但凡不是最后一个文件名，那么都是文件夹，没有的话需要提前创建一个
                if not os.path.exists(tempPath):
                    os.mkdir(tempPath)
            else:
                # 如果是文件名了，则直接退出
                break
            tempPath += '/'
    except:
        print('!---------失败dirAndName:', dirAndName)

    return tempPath


if __name__ == '__main__':

    fileList = filter(lambda temp: str(temp).endswith(".md"), os.listdir("."))
    fileList = sorted(fileList)  # 排序

    for fileName in fileList:
        start = time.time()
        with open(fileName, "r", encoding='utf-8') as read_f:
            fileLines = read_f.read()

            imageArr = re.findall(exp, fileLines)

            count = 0
            for desc, path in imageArr:
                count += 1
                finalPath = CreatePicDirAndRetFinalPath(path)
                if not finalPath:
                    if not path.startswith("https://cdn.jsdelivr.net/gh/wmyskxz"):
                        print('!!!! 失败：', path)
                    continue
                try:
                    urlretrieve(path, finalPath)
                except TimeoutError:
                    try:
                        # 重试一次
                        urlretrieve(path, finalPath)
                    except:
                        print('----错误：', path)
                percent = round(float(count) / len(imageArr), 2) * 100
                print('\r', '---------正在处理： %s [%d/%d]' % (fileName, count, len(imageArr)), end='')

        fileLines = fileLines.replace("https://cdn.jsdelivr.net/gh/wmyskxz", 'https://wmyskxz-blog.oss-cn-chengdu.aliyuncs.com') \
            .replace("https://gitee.com/wmyskxz/pic/raw/master", 'https://wmyskxz-blog.oss-cn-chengdu.aliyuncs.com/pic/raw/master') \
            .replace("https://files.mdnice.com/user/4774", 'https://wmyskxz-blog.oss-cn-chengdu.aliyuncs.com/gitee')

        with open(fileName, 'w', encoding='utf-8') as dump_f:
            dump_f.write(fileLines)
        end = time.time()
        print('\n========处理完成：', fileName, '， 耗时：', (end - start), 's')
