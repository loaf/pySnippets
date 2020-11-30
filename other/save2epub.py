# encoding:utf-8
# !/usr/bin/python3
import zipfile
import os.path

'''
Script Name     : createEpubBook.py
Author          : svoid
Created         : 2015-03-28
Last Modified   : 
Version         : 1.0
Modifications   : 
Description     : 根据HTML生成epub文档
'''


def create_mimetype(epub):
    epub.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)


def create_container(epub):
    container_info = '''<?xml version="1.0" encoding="utf-8" standalone="no"?>
    <container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
      <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
      </rootfiles>
  </container>
    '''
    epub.writestr('META-INF/container.xml', container_info, compress_type=zipfile.ZIP_STORED)


def create_content(epub, path):
    content_info = '''
    <?xml version="1.0" encoding="utf-8" standalone="no"?>
    <package xmlns="http://www.idpf.org/2007/opf" 
             xmlns:dc="http://purl.org/dc/elements/1.1/" 
             unique-identifier="bookid" version="2.0">
      <metadata>
        <dc:title>Hello World: My First EPUB</dc:title>
        <dc:creator>Svoid</dc:creator>
        <dc:identifier id="bookid">urn:uuid:12345</dc:identifier>
        <meta name="cover" content="cover-image" />
      </metadata>
      <manifest>
          %(manifest)s
        <item id="ncx" href="toc.ncx" media-type="text/xml"/>
        <item id="content" href="content.html" media-type="application/xhtml+xml"/>
        <item id="css" href="stylesheet.css" media-type="text/css"/>
      </manifest>
      <spine toc="ncx">
          %(spine)s
        <itemref idref="cover" linear="no"/>
        <itemref idref="content"/>
      </spine>
      <guide>
        <reference href="cover.html" type="cover" title="Cover"/>
      </guide>
    </package>
    '''
    manifest = ''
    spine = ''
    for html in os.listdir(path):
        basename = os.path.basename(html)
        if basename.endswith('html'):
            manifest += '<item id="%s" href="%s" media-type="application/xhtml+xml"/>' % (basename, basename)
            spine += '<itemref idref="%s"/>' % (basename)
    epub.writestr('OEBPS/content.opf', content_info % {
        'manifest': manifest,
        'spine': spine, },
                  compress_type=zipfile.ZIP_STORED)


def create_stylesheet(epub):
    css_info = '''
        body {
          font-family: sans-serif;     
        }
        h1,h2,h3,h4 {
          font-family: serif;     
          color: red;
        }
    '''
    epub.writestr('OEBPS/stylesheet.css', css_info, compress_type=zipfile.ZIP_STORED)


def create_archive(path):
    epub_name = '%s.epub' % os.path.basename(path)
    os.chdir(path)
    epub = zipfile.ZipFile(epub_name, 'w')
    create_mimetype(epub)
    create_container(epub)
    create_content(epub, path)
    create_stylesheet(epub)
    for html in os.listdir('.'):
        basename = os.path.basename(html)
        if basename.endswith('html'):
            epub.write(html, 'OEBPS/' + basename, compress_type=zipfile.ZIP_DEFLATED)
    epub.close()


if __name__ == '__main__':
    path = 'D:\\persion\\epub\\test1'
    create_archive(path)