import sys,os,time
from PyQt4 import QtGui
from PyQt4 import QtCore
#from ticker_import import *
from fetchBlp import fetchBlp
from resultParser import resultParser
from cluster_interaction import RemoteInterface
import numpy as np

class submitPress(QtCore.QObject):
    def __init__(self, parent):
        super(submitPress,self).__init__()
        self.par=parent
        self.sendList=[]

    def send(self):
        self.sendList.insert(1,str(self.l3.text()))
        self.sendList.insert(1,str(self.l2.text()))
        self.sendList.insert(1,str(self.l1.text()))
        print(self.sendList)
        try:
            os.remove('simpredResults.txt')
        except OSError:
            pass
        remoteInterface = RemoteInterface(self.sendList[1], ['-e'] +[str(self.sendList[4])]+ self.sendList[5:])
        remoteInterface.submit_job()
        while True:
            if os.path.isfile('simpredResults.txt'):
                r=resultParser()
                self.par.result(r.response)
                break
        
    def dialog(self):
        self.mess=QtGui.QWidget()
        self.mess.setWindowFlags(QtCore.Qt.Dialog)
        self.mess.setWindowTitle("SSH")
        self.mess.resize(300, 200)
        self.box=QtGui.QGridLayout()
        self.box.addWidget(QtGui.QLabel("IP"),0,0)
        self.box.addWidget(QtGui.QLabel("Username"),1,0)
        self.box.addWidget(QtGui.QLabel("Password"),2,0)
        self.l1=QtGui.QLineEdit()
        self.l1.setText("10.188.164.9")
        self.l2=QtGui.QLineEdit()
        self.l3=QtGui.QLineEdit()
        self.box.addWidget(self.l1,0,1)
        self.box.addWidget(self.l2,1,1)
        self.box.addWidget(self.l3,2,1)
        self.but=QtGui.QPushButton("Ok")
        self.box.addWidget(self.but,3,1)
        self.connect(self.but, QtCore.SIGNAL("clicked()"), self.send)
        self.connect(self.but, QtCore.SIGNAL("clicked()"), self.mess.close)
        self.mess.setLayout(self.box)
        self.mess.show()

    def clicked(self):
        if self.par.cur.text() != "":
            #print(self.par.remoteGroup.checkedButton().text())
            self.sendList=[]
            if self.par.remoteGroup.checkedButton().text()=="Remote":
                self.sendList.append('-e')
            strList=self.par.actNumFunc.keys()
            numList=[]
            for i in strList:
                numList.append(self.par.prefNumFunc.get(str(i),0))
            self.sendList.append(numList)
            if self.par.metLine.currentIndex() == 0:
                self.sendList.append('-svm')
            elif self.par.metLine.currentIndex() == 1:
                self.sendList.append('-dt')
            elif self.par.metLine.currentIndex() == 2:
                self.sendList.append('-g')
            n=self.par.prefNum.get(str(self.par.cur.text()),0)
            self.sendList.append('-row'+str(n))
            self.dialog()

class mainWid(QtGui.QWidget):

    def __init__(self, parent):
        super(mainWid,self).__init__()
        self.par=parent
        self.initUI()        

    def selectStock(self, stc):
        if stc == self.cur:
            self.stock.setText('')
        else:
            self.stock.setText(stc.text())
            self.disconnect(self.model2, QtCore.SIGNAL("itemChanged(QStandardItem*)"), self.selectStock)
            self.cur.setCheckState(QtCore.Qt.Unchecked)
            self.connect(self.model2, QtCore.SIGNAL("itemChanged(QStandardItem*)"), self.selectStock)
            self.cur = stc

    '''def setUpList(self, listStock):
        for i in listStock:
            item = QtGui.QStandardItem(i)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
            #self.butGroup.addButton(item)
            self.model.appendRow(item)

        self.connect(self.model, QtCore.SIGNAL("itemChanged(QStandardItem*)"),self.par.butCheck)
        #proxy = QtGui.QSortFilterProxyModel()
        #proxy.setSourceModel(self.model)
        self.stList.setModel(self.model)
        #self.connect(filterLineEdit, QtCore.SIGNAL("textChanged(QString)"),proxy.setFilterFixedString)

        self.prefNum=dict()
        self.prefNum= dict()
        j=1
        for i in sp100:
            self.prefNum[i]=j
            j+=1
        self.actNum=dict()
        self.prefNumFunc=dict()
        for i in range(1,11):
            self.prefNumFunc["F"+str(i)]=i
        self.actNumFunc=dict()'''
        

    #click predict
    def predClick(self):
        self.cur=QtGui.QStandardItem()
        #stuff happens from other api
        #pop-up shows up
        self.mess=QtGui.QWidget()
        #self.mess.setWindowFlags(QtCore.Qt.Dialog)
        #self.mess.setWindowTitle("Results")
        #self.mess.resize(300,200)
        vbox=QtGui.QGridLayout()
        vbox.addWidget(QtGui.QLabel("Target Stock"),0,0)

        listBox=QtGui.QVBoxLayout()
        #list prototype
        self.stList2=QtGui.QListView()
        seaLabel2=QtGui.QLabel("Search: ")
        filterLineEdit2=QtGui.QLineEdit()
        if sys.version_info[0] == 3:
            filterLineEdit2.setValidator(upValidator3())
        else:
            filterLineEdit2.setValidator(upValidator2())
        tmpHbox=QtGui.QHBoxLayout()
        tmpHbox.addWidget(seaLabel2)
        tmpHbox.addWidget(filterLineEdit2)
        listBox.addLayout(tmpHbox)
        listBox.addWidget(self.stList2)

        self.model2 = QtGui.QStandardItemModel()
        
        for i in self.lSide.rowNames:
            item = QtGui.QStandardItem(i)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
            #self.butGroup.addButton(item)
            self.model2.appendRow(item)

        self.connect(self.model2, QtCore.SIGNAL("itemChanged(QStandardItem*)"), self.selectStock)
        proxy = QtGui.QSortFilterProxyModel()
        proxy.setSourceModel(self.model2)
        self.stList2.setModel(proxy)
        self.connect(filterLineEdit2, QtCore.SIGNAL("textChanged(QString)"),proxy.setFilterFixedString)
        
        #self.connect(clearAll, QtCore.SIGNAL("clicked()"), self.selectStock)
        vbox.addLayout(listBox,0,1)

        vbox.addWidget(QtGui.QLabel("Selected Stock:"),1,0)
        self.stock=QtGui.QLabel("")
        vbox.addWidget(self.stock,1,1, QtCore.Qt.AlignCenter)

        vbox.addWidget(QtGui.QLabel("Select ML Algorithm"),2,0)
        self.metLine=QtGui.QComboBox()
        self.metLine.addItem("Support Vector Machine")
        self.metLine.addItem("Decision Tree")
        self.metLine.addItem("Guassian")
        vbox.addWidget(self.metLine,2,1)
        #self.metLine.addItem("DJIA")

        self.remoteGroup=QtGui.QButtonGroup()
        hbox=QtGui.QHBoxLayout()
        but1=QtGui.QRadioButton("Local")
        but2=QtGui.QRadioButton("Remote")
        self.remoteGroup.addButton(but1)
        self.remoteGroup.addButton(but2)
        self.remoteGroup.setExclusive(True)
        but2.setChecked(True)
        hbox.addWidget(but1)
        hbox.addWidget(but2)
        vbox.addWidget(QtGui.QLabel("Job Type"),3,0)
        vbox.addLayout(hbox,3,1)
        butSubmit=QtGui.QPushButton("Submit")#needs new name
        self.sub=submitPress(self)
        self.connect(butSubmit, QtCore.SIGNAL("clicked()"), self.sub.clicked)
        vbox.addWidget(butSubmit,4,1)

        
        #but=QtGui.QPushButton("Close")
        #vbox.addWidget(but)
        self.mess.setLayout(vbox)
        #but.setMaximumWidth(100)
        #but.connect(but, QtCore.SIGNAL("clicked()"), self.mess.close)
        #self.mess.show()
        self.tabs.insertTab(1,self.mess,"Predict")
        #self.tabs.setCurrentIndex(1)

    def initUI(self):
        #current list location:
        #(self.master, self.test, self.train) = tickers()
        #hbox
        self.hbox=QtGui.QHBoxLayout()
        self.tabs=QtGui.QTabWidget()
        #table
        self.table=QtGui.QTableWidget(0,1,self)
        self.table.setHorizontalHeaderItem(0,QtGui.QTableWidgetItem("Ticker"))
        self.table.setMaximumWidth(self.par.size().width()*4/5)
        self.table.setMinimumWidth(self.par.size().width()*4/5-50)
        self.table.setMaximumHeight(self.par.size().height()*7/8)
        self.table.setMinimumHeight(self.par.size().height()*7/8-50)
        #input window
        self.lSide=inputWid(self)
        self.hbox.addWidget(self.lSide, 0, QtCore.Qt.AlignLeft)
        self.tabs.insertTab(0,self.table, "Stocks")
        self.hbox.addWidget(self.tabs, 0, QtCore.Qt.AlignTop)
        #vbox
        '''self.vbox=QtGui.QVBoxLayout()
        self.vbox.addLayout(self.hbox)
        #hbox2
        self.hbox2=QtGui.QHBoxLayout()
        #buttons, built, predict, test
        self.fetchBut=QtGui.QPushButton("Fetch")
        self.fetchBut.setDisabled(True)
        #testBut=QtGui.QPushButton("Test")
        predictBut=QtGui.QPushButton("Predict")
        self.connect(predictBut, QtCore.SIGNAL("clicked()"), self.predClick)
        self.hbox2.addWidget(self.fetchBut)
        self.hbox2.addItem(QtGui.QSpacerItem(200,25))
        self.hbox2.addWidget(predictBut)
        self.vbox.addLayout(self.hbox2)'''
        self.setLayout(self.hbox)
        #preference dictionaries
        self.prefNum=dict()
        self.actNum=dict()
        '''self.prefNum=dict()
        self.prefNum= dict()
        j=1
        for i in sp100:
            self.prefNum[i]=j
            j+=1
        self.actNum=dict()'''
        self.prefNumFunc=dict()
        tmpNames = ('1 day price change', '3 day price change', '5 day price change', '6 month price change', '12 month price change', 'Volatility 90 days', 'Price sales ratio', 'Price earnings ratio', 'Insider held shares', 'Price book ratio' )
        for i in range(1,11):
            self.prefNumFunc[tmpNames[i-1]]=i
        self.actNumFunc=dict()
        self.predClick()

    #event for checking/unchecking stocks
    def butCheck(self, butt):
        if (butt.checkState()==QtCore.Qt.Checked):
            pref=self.prefNum.get(butt.text(),0)
            addN = True
            for i in range(self.table.rowCount()):
                if self.prefNum.get(self.table.item(i,0).text(),0) > pref:
                    self.table.insertRow(i)
                    self.table.setItem(i,0,QtGui.QTableWidgetItem(butt.text()))
                    self.actNum.clear()
                    for i in range(1,self.table.rowCount()):
                        self.actNum[self.table.item(i,0).text()]=i
                    addN = False
                    break
            if addN:
                self.table.setRowCount(self.table.rowCount()+1)
                self.actNum[butt.text()]=self.table.rowCount()-1
                self.table.setItem(self.actNum.get(butt.text(),0),0,QtGui.QTableWidgetItem(butt.text()))
        else:
            self.table.removeRow(self.actNum.get(butt.text(),0))
            self.actNum.clear()
            for i in range(self.table.rowCount()):
                self.actNum[self.table.item(i,0).text()]=i

    #event for checking/unchecking functions
    def butCheckFunc(self, but):
        butt=self.lSide.butGroupFunc.button(but)
        if (butt.checkState()==QtCore.Qt.Checked):
            pref=self.prefNumFunc.get(str(butt.text()),0)
            addN = True
            for i in range(1,self.table.columnCount()):
                if self.prefNumFunc.get(self.table.horizontalHeaderItem(i).text()) > pref:
                    self.table.insertColumn(i)
                    self.table.setHorizontalHeaderItem(i,QtGui.QTableWidgetItem(butt.text()))
                    self.actNumFunc.clear()
                    for i in range(1,self.table.columnCount()):
                        self.actNumFunc[self.table.horizontalHeaderItem(i).text()]=i
                    addN = False
                    print("dfd")
                    for j in range(0,self.table.rowCount()):
                        self.table.setItem(j,i,QtGui.QTableWidgetItem(self.lSide.data[self.prefNum.get(self.table.item(j,0).text(),0),pref]))
                    break
            if addN:
                self.table.setColumnCount(self.table.columnCount()+1)
                self.actNumFunc[butt.text()]=self.table.columnCount()-1
                self.table.setHorizontalHeaderItem(self.actNumFunc.get(butt.text(),0),QtGui.QTableWidgetItem(butt.text()))
                for j in range(0,self.table.rowCount()):
                    #print(j)
                    #print('dfdds')
                    #print(j,self.table.columnCount())
                    #print(self.lSide.data[0,0])
                    item=QtGui.QTableWidgetItem()
                    #print(item.text())
                    #item.setData(QtCore.Qt.DisplayRole, str(self.lSide.data[self.prefNum.get(self.table.item(j,0).text(),0),pref]))
                    item.setText(str(self.lSide.data[self.prefNum.get(str(self.table.item(j,0).text()),0)-1,pref]))
                    #print(item.text())
                    #print(self.prefNum)
                    #print(self.table.item(j,0).text())
                    #print(self.lSide.data[self.prefNum.get(str(self.table.item(j,0).text()),0),pref])
                    self.table.setItem(j,self.table.columnCount()-1,item)
                    item=0
        else:
            self.table.removeColumn(self.actNumFunc.get(butt.text(),0))
            self.actNumFunc.clear()
            for i in range(1, self.table.columnCount()):
                self.actNumFunc[self.table.horizontalHeaderItem(i).text()]=i

    def openBox(self):
        fileName=QtGui.QFileDialog.getOpenFileName(self,"Open Model")
        print(fileName)

    def saveBox(self):
        fileName=QtGui.QFileDialog.getSaveFileName(self,"Save Model")
        print(fileName)

    def resizeEvent(self, event):
        self.table.setMaximumWidth(event.size().width()*4/5)
        self.table.setMinimumWidth(event.size().width()*4/5-50)
        self.table.setMaximumHeight(event.size().height()*7/8)
        self.table.setMinimumHeight(event.size().height()*7/8-50)
        
    def result(self, res):
        self.pic=QtGui.QLabel()
        if res > .5:
            self.pic.setPixmap(QtGui.QPixmap(QtCore.QString("buffet_happy.jpg")))
        else:
            self.pic.setPixmap(QtGui.QPixmap(QtCore.QString("buffet_sad.jpg")))
        self.tabs.insertTab(2,self.pic,"Result")
        self.tabs.setCurrentIndex(2)

class upValidator3(QtGui.QValidator):
#makes sure input is always capital
    def __init__(self, parent=None):
        super(upValidator3,self).__init__(parent)

    def validate(self, st, pos):
        st = st.upper()
        return (QtGui.QValidator.Acceptable, st, pos)

class upValidator2(QtGui.QValidator):
#makes sure input is always capital
    def __init__(self, parent=None):
        super(upValidator2,self).__init__(parent)

    def validate(self, st, pos):
        if st == st.toUpper():
            return (QtGui.QValidator.Acceptable, pos)
        else:
            return (QtGui.QValidator.Invalid, pos)

class inputWid(QtGui.QWidget):
#holds the input on the left side of screen
    def __init__(self, parent):
        super(inputWid,self).__init__()
        self.par=parent
        self.initUI()
        self.rowNames=[]

    def setUpList(self, listStock):
        self.clear()
        #self.model.setRowCount(0)
        self.model=QtGui.QStandardItemModel()
        self.par.model2.setRowCount(0)
        for i in listStock:
            item = QtGui.QStandardItem(i)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
            #self.butGroup.addButton(item)
            self.model.appendRow(item)

        self.connect(self.model, QtCore.SIGNAL("itemChanged(QStandardItem*)"),self.par.butCheck)
        #proxy = QtGui.QSortFilterProxyModel()
        #proxy.setSourceModel(self.model)
        #self.stList.setModel(proxy)
        #self.connect(self.filterLineEdit, QtCore.SIGNAL("textChanged(QString)"),proxy.setFilterFixedString)

        self.par.prefNum=dict()
        j=1
        for i in listStock:
            self.par.prefNum[i]=j
            j+=1
        self.par.actNum=dict()

        for i in self.rowNames:
            item = QtGui.QStandardItem(i)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
            #self.butGroup.addButton(item)
            self.par.model2.appendRow(item)
        
#clears the checks
    def clear(self):
            for i in range(self.model.rowCount()):
                self.model.item(i).setCheckState(QtCore.Qt.Unchecked)

    def check(self):
            for i in range(self.model.rowCount()):
                self.model.item(i).setCheckState(QtCore.Qt.Checked)

    def stockChanged(self, num):
        if (num == 0):
            self.fetchBut.setDisabled(True)
        else:
            self.fetchBut.setDisabled(False)

    def fetchScr(self):
        n=self.stockLine.currentIndex()
        fetchBlp(n)
        f=np.load("simpredRawData.npz")
        self.rowNames=f["rowNames"]
        self.data=f["data"]
        #print(self.data[0,:])
        self.setUpList(self.rowNames)
        self.check()

    def initUI(self):
        self.vbox=QtGui.QVBoxLayout()
        #list prototype
        sheet="font-size:13pt;"
        stcName=QtGui.QLabel("Stocks")
        stcName.setStyleSheet(sheet)
        self.vbox.addWidget(stcName,0,QtCore.Qt.AlignCenter)
        self.stockLine=QtGui.QComboBox()
        self.stockLine.addItem("Please Select One")
        self.stockLine.addItem("S&P 100")
        self.stockLine.addItem("S&P 500")
        self.stockLine.addItem("DJIA")
        self.connect(self.stockLine, QtCore.SIGNAL("currentIndexChanged(int)"), self.stockChanged)
        self.vbox.addWidget(self.stockLine)
        self.fetchBut=QtGui.QPushButton("Fetch")
        self.connect(self.fetchBut, QtCore.SIGNAL("clicked()"), self.fetchScr)
        self.fetchBut.setDisabled(True)
        self.vbox.addWidget(self.fetchBut)
        '''self.stList=QtGui.QListView()
        seaLabel=QtGui.QLabel("Search: ")
        self.filterLineEdit=QtGui.QLineEdit()
        if sys.version_info[0] == 3:
            self.filterLineEdit.setValidator(upValidator3())
        else:
            self.filterLineEdit.setValidator(upValidator2())
        tmpHbox=QtGui.QHBoxLayout()
        tmpHbox.addWidget(seaLabel)
        tmpHbox.addWidget(self.filterLineEdit)
        self.vbox.addLayout(tmpHbox)
        self.vbox.addWidget(self.stList)
        checkAll=QtGui.QPushButton("Check All")
        clearAll=QtGui.QPushButton("Clear All")
        self.vbox.addWidget(checkAll)
        self.vbox.addWidget(clearAll)
        self.connect(checkAll, QtCore.SIGNAL("clicked()"), self.check)
        self.connect(clearAll, QtCore.SIGNAL("clicked()"), self.clear)'''
        
        self.model = QtGui.QStandardItemModel()
        
        '''for i in sp100:
            item = QtGui.QStandardItem(i)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
            #self.butGroup.addButton(item)
            self.model.appendRow(item)

        self.connect(self.model, QtCore.SIGNAL("itemChanged(QStandardItem*)"),self.par.butCheck)
        proxy = QtGui.QSortFilterProxyModel()
        proxy.setSourceModel(self.model)
        self.stList.setModel(proxy)
        self.connect(filterLineEdit, QtCore.SIGNAL("textChanged(QString)"),proxy.setFilterFixedString)'''
        
        self.butGroupFunc=QtGui.QButtonGroup(self)
        self.butGroupFunc.setExclusive(False)
        self.checkBox=QtGui.QVBoxLayout()
        for name in ('1 day price change', '3 day price change', '5 day price change', '6 month price change', '12 month price change', 'Volatility 90 days', 'Price sales ratio', 'Price earnings ratio', 'Insider held shares', 'Price book ratio' ):
            but=QtGui.QCheckBox(name)
            self.butGroupFunc.addButton(but)
            self.checkBox.addWidget(but)
        self.butGroupFunc.connect(self.butGroupFunc,QtCore.SIGNAL("buttonClicked(int)"), self.par.butCheckFunc)
        funcName=QtGui.QLabel("Features")
        funcName.setStyleSheet(sheet)
        self.vbox.addWidget(funcName,0,QtCore.Qt.AlignCenter)
        self.vbox.addLayout(self.checkBox)
        self.setLayout(self.vbox)
        

class mainWin(QtGui.QMainWindow):

    def __init__(self):
        super(mainWin,self).__init__()
        self.initUI()

    def initUI(self):
        self.MW=mainWid(self)
        self.createMenus()
        self.setCentralWidget(self.MW)
        self.resize(640,480)
        self.show()

    def createMenus(self):
        openFi = QtGui.QAction('&Open Model',self)
        #quitAc.setShortcut('Ctrl+Q')
        openFi.triggered.connect(self.MW.openBox)

        saveFi = QtGui.QAction('&Save Model',self)
        saveFi.triggered.connect(self.MW.saveBox)

        quitAc = QtGui.QAction('&Quit',self)
        quitAc.setShortcut('Ctrl+Q')
        quitAc.triggered.connect(self.close)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFi)
        fileMenu.addAction(saveFi)
        fileMenu.addAction(quitAc)

def main():
    a=QtGui.QApplication(sys.argv)
    w=mainWin()
    w.setWindowTitle("simpred")
    sys.exit(a.exec_())

if __name__ == '__main__':
    main()
