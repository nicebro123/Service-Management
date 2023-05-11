import sys
import subprocess
import psutil
import signal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QVBoxLayout
from PyQt5.QtCore import QTimer


class ServiceManager(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle('一键启动服务管理器')
        self.setGeometry(100, 100, 300, 150)

        # 设置背景颜色
        self.setStyleSheet('background-color: #f2f2f2;')

        # 创建垂直布局管理器
        layout = QVBoxLayout()

        # 添加“启动服务”按钮
        start_button = QPushButton('启动服务', self)
        layout.addWidget(start_button)
        start_button.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            
            QPushButton:hover {
                background-color: #3e8e41;
            }
        ''')
        start_button.clicked.connect(self.start_service)

        # 添加“停止服务”按钮
        stop_button = QPushButton('停止服务', self)
        layout.addWidget(stop_button)
        stop_button.setStyleSheet('''
            QPushButton {
                background-color: #f44336;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            
            QPushButton:hover {
                background-color: #d32f2f;
            }
        ''')
        stop_button.clicked.connect(self.stop_service)

        # 添加“退出”按钮
        exit_button = QPushButton('退出', self)
        layout.addWidget(exit_button)
        exit_button.setStyleSheet('''
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            
            QPushButton:hover {
                background-color: #1976D2;
            }
        ''')
        exit_button.clicked.connect(self.confirm_exit)

        # 将布局管理器设置为主窗口的布局管理器
        self.setLayout(layout)

        # 创建一个空的进程列表
        self.processes = []

    def start_service(self):
        # 启动一个新进程并保存进程对象
        process = subprocess.Popen(['python', 'hello1.py'])
        self.processes.append(process)

    def stop_service(self):
        # 实现停止服务逻辑
        for process in self.processes:
            # 终止进程
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

        # 清空进程列表
        self.processes.clear()

        # 弹出提示框告知用户服务已经停止
        QMessageBox.information(self, '提示', '服务已经停止', QMessageBox.Ok)

    def confirm_exit(self):
        # 创建确认对话框，询问用户是否要退出
        reply = QMessageBox.question(self, '确认', '您确定要退出吗？',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # 实现退出逻辑
            for process in self.processes:
                try:
                    # 向进程发送 SIGTERM 信号
                    process.send_signal(signal.SIGTERM)
                    # 等待进程退出
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # 如果在超时时间内进程还没退出，则使用 Popen 对象终止进程
                    process.terminate()
                    process.wait(timeout=5)
                except ProcessLookupError:
                    pass

            # 延迟一段时间后退出应用程序
            QTimer.singleShot(1000, app.quit)


if __name__ == '__main__':
    # 创建 QApplication 实例和 ServiceManager 对象，并将 ServiceManager 对象显示出来
    app = QApplication(sys.argv)
    service_manager = ServiceManager()
    service_manager.show()

    # 进入 Qt 事件循环
    sys.exit(app.exec_())
