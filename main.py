from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QMainWindow
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
from os import path
import sys
from pytube import YouTube,Playlist

From_class, _ = loadUiType(path.join(path.dirname(__file__), "untitled.ui"))

class Mainapp(QMainWindow, From_class):
    def __init__(self, parent=None):
        super(Mainapp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.hundel_ui()
        self.hundel_button()
    def hundel_ui(self):
        self.setWindowTitle('Youtube Video Downloader')
        self.setFixedSize(700,556)
    def hundel_button(self):
        self.pushButton_2.clicked.connect(self.hundel_browser)
        self.pushButton_3.clicked.connect(self.download_video)
        self.pushButton_4.clicked.connect(self.download_playlist)
        self.pushButton.clicked.connect(self.hundel_browser)
    def on_progress(self, stream, chunk, bytes_remaining):
        previousprogress = 0
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining 
        liveprogress = (int)(bytes_downloaded / total_size * 100)
        if liveprogress > previousprogress:
            previousprogress = liveprogress
            self.progressBar.setValue(liveprogress)
            QApplication.processEvents()#hundell the affichage during the download
    def on_progress2(self, stream, chunk, bytes_remaining):
        previousprogress = 0
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining 
        liveprogress = (int)(bytes_downloaded / total_size * 100)
        if liveprogress > previousprogress:
            previousprogress = liveprogress
            self.progressBar_2.setValue(liveprogress)
            QApplication.processEvents()
    def hundel_browser(self,n=2):
        location = str(QFileDialog.getExistingDirectory(self, 'Select Folder'))
        self.lineEdit_2.setText(location)
        self.lineEdit_4.setText(location)
    def download_video(self):
        url = self.lineEdit.text()
        locate = self.lineEdit_2.text()
        quality = self.comboBox.currentText()
        video = YouTube(url,on_progress_callback=self.on_progress)
        if quality == "audio":
            try:
                video.streams.filter(only_audio=True).first().download(output_path=locate)
                QMessageBox.information(self, "Download Complet", "The Download Finished")
            except:
                QMessageBox.warning(self , "The Download Faile", "Download error enter the url again")
                return 
        else:
            try:
                video.streams.filter(res=quality,progressive=True).first().download(output_path=locate)
                QMessageBox.information(self , "Download Complet", "The Download Finished")
            except:
                QMessageBox.warning(self , "The Download Faile", "Download error enter the url again")
                return 
        self.progressBar.setValue(0)
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
    def download_playlist(self):
        url = self.lineEdit_3.text()
        locate = self.lineEdit_4.text()
        quality = self.comboBox_2.currentText()
        playlist = Playlist(url)
        n = 0
        self.lcdNumber_2.display(playlist.__len__())
        if quality == "audio":
            try:
                for video in playlist.videos:
                    video.register_on_progress_callback(self.on_progress2)
                    video.streams.filter(only_audio=True).first().download(output_path=locate)
                    n += 1 
                    self.progressBar_2.setValue(0)
                    self.lcdNumber.display(n)
                QMessageBox.information(self, "Download Complet", "The Download Finished")
            except:
                QMessageBox.warning(self , "The Download Faile", "Download error enter the url again")
                return
        else:    
            try:
                for video in playlist.videos:
                    video.register_on_progress_callback(self.on_progress2)
                    video.streams.filter(res=quality, progressive=True).first().download(output_path=locate)
                    n += 1 
                    self.progressBar_2.setValue(0)
                    self.lcdNumber.display(n)
                QMessageBox.information(self, "Download Complet", "The Download Finished")
            except:
                QMessageBox.warning(self , "The Download Faile", "Download error enter the url again")
                return
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")
        self.lcdNumber.display(0)
        self.lcdNumber_2.display(0)

def main():
    app = QApplication(sys.argv)
    window = Mainapp()
    window.show() #show the window
    app.exec_()  # infinite loop

if __name__ == '__main__':
    main()