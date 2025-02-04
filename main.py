import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTextEdit, QPushButton, QVBoxLayout, QWidget
try :
    from ui.main_window import Ui_MainWindow #导入ui
except ImportError:
    print("Ui_MainWindow 未导入，跳过相关操作。")
from PyQt5 import uic
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import Qt, QUrl,QObject,pyqtSignal
from PyQt5.QtMultimedia import QAudioInput, QAudioOutput, QAudioFormat,QAudioBuffer
from PySide6.QtMultimedia import QMediaDevices

import wave

import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class AudioRecorder(QObject):


    def __init__(self, parent=None, duration=5, fs=44100, channels=2, gain_db=12):
            super().__init__(parent)
            self.duration = duration
            self.fs = fs
            self.channels = channels
            self.gain_db = gain_db



        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #加载 ui代码 @@self.setupUi(self)@@
        uic.loadUi("main_window.ui", self)
        # 初始化控件
        self.init_ui()
        self.duration = 5
        self.fs = 44100
        self.channels = 2
        self.gain_db = 24       
        file_path = ""
        # 初始化媒体播放器
        
        #self.media_player = QMediaPlayer()
        self.recorder = AudioRecorder(parent=self, duration=1, fs=44100, channels=2, gain_db=12)

    def init_ui(self):
        # 创建按钮并连接信号槽
        self.load_button.clicked.connect(self.load_file)
        self.play_audio_button.clicked.connect(self.play_audio)
        self.record_audio_button.clicked.connect(self.record_audio)
        self.start_button.clicked.connect(self.start_recording)#录音
        #self.stop_button.clicked.connect(self.stop_recording)#录音
        # 显示初始状态
        self.text_edit.setPlainText("请选择一个文件...")
        

        


    def load_file(self):
        # 打开文件选择对话框
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "打开文件", "", "All Files (*)")

        print(f"file_path 路径。{file_path}")
            
        if file_path:
            try:
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # 显示文件内容
                self.text_edit.setPlainText(content)
            except Exception as e:
                self.text_edit.setPlainText(f"无法读取文件：{e}")
    def get_file_path():

    
        # 假设用户点击了加载文件按钮并选择了文件
        file_path = window.load_file()
        
        return file_path

    def play_audio(self):
        file_dialog = QFileDialog()
        self.file_path, _ = file_dialog.getOpenFileName(self, "打开文件", "", "All Files (*)")
        
        if self.file_path:
                self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.file_path)))
                self.media_player.play()
        else:
            print("请先选择一个文件")
    def record_audio(self):
        file_dialog = QFileDialog()
        self.file_path, _ = file_dialog.getOpenFileName(self, "打开文件", "", "All Files (*)")
        
        if self.file_path:
                self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.file_path)))
                self.media_player.play()
        else:
            print("请先选择一个文件")
           
    def start_recording(self):
        logging.debug("开始录音...")
        try :
            # 录制音频
            myrecording = sd.rec(int(self.duration * self.fs), samplerate=self.fs, channels=self.channels)

            # 等待录音结束
            sd.wait()

            print("录音完成!")

            # 进行增益处理
            gain_factor = 10 ** (self.gain_db / 20)
            increased_volume_recording = myrecording * gain_factor

            sd.play(increased_volume_recording, samplerate=44100)
            sd.wait() 
            # 保存处理后的音频到文件（可选）
            write('output_audio.wav', self.fs, increased_volume_recording)
            print("处理后的音频已保存到 'output_audio.wav'")
        except Exception as e:
            logging.error(f"录音过程中发生错误: {e}")         

        

            

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    window = MainWindow()
    
    window.show()
    # 检查音频设备
    devices = sd.query_devices()
    #logging.info(f"可用的音频设备: {devices}")
    
    sys.exit(app.exec_())

    
