#coding=utf-8
#获取当前路径：os.getcwd()与os.path.abspath('.'),都可以
import os
print(os.getcwd())
print(os.path.abspath('.'))

#获取路径的目录部分和文件部分
aa=os.path.split("C:/Python35/a.txt")
bb=os.path.split("c:/python27/")
print(aa[0],aa[1])
print(bb)

#判断路径类型
cc=os.path.isdir("c:/")
print(cc)
dd=os.path.isfile("c:/python27")
print(dd)


#目录操作
#列出某个目录所有文件名
allfile=os.listdir("c:/Python27")
for alldir in allfile:
    child=os.path.join('%s%s' % ("c:/Python27",alldir))
    print(child)
print(allfile)


def gci(filepath):
#遍历filepath下所有文件，包括子目录
  files = os.listdir(filepath)
  for fi in files:
    fi_d = os.path.join(filepath,fi)
    if os.path.isdir(fi_d):
      gci(fi_d)
    else:
      print(os.path.join(filepath,fi_d))

#递归遍历/root目录下所有文件
#gci('c:/python27')

for fpathe,dirs,fs in os.walk('c:/python27'):
  for f in fs:
    #print(os.path.join(fpathe,f))
    print(f)

for i in os.walk('c:/python27'):
    print(i[0])

#列出所有以exe为文件后缀的文件
fpath="C:\dev\Quant\stock\Data\SZ"
for i in os.listdir(fpath):
    fi=os.path.join(fpath,i)
    if os.path.isfile(fi) and os.path.splitext(i)[1]==".CSV":
        print(i,fi)
'''
#创建目录
import os
os.mkdir("c:/Python35/pydir")
#重命名目录
import os
os.rename("D:\\Python35\\pydir","D:\\Python35\\pydir2")
#删除目录
import os
os.rmdir("D:/Python35/pydir2")

#高级文件操作
#删除文件
import os
os.remove("D:/pydir1/木兰花.txt")
'''