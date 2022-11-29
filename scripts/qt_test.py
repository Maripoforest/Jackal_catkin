
import sys

from PyQt5.QtWidgets import (QApplication, QWidget, QSlider, QLCDNumber, QVBoxLayout, QPushButton)
from PyQt5.QtCore import Qt

import rospy
import geometry_msgs.msg
import threading


drive_para = geometry_msgs.msg.Twist()
pub = rospy.Publisher('/cmd_vel', geometry_msgs.msg.Twist, queue_size=10)

def release():
    global drive_para  
    while not rospy.is_shutdown():
        pub.publish(drive_para)
        rospy.loginfo(drive_para)
    

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def out(self):
        global drive_para
        drive_para.linear.x = self.sld.value() / 100.0
        drive_para.angular.z = 0 - self.sld_2.value() / 100.0

        # release()
        
    def stop(self):
        global drive_para
        drive_para.linear.x = 0
        drive_para.angular.z = 0
        self.sld.setValue(0)
        self.sld_2.setValue(0)


    def initUI(self):
        
        lcd = QLCDNumber(self)
        lcd_2 = QLCDNumber(self)

        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setValue(0)
        self.sld.setMinimum(-200)
        self.sld.setMaximum(200)

        self.sld_2 = QSlider(Qt.Horizontal, self)
        self.sld_2.setValue(0)
        self.sld_2.setMinimum(-144)
        self.sld_2.setMaximum(144)

        vbox = QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(lcd_2)
        vbox.addWidget(self.sld)
        vbox.addWidget(self.sld_2)

        self.setLayout(vbox)
        self.sld.valueChanged.connect(lcd.display)
        self.sld.sliderReleased.connect(self.stop)
        self.sld.valueChanged.connect(self.out)
                
        self.sld_2.valueChanged.connect(self.out)
        self.sld_2.sliderReleased.connect(self.stop)
        self.sld_2.valueChanged.connect(lcd_2.display)

        button1 = QPushButton(self)
        button1.setText('Stop')
        button1.move(64, 32)
        button1.clicked.connect(self.stop)
        
        self.setGeometry(500, 500, 500, 400)
        self.setWindowTitle('Jackal Vel CMD') 
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    rospy.init_node('driver')
    t = threading.Thread(target=release)
    t.start()
    app.exec_()
    t.join()
    sys.exit()