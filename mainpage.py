import time
import sys
import os
import pandas as pd
from qtpy import QtWidgets, QtGui
from backend import *
from Main.mainwindow import Ui_MainWindow
import pyperclip
import glob

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.mainwin = Ui_MainWindow()
        self.mainwin.setupUi(self)
        self.setWindowTitle("Scrapping Tool")
        self.setWindowIcon(QtGui.QIcon('web-crawler.png'))
        self.mainwin.comboBox_2.clear()
        self.add_databases_names()
        self.add_search_method()
        
        self.mainwin.pushButton.clicked.connect(self.search)
        self.mainwin.pushButton_3.clicked.connect(self.export)
        self.mainwin.pushButton_4.clicked.connect(self.open_file)
        self.mainwin.pushButton_5.clicked.connect(self.copy)
        self.mainwin.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.mainwin.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.showMaximized()
                
    def add_databases_names(self):
        cwd = os.getcwd()
        db_names = glob.glob("{0}/*.db".format(cwd))
        cnt = 0
        for name in db_names:
            name = name.split('\\')
            name = name[-1]
            name = name.replace('.db','')
            db_names[cnt] = name
            cnt += 1
        del cnt
        self.mainwin.comboBox_2.addItems(db_names) 
    def add_search_method(self):
        methods = ['id','email','gender']
        self.mainwin.comboBox.addItems(methods)
    def open_file(self):
        try:
            f = open('last_path.txt','r')
            path2 = f.readline()
            path, _ = QtWidgets.QFileDialog.getOpenFileNames(self,'Open File',path2,'CSV(*.csv)'+'\n'+'TXT(*.txt)'+'\n'+'ALL FILES(*.*)')
        except Exception as e:
            path2 = os.path.join (os.path.expanduser ("~"), "desktop")
            path, _ = QtWidgets.QFileDialog.getOpenFileNames(self,'Open File',path2,'CSV(*.csv)'+'\n'+'TXT(*.txt)'+'\n'+'ALL FILES(*.*)')
        try:
            f = open('last_path.txt','w')
            f.write(path)
        except :
            pass
        if len(path) == 1 :
            dialog = QtWidgets.QInputDialog(self)
            dialog.setGeometry(750,475,350,275)
            dialog.setInputMode(QtWidgets.QInputDialog.TextInput)
            dialog.setWindowTitle('Get Indexes Window')
            dialog.setLabelText('Enter Indexes: ')
            lineEdit = dialog.findChild(QtWidgets.QLineEdit)
            lineEdit.setPlaceholderText('ex: 0,1,2')
            if dialog.exec_():
                indexs = dialog.textValue()
            
            dialog2 = QtWidgets.QInputDialog(self)
            dialog2.setGeometry(750,475,350,275)
            dialog2.setInputMode(QtWidgets.QInputDialog.TextInput)
            dialog2.setWindowTitle('Get Indexes Names Window')
            dialog2.setLabelText('Enter Indexes Names: ')
            lineEdit2 = dialog2.findChild(QtWidgets.QLineEdit)
            lineEdit2.setPlaceholderText('ex: id,phone,name')
            if dialog2.exec_():
                indexes_names = dialog2.textValue()
            indexes_names= indexes_names.split(',')
            indexs= indexs.split(',')
            for i in range(len(indexs)):
                indexs[i] = int(indexs[i])
            try: 
                db_name = path[0].split('/')
                db_name = db_name[-1]
                if db_name.__contains__('.txt'):
                    db_name = db_name.replace('.txt','')
                else:
                    db_name = db_name.replace('.csv','')        
                conn = sqlite3.connect('{0}.db'.format(db_name))
                for chunk in pd.read_csv(path[0],chunksize=20000,low_memory=False,warn_bad_lines=False, error_bad_lines=False,header=None):
                    chunk = chunk[indexs]
                    chunk = chunk.rename(columns=dict(zip(chunk.columns,indexes_names)))
                    print(chunk.columns)
                    chunk.drop_duplicates(subset=indexes_names)
                    chunk.to_sql('facebookusers',conn,if_exists='append',index=False)
                conn.close()
                QtWidgets.QMessageBox.information(self,'information','finished')                                 
            except Exception as e:
                print(e)
                QtWidgets.QMessageBox.warning(self,'warning','error acoured please check indexs and indexs names fields') 
        elif len(path) > 1:
            for p in path:
                dialog = QtWidgets.QInputDialog(self)
                dialog.setGeometry(750,475,350,275)
                dialog.setInputMode(QtWidgets.QInputDialog.TextInput)
                dialog.setWindowTitle('Get Indexes Window')
                dialog.setLabelText('Enter Indexes: ')
                lineEdit = dialog.findChild(QtWidgets.QLineEdit)
                lineEdit.setPlaceholderText('ex: 0,1,2')
                if dialog.exec_():
                    indexs = dialog.textValue()
                dialog2 = QtWidgets.QInputDialog(self)
                dialog2.setGeometry(750,475,350,275)
                dialog2.setInputMode(QtWidgets.QInputDialog.TextInput)
                dialog2.setWindowTitle('Get Indexes Names Window')
                dialog2.setLabelText('Enter Indexes Names: ')
                lineEdit2 = dialog2.findChild(QtWidgets.QLineEdit)
                lineEdit2.setPlaceholderText('ex: id,phone,name')
                if dialog2.exec_():
                    indexes_names = dialog2.textValue()
                indexes_names= indexes_names.split(',')
                indexs= indexs.split(',')
                for i in range(len(indexs)):
                    indexs[i] = int(indexs[i])
                try: 
                    db_name = p.split('/')
                    db_name = db_name[-1]
                    if db_name.__contains__('.txt'):
                        db_name = db_name.replace('.txt','')
                    else:
                        db_name = db_name.replace('.csv','')        
                    conn = sqlite3.connect('{0}.db'.format(db_name))
                    for chunk in pd.read_csv(p,chunksize=20000,low_memory=False,warn_bad_lines=False, error_bad_lines=False,header=None):
                        chunk = chunk[indexs]
                        chunk = chunk.rename(columns=dict(zip(chunk.columns,indexes_names)))
                        chunk.drop_duplicates(subset=indexes_names)
                        chunk.to_sql('facebookusers',conn,if_exists='append',index=False)
                    conn.close()                 
                except Exception as e:
                    print(e)
                    QtWidgets.QMessageBox.warning(self,'warning','error acoured please check indexs and indexs names fields [{0}]'.format(db_name))
            QtWidgets.QMessageBox.information(self,'information','finished') 
            
        cwd = os.getcwd()
        db_names = glob.glob("{0}/*.db".format(cwd))
        cnt = 0
        for name in db_names:
            name = name.split('\\')
            name = name[-1]
            name = name.replace('.db','')
            db_names[cnt] = name
            cnt += 1
        del cnt
        self.mainwin.comboBox_2.clear()
        self.mainwin.comboBox_2.addItems(db_names)                          
    def search(self):
        try:
            database = self.mainwin.comboBox_2.currentText()
            method = self.mainwin.comboBox.currentText()
            value = self.mainwin.textEdit.toPlainText()
            value = value.split('\n')
            
            i = 0
            for x in range(0,len(value)):
                if value[x] == '':
                    i += 1
            for x in range(0,i):
                value.remove('')                     

            conn = sqlite3.connect('{0}.db'.format(database))
            cur = conn.cursor()
            get_column_names=cur.execute("select * from facebookusers limit 1")
            col_name=[i[0] for i in get_column_names.description]
            self.mainwin.tableWidget.setRowCount(0)
            self.mainwin.tableWidget.setColumnCount(0)
            for i in range(len(col_name)):
                self.mainwin.tableWidget.insertColumn(i)
            for i in range(len(col_name)):
                col_name[i] = col_name[i].capitalize()
            self.mainwin.tableWidget.setHorizontalHeaderLabels(col_name)
            flag = True
            droped_ids = []
            for i in value :
                cur.execute('SELECT * FROM facebookusers WHERE {0} = ? GROUP BY {1}'.format(method,method),(i,))
                try:
                    row = cur.fetchall()
                    if len(row) == 0 :
                        droped_ids.append(i)
                    else:
                        for d in row:
                            row_count = self.mainwin.tableWidget.rowCount()
                            self.mainwin.tableWidget.insertRow(row_count)
                            self.mainwin.tableWidget.setRowHeight(row_count,50)
                            for r in range(len(col_name)):     
                                self.mainwin.tableWidget.setItem(row_count,r, QtWidgets.QTableWidgetItem(str(d[r])))
                            self.mainwin.tableWidget.horizontalHeader().setStretchLastSection(True)
                            self.mainwin.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)             
                except :
                    QtWidgets.QMessageBox.warning(self,'error','error')
            if len(droped_ids) > 0 :
                QtWidgets.QMessageBox.warning(self,'error','couldn\'t find these IDs {0}'.format(droped_ids))
            conn.close()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self,'warning','please select method and database')
            print(str(e)) 
            flag = False 
        if flag:
            QtWidgets.QMessageBox.information(self,'information','Search finished successfully')
             
    def export(self):
        database_name = self.mainwin.comboBox_2.currentText()
        row_count = self.mainwin.tableWidget.rowCount()
        column_count = self.mainwin.tableWidget.columnCount()
        if row_count == 0:
            QtWidgets.QMessageBox.warning(self,'warning','no data to be exported in the table')
        else:
            full_data = []
            for i in range(row_count):    
                    row_data = []
                    for c in range(column_count):
                        value = self.mainwin.tableWidget.item(i,c).text()
                        row_data.append(value)
                    full_data.append(row_data)
            
            df = pd.DataFrame(full_data)
            path = os.path.join(os.path.expanduser('~'),'desktop')
            flag = True
            conn = sqlite3.connect('{0}.db'.format(database_name))
            cur = conn.cursor()
            get_column_names=cur.execute("select * from facebookusers limit 1")
            col_name=[i[0] for i in get_column_names.description]
            conn.close()
            try:
                writer = pd.ExcelWriter(path+'\\{0}.xlsx'.format(database_name), engine='openpyxl',if_sheet_exists='new',mode='a')
                df.to_excel(writer,index=False,header=col_name)
                writer.save()         
            except Exception as e : 
                try:
                    writer = pd.ExcelWriter(path+'\\{0}.xlsx'.format(database_name), engine='xlsxwriter',mode='w')
                    df.to_excel(writer,index=False,header=col_name)
                    writer.save()
                except Exception as e:
                    print(e)
                    QtWidgets.QMessageBox.warning(self,'error','error accoured cause u open the excel file close it then try again')
                    flag = False
            if flag:
                QtWidgets.QMessageBox.information(self,'informatio','data exported succssefully to desktop')             
    def copy(self):
        text = ''
        for x in self.mainwin.tableWidget.selectedIndexes():
            row = x.row()
            column = x.column()
            value = self.mainwin.tableWidget.item(row,column).text()
            text += (value+'\n')
        pyperclip.copy(text)

if __name__ == '__main__':
    App = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    App.setStyle('Fusion')
    sys.exit(App.exec_())