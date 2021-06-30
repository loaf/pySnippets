# coding: utf-8
# 查询目录下所有的Word文档，如果是陈莉英创建的，保留，否则就删除
# 如果文档是docx,直接可用python-docx库查询属性，如果是doc,只能通过pywin32com库，先将其转成docx
from docx import Document
import os
import sys
import pickle
import re
import codecs
import string
import shutil
from win32com import client as wc

maindir=u'D:\\公司文档库\\filesys1'
todir=u'D:\\tmp'


def FindFileByAuthor(filename):
    f=open(filename,'rb')
    document = Document(f)

    core_properties = document.core_properties

    if (core_properties.author=='陈莉英' or core_properties.last_modified_by=='陈莉英'):
        shutil.copy(filename,todir)
        print(filename)

    f.close()


def transToDocx(filename):
    word = wc.Dispatch('Word.Application')
    doc = word.Documents.Open(filename)
    docxfilename=filename.replace('.doc','.docx',2)
    doc.SaveAs(docxfilename, 12, False, "", True, "", False, False, False, False)
    doc.Close()
    word.Quit()
    FindFileByAuthor(docxfilename)




def Opfile(filename):
    if filename[-4:] == ".doc":
        transToDocx(filename)
    elif filename[-4:] == 'docx':
        FindFileByAuthor(filename)
    else:
        pass

def gci(filepath):
    # 遍历filepath下所有文件，包括子目录
    files = os.listdir(filepath)
    for fi in files:
        fi_d = os.path.join(filepath, fi)
        if os.path.isdir(fi_d):
            gci(fi_d)
        else:
            Opfile(os.path.join(filepath, fi_d))

gci(maindir)
print('is End!')


'''
word = wc.Dispatch('Word.Application')
doc = word.Documents.Open(u'D:\\公司文档库\\filesys2011\\2011.03\\10140.doc')  # 目标路径下的文件
doc.
doc.SaveAs(u'D:\\公司文档库\\filesys2011\\2011.03\\10140.docx', 12, False, "", True, "", False, False, False, False) # 转化后路径下的文件
doc.Close()
word.Quit()
# f = open('C:/Users/李军/Documents/行政复议申请书.docx', 'rb')
f=open('D:\\公司文档库\\filesys2011\\2011.03\\10140.docx','rb')
document = Document(f)

core_properties = document.core_properties

if (core_properties.author=='陈莉英'):
    print('isok')
else:
    print('isnotok')

print('作者',core_properties.author)
f.close()
'''