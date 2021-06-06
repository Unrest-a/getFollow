from PyQt5.QtWidgets import*
from getFollowings_python import Ui_MainWindow
import sqlite3
import tweepy
from PyQt5.QtCore import QTimer
#you need to be twitter developer for use this program
consumer_key = "***"
consumer_secret = "***"
access_token = "***"
access_token_secret = "***"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


class getFollowings(QMainWindow):

    def __init__(self):

        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        database2 = sqlite3.connect("gettingUsers.sqlite")
        rasgele = database2.cursor()
        rasgele.execute("SELECT name FROM sqlite_master")
        item = rasgele.fetchall()
        i = 0
        for i in item:

            self.ui.comboBox_users.addItems(i)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.Check)
        self.timer.setInterval(900000)

        self.ui.lineEdit_getName.returnPressed.connect(self.getNameF)
        self.ui.pushButton_save.clicked.connect(self.take_friends)
        self.ui.pushButton_delete.clicked.connect(self.delete_user)
        self.ui.pushButton_update.clicked['bool'].connect(self.Clicked)


    def getNameF(self):
        try:
            self.user = self.ui.lineEdit_getName.text()
            self.take_friends()
            self.ui.lineEdit_getName.clear()
        except sqlite3.OperationalError:
            QMessageBox.about(self,"Error","İsim Yanlış Girildi.")
        except tweepy.error.RateLimitError:
            QMessageBox.about(self,"Error","Çok Fazla Deneme Yaptınız.")


    def take_friends(self):
        try:
            self.ui.comboBox_users.addItem(self.ui.lineEdit_getName.text())
            self.database = sqlite3.connect("gettingUsers.sqlite")
            self.followings = self.database.cursor()
            self.followings.execute(f"CREATE TABLE IF NOT EXISTS {str(self.ui.lineEdit_getName.text())}('no','username','name')")
            takipciler = api.friends(id=str(self.ui.lineEdit_getName.text()), count=220)
            i = 1
            for takipci in takipciler:
                veriler = (i, takipci.screen_name, takipci.name)
                self.followings.execute(f"INSERT INTO {str(self.ui.lineEdit_getName.text())} VALUES(?, ?, ?)", veriler)
                i += 1

            self.database.commit()
            self.database.close()
        except sqlite3.OperationalError:
            QMessageBox.about(self,"Syntax","İsim Yanlış Girildi.")
        except tweepy.error.RateLimitError:
            QMessageBox.about(self,"Error","Çok Fazla Deneme Yaptınız.")


    def delete_user(self):
        try:


            selected_text = self.ui.comboBox_users.currentText()
            self.ui.comboBox_users.removeItem(self.ui.comboBox_users.currentIndex())
            self.database = sqlite3.connect("gettingUsers.sqlite")
            self.followings = self.database.cursor()
            self.followings.execute(f"DROP TABLE {selected_text}")
            self.database.commit()
            self.database.close()


        except sqlite3.OperationalError:
            QMessageBox.about(self,"Error","Seçili eleman bellekte bulunamıyor.(Muhtemelen isim yanlış girilmiştir.)")


    def Clicked(self, circumstance):
        self.durum = circumstance
        try:

            if circumstance:

                self.ui.pushButton_update.setText("Stop")
                self.ui.pushButton_update.setStyleSheet("background-color: rgb(0, 211, 0);")
                self.timer.start()

            else:

                self.timer.stop()
                self.ui.pushButton_update.setStyleSheet("background-color: rgb(255, 0, 0)")
                self.ui.pushButton_update.setText("Start")


        except sqlite3.OperationalError:
            QMessageBox.about(self, "Error", "Takipci Seçmemiş Olabilirsiniz.")
        except tweepy.error.RateLimitError:
            QMessageBox.about(self,"Error","Çok Fazla Deneme Yaptınız.")


    def Check(self):
        try:

            selected_text_comp = self.ui.comboBox_users.currentText()

            self.database_compare = sqlite3.connect(':memory:')
            self.imlec = self.database_compare.cursor()
            self.imlec.execute(f"CREATE TABLE IF NOT EXISTS {str(selected_text_comp)}('no','username','name')")
            takipciler1 = api.friends(id=str(selected_text_comp), count=220)
            i = 1
            for takipci in takipciler1:
                veriler1 = (i, takipci.screen_name, takipci.name)
                self.imlec.execute(f"INSERT INTO {str(selected_text_comp)} VALUES(?, ?, ?)", veriler1)
                i += 1
            self.imlec.execute(f"SELECT * FROM {str(selected_text_comp)}")
            data_1 = self.imlec.fetchmany(5)
            new_user = self.imlec.fetchone()
            self.database_compare.commit()

            self.database = sqlite3.connect("gettingUsers.sqlite")
            self.followings = self.database.cursor()
            self.followings.execute(f"SELECT * FROM {str(selected_text_comp)}")
            data_2 = self.followings.fetchmany(5)
            self.database.commit()

            if data_1 != data_2:
                QMessageBox.warning(self, "Güncelleme", f"Yeni Takipci: {str(data_1[0][2])}")
                self.timer.stop()

        except sqlite3.OperationalError:
            QMessageBox.about(self, "Error", "Takipci Seçmemiş Olabilirsiniz.")

        except tweepy.error.RateLimitError:
            QMessageBox.about(self, "Error", "Çok Fazla Deneme Yaptınız.")


deneme1 = QApplication([])
pencere = getFollowings()
pencere.show()
deneme1.exec_()