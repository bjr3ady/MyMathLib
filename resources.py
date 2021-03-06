from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from PyQt4.QtWebKit import *
from myQwebview import myqwebview
import markdown, os, shutil, xlrd, pyperclip, re, time, lxml, glob, filecmp
from time import gmtime, strftime
import latex2mathml
from bs4 import BeautifulSoup
import win32com
from win32com.client import Dispatch, constants
try: import mdx_mathjax
except: pass

mdProcessor = markdown.Markdown(extensions=['mathjax'])

CUR_VERSION = "广东省育苗杯电子题库\n版本：2016.0706.1.0"
CUR_CONTACT = "如有任何问题请联系：mybsppp@163.com\n\n程序开发：赵小娜\n2016"

def globaldb():
    db = QSqlDatabase.addDatabase("QSQLITE");
    db.setDatabaseName("myQuestion.db")
    if not db.open():
        QMessageBox.warning(None, "错误",  "数据库连接失败: %s" % db.lastError().text())
        sys.exit(1)
    return db


class ComboBoxDelegate(QItemDelegate):
    def __init__(self, parent, itemslist=["a", "b", "c"]):
        QItemDelegate.__init__(self, parent)
        self.itemslist = itemslist
        self.parent = parent

    def createEditor(self, parent, option, index):
        self.editor = QComboBox(parent)
        self.editor.addItems(self.itemslist)
        self.editor.setCurrentIndex(0)
        self.editor.installEventFilter(self)
        return self.editor

    def setEditorData(self, editor, index):
        curtxt = index.data(Qt.DisplayRole)
        # print(type(curtxt)== QPyNullVariant )
        if type(curtxt) == type(1):
            curindx = int(index.data(Qt.DisplayRole))
            curtxt = self.itemslist[curindx]
        elif type(curtxt)== QPyNullVariant:
            curtxt = ""
        pos = self.editor.findText(curtxt)
        if pos == -1:
            pos = 0
        self.editor.setCurrentIndex(pos)


    def setModelData(self,editor,model,index):
        curindx = self.editor.currentIndex()
        text = self.itemslist[curindx]
        model.setData(index, text)

class DragImgTextEdit(QTextEdit):
    def __init__(self, type, parent=None):
        super(DragImgTextEdit, self).__init__(parent)
        self.setAcceptDrops(True)
        # self.setIconSize(QtCore.QSize(72, 72))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.emit(SIGNAL("dropped"), links)
        else:
            event.ignore()
