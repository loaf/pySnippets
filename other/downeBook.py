#!python3
# coding: utf-8
# internal-version-tracking: 143

import os
import random
import re
import string
import sys
import time
import json

import urllib.error
import urllib.parse
import urllib.request
import requests
import fake_useragent
from bs4 import BeautifulSoup


def GetSoup(url):
    pageSoup = None

    htmlfile = open(url, 'r', encoding='utf-8')
    htmlhandle = htmlfile.read()
    pageSoup = BeautifulSoup(htmlhandle, 'html.parser')

    return pageSoup

#

def GetHead(url):
    responseCode = 0
    headersUserAgent = {'User-Agent': randomUserAgent}

    try:

        if useProxies:
            response = requests.head(url, headers=headersUserAgent, proxies=proxyDict, timeout=requestMaxTimeout,
                                     verify=False, allow_redirects=False)
        else:
            response = requests.head(url, headers=headersUserAgent, timeout=requestMaxTimeout, verify=False,
                                     allow_redirects=False)
        #

        responseCode = int(str(response.status_code))

    except:

        print('Problem connecting to ' + url + '\n' + str(sys.exc_info()[0]))
        pass
    #

    if responseCode == 200:

        responseHeaders = response.headers

    else:

        responseHeaders = ''

    #

    # Returns the results
    return responseHeaders

#

def EvaluateAccordingToRules(bookTitle):
    bookWanted = True

    # print('processing rule for ' + bookTitle)

    for ruleEntry in ruleList:

        # startswith
        try:
            if not ruleEntry['startswith'] == None:
                # print('Has startswith')
                if ruleEntry['case_sensitive']:
                    # print('is case sense')
                    if bookTitle.startswith(ruleEntry['startswith']):
                        # print('Rule match, setting to ' + str(ruleEntry['wanted']))
                        bookWanted = ruleEntry['wanted']
                        break
                #
                else:
                    # print('is not case sense')
                    if bookTitle.lower().startswith(ruleEntry['startswith'].lower()):
                        bookWanted = ruleEntry['wanted']
                        break
                #
            #
        #
        except KeyError:
            pass
        #

        # endswith
        try:
            if not ruleEntry['endswith'] == None:
                if ruleEntry['case_sensitive']:
                    if bookTitle.endswith(ruleEntry['endswith']):
                        bookWanted = ruleEntry['wanted']
                        break
                #
                else:
                    if bookTitle.lower().endswith(ruleEntry['endswith'].lower()):
                        bookWanted = ruleEntry['wanted']
                        break
                #
            #
        #
        except KeyError:
            pass
        #

        # contains
        try:
            if not ruleEntry['contains'] == None:
                if ruleEntry['case_sensitive']:
                    if ruleEntry['contains'] in bookTitle:
                        bookWanted = ruleEntry['wanted']
                        break
                #
                else:
                    if ruleEntry['contains'].lower() in bookTitle.lower():
                        bookWanted = ruleEntry['wanted']
                        break
                #
            #
        #
        except KeyError:
            pass
        #

        # is
        try:
            if not ruleEntry['is'] == None:
                if ruleEntry['case_sensitive']:
                    if bookTitle == ruleEntry['is']:
                        bookWanted = ruleEntry['wanted']
                        break
                #
                else:
                    if bookTitle.lower() == ruleEntry['is'].lower():
                        bookWanted = ruleEntry['wanted']
                        break
                #
            #
        #
        except KeyError:
            pass
    #
    #

    return bookWanted


#


def DownloadFile(fileURL, filePath, fileName):
    downloadSuccessful = False

    if not os.path.isfile(os.path.join(filePath, fileName)):

        try:
            headersUserAgent = {'User-Agent': randomUserAgent}

            if useProxies:
                response = requests.get(fileURL, stream=True, headers=headersUserAgent, proxies=proxyDict,
                                        timeout=requestMaxTimeout, verify=False, allow_redirects=False)
            else:
                response = requests.get(fileURL, stream=True, headers=headersUserAgent, timeout=requestMaxTimeout,
                                        verify=False, allow_redirects=False)
            #

            with open(os.path.join(filePath, fileName), 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                #
            #
            #

            if os.path.isfile(os.path.join(filePath, fileName)):
                downloadSuccessful = True
        #

        except KeyboardInterrupt:

            print('Download aborted, removing incomplete file')

            os.remove(os.path.join(filePath, fileName))

            sys.exit('Aborting script, bye!')

            pass

        except FileNotFoundError as e:

            print('Problem creating file to download to, might be because disc is full?')

        except:

            # input('Problem with download: ' + '\n' + str(sys.exc_info()[0]))	# Enable for more verbosive troubleshooting
            print('Problem with download, skipping...')
        #

        if downloadSuccessful:
            print('File downloaded successfully')
    #

    else:

        print('File ' + str(fileName) + ' downloaded before, skipping')



def DownloadLibrary():

    print('Enumerating books')
    pageSoup = GetSoup(inputHtml)

    outputFile = os.path.join(libraryStorage, outputFileName)

    # Find all elements in the HTML-soup
    listingTable = pageSoup.find('table', id='listing')
    bookRows = listingTable.findAll('tr')

    # Figures out the number of books in the library
    bookCount = pageSoup.find('div', class_='navigation').find('span').text
    bookCount = int(bookCount[bookCount.rfind(' '):].strip())

    # Compares above number to the loaded table-rows. You'll probably never see this message, unless the library has just under 10 million books...
    if not len(bookRows) == bookCount:
        input('Halted, mismatch between found books and fetched books!' + '\n' + 'bookCount: ' + str(
            bookCount) + '\n' + 'len(bookRows): ' + str(len(bookRows)))
        pass
    #


    print('Library ' +  ' contains ' + str(bookCount) + ' books, iterating over them')
    #

    bookCountCurrent = 1

    for bookRow in bookRows:

        bookTitleAuthor = str(BeautifulSoup(str(bookRow.find('span', class_='first-line')),
                                            'html.parser').text).strip()  # Yes, a kludge, but had problems reading the .text from it otherwise
        bookAuthor = bookTitleAuthor[bookTitleAuthor.rfind(' by ') + len(' by '):].strip()
        bookTitle = bookTitleAuthor[:bookTitleAuthor.rfind(' by ')].strip()
        bookInformation = bookRow.find('span', class_='second-line').get_text().strip()

        if 'Tags=[' in bookInformation:
            bookTags = bookInformation[bookInformation.find(' Tags=[') + len(' Tags=['):bookInformation.rfind(
                '] Formats=[')].strip().split(',')
            bookTags = map(str.strip, bookTags)
        #

        hasWantedFormat = False
        bookWanted = True
        informUser = True
        listBooks = []

        downloadButtons = bookRow.findAll('span', class_='button')
        for downloadButton in downloadButtons:
            bookItem = {}
            bookItem['format'] = str(downloadButton.text).lower().strip()
            bookItem['url'] = 'http://' + serverAddress + str(downloadButton.find('a')['href']).strip()

            listBooks.append(bookItem)

        #

        for listItem in listBooks:

            if str(listItem['format']).lower() in wantedFormats:
                hasWantedFormat = True
        #
        #

        bookWanted = EvaluateAccordingToRules(bookTitle)

        initiateDownload = False

        if bookWanted and hasWantedFormat:

            downloadBook = True

            for listItem in listBooks:

                bookFormat = listItem['format']
                bookURL = listItem['url']

                bookFilename = bookURL[bookURL.rfind(r'/') + 1:]
                bookFilename = urllib.parse.unquote(bookFilename)
                bookFilename = bookFilename.encode('utf-8', 'ignore').decode().encode('ascii', 'ignore').decode()

                # A special operation, if script is running on windows and filename exceeds 200 chars
                if (os.name == 'nt') and (len(bookFilename) > 200):

                    # Makes sure we're only keeping ASCII-characters
                    bookTitleEncoded = bookTitle.encode('ascii', 'ignore').decode()

                    # Further more, remove disallowed filename-characters
                    bookTitleEncoded = re.sub(r'[\\/:"*?<>|]+', '', bookTitleEncoded)

                    if len(bookTitleEncoded) > 150:
                        bookTitleEncoded = bookTitleEncoded[:150]
                    #

                    bookFilename = bookTitleEncoded + '__' + bookFilename[bookFilename.rfind('.'):]

                #

                fileExtension = bookFilename.split('.')[-1].lower()

                # Removes the calibre-numering from the filename
                # ie
                # Evan and Elle - Rhys Bowen_9423.epub
                # or
                # Eternity Road - Jack McDevitt_273.epub
                r1 = re.compile('_' + '[0-9]+' + '.' + fileExtension + '$')  # regular expression corrected
                if r1.search(bookFilename.lower()):  # re.match() replaced with re.search()
                    bookFilename = bookFilename[:bookFilename.rfind('_')] + '.' + fileExtension
                #

                baseFileName = bookFilename[:bookFilename.rfind('.')]

                # Lots of duplicates avoided by using these two removals
                if baseFileName.endswith('_A Novel'):
                    baseFileName = baseFileName[:-len('_A Novel')]
                #

                if baseFileName.endswith('_ A Novel'):
                    baseFileName = baseFileName[:-len('_ A Novel')]
                #

                if not os.path.isfile(os.path.join(libraryStorage, bookFilename)):

                    for wantedFormat in wantedFormats:

                        if (bookFormat == wantedFormat) and downloadBook:

                            availableFormatIndex = wantedFormats.index(bookFormat)
                            existingItem = False

                            for formatName in wantedFormats:

                                if os.path.isfile(os.path.join(libraryStorage, baseFileName + '.' + formatName)):

                                    existingItem = True

                                    existingFormat = formatName
                                    existingFormatIndex = wantedFormats.index(existingFormat)

                                    if availableFormatIndex < existingFormatIndex:
                                        print('Oh, we already have this book (' + baseFileName + ') in ' + str(
                                            existingFormat).upper() + ' but now we can grab it in a better format: ' + bookFormat.upper())
                                        initiateDownload = True
                                #

                            #
                            #

                            if not existingItem:
                                initiateDownload = True
                            #

                            if initiateDownload:
                                dateTimeNow = time.strftime('%Y-%m-%d %H:%M:%S')

                                print(dateTimeNow + '\n' + 'Book ' + str(bookCountCurrent) + '/' + str(
                                    bookCount) + '\n' + bookTitle + ' by ' + bookAuthor)

                                # Grab headers to calculate book size
                                fileHeaders = GetHead(bookURL)
                                fileSizeMB=0
                                #fileSizeB = int(fileHeaders[r'Content-Length'])
                                #fileSizeMB = round((fileSizeB / 1024 / 1024), 2)

                                print(
                                    'Downloading book in ' + str(bookFormat).upper() + ' (' + str(fileSizeMB) + ' MB)')

                                DownloadFile(bookURL, libraryStorage, bookFilename)

                                bookList = open(outputFile, mode='a', encoding='utf-8')
                                bookList.write(
                                    dateTimeNow + '|' + serverAddress + '|' + bookAuthor + '|' + bookTitle + '|' + bookFilename + '\n')
                                bookList.close()

                                downloadBook = False

                                print('-----------------[' + str(serverAddress) + ']-----------------')

                                time.sleep(1.5)
                        #

                    #
                #
                else:
                    downloadBook = False
            #
        #

        else:
            # print(dateTimeNow + '\n' + 'Book ' + str(bookCountCurrent) + '/' + str(bookCount) + '\n' + bookTitle + ' by ' + bookAuthor + ' skipped, because it did not have any of the defined formats')
            pass
        #

        bookCountCurrent = bookCountCurrent + 1



    print('Library ' + str(calibreAddress) + ' processed' + '\n' + '----------------------------------')


#


#
# <CONFIGURABLES>
#


#
requests.packages.urllib3.disable_warnings()
proxyDict = {}
randomUserAgent = fake_useragent.UserAgent().random
calibreAddresses = []

jsonRulesData = open('rules.json', mode='r', encoding='utf8').read()
ruleList = json.loads(jsonRulesData)['rules']

useProxies = False
requestMaxTimeout = 300

wantedFormats = ['kfx', 'azw4', 'azw3', 'azw', 'epub', 'mobi']
outputFileName = 'booklist.txt'
libraryStorage = r'e:\Temp\all3'
inputHtml=r'e:\Temp\2.html'

#
# </CONFIGURABLES>
#

if useProxies:
    proxyString = 'SOCKS5://username:P@ssw0rd@proxy.example.com:3128'  # Example of proxy-string
    proxyDict = {"http": proxyString, "https": proxyString}
#


scriptInput = "220.189.209.76:8080"
serverAddress = scriptInput.lower()

print('Connecting to ' + serverAddress)

isCalibre = False
isOpen = False
multiLibrary = False
pageSoup = ''

responseHeaders = GetHead(r'http://' + serverAddress)

if 'Server'.lower() in str(responseHeaders).lower():

        serverType = responseHeaders['Server'].lower()

        if 'calibre' in serverType:

            isCalibre = True

            pageSoup = GetSoup(inputHtml)

            if not pageSoup == None:

                print('Connection to an open calibre-server successfully established')

                isOpen = True
            #
            else:
                print(str(serverAddress) + ' is running, but is password-protected :-(')
        #
        else:
            print(str(serverAddress) + ' is running, but not a calibre library')
else:
    print(str(serverAddress) + ' is not running a webserver')
    #

if isCalibre and isOpen:
    DownloadLibrary()

#