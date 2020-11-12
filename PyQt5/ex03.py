# Coding=utf8
from PyQt5.QtCore import QObject,pyqtSlot
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QSystemTrayIcon,QApplication

'''这个类定义浏览器视图的内容'''
class BrowserScreen(QWebEngineView):
    def __init__(self):
        QWebEngineView.__init__(self)

        self.resize(800, 600)
        self.show()
        #增加了一行 <script src="qrc:///qtwebchannel/test.js"></script>
        self.setHtml("""
            <script src="qrc:///qtwebchannel/test.js"></script>
           <script>function message() { return "Clicked!"; }</script>
           <h1>QtWebKit + Python sample program</h1>
           <input type="button" value="Click JavaScript!"
                  onClick="alert('[javascript] ' + message())"/>
           <input type="button" value="Click Python!"
                  onClick="python.alert('[python] ' +
                                        python.message())"/>
           <br />

           <iframe src="http://www.so.com/"
                   width="750" height="500"
                   scrolling="no"
                   frameborder="0"
                   align="center"></iframe>
        """)
        self.createTrayIcon()
        self.trayIcon.show()

    def createTrayIcon(self):
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon("images/trash.png"))

    def showMessage(self, msg):
        self.trayIcon.showMessage("This is Python", msg,
            QSystemTrayIcon.MessageIcon(0), 15 * 1000)

class PythonJS(QObject):

    @pyqtSlot()
    def alert(self, msg):
        self.emit(pyqtSignal('contentChanged(const QString &)'), msg)

    @pyqtSlot()
    def message(self):
        return "Click!"

if __name__=='__main__':
    import sys
    app = QApplication(sys.argv)
    browser = BrowserScreen()
    pjs = PythonJS()

    #加一个channel
    channel=QWebChannel()
    handler=CallHandler()
    browser.page().mainFrame().addToJavaScriptWindowObject("python", pjs)
    QObject.connect(pjs, SIGNAL("contentChanged(const QString &)"),
                    browser.showMessage)

    sys.exit(app.exec_())
