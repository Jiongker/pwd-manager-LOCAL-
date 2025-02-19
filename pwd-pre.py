import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QTabWidget, QMessageBox
from PyQt6.QtGui import QIcon, QFontDatabase, QFont  # Add QFont import
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve

# 假设这些函数已经在别处定义
def save_encrypted_password(label, account, password, directory):
    pass

def load_encrypted_password(label, directory):
    return None, None

def cipher_suite():
    pass

def set_password():
    """
    设置密码的函数
    """
    label = label_entry.text()
    account = account_entry.text()
    password = password_entry.text()
    directory = directory_var.text()
    if not os.path.exists(directory):
        QMessageBox.critical(set_window, "错误", "指定的目录不存在，请检查！")
        return
    if label and account and password:
        save_encrypted_password(label, account, password, directory)
        QMessageBox.information(set_window, "提示", "密码设置成功！")
    else:
        QMessageBox.critical(set_window, "错误", "请输入有效的标签、账号和密码！")

def verify_password():
    """
    验证密码的函数
    """
    label = query_label_entry.text()
    directory = query_directory_var.text()
    if not os.path.exists(directory):
        QMessageBox.critical(query_window, "错误", "指定的目录不存在，请检查！")
        return
    account, encrypted_password = load_encrypted_password(label, directory)
    if encrypted_password:
        try:
            decrypted_password = cipher_suite().decrypt(encrypted_password.encode()).decode()
            QMessageBox.information(query_window, "验证结果", f"标签 {label} 对应的账号是: {account}，原始密码是: {decrypted_password}")
        except Exception:
            QMessageBox.critical(query_window, "错误", "解密过程中出现错误！")
    else:
        QMessageBox.critical(query_window, "错误", f"未找到标签 {label} 对应的密码，请先设置！")

def select_directory():
    """
    打开资源管理器选择存储目录
    """
    directory = QFileDialog.getExistingDirectory(set_window, "选择存储目录")
    if directory:
        directory_var.setText(directory)

def select_query_directory():
    """
    打开资源管理器选择查询密码的存储目录
    """
    directory = QFileDialog.getExistingDirectory(query_window, "选择查询目录")
    if directory:
        query_directory_var.setText(directory)

# 创建主窗口
app = QApplication(sys.argv)

# Load font
font_id = QFontDatabase.addApplicationFont("C:/Windows/Fonts/HarmonyOS_Sans_SC_Regular.ttf")
if font_id != -1:
    font_families = QFontDatabase.applicationFontFamilies(font_id)
    if font_families:
        font_family = font_families[0]
        app.setFont(QFont(font_family))

root = QWidget()
root.setWindowTitle("密码管理系统")
root.setWindowIcon(QIcon("D:/python/密码.ico"))  # 替换为实际的图标文件路径
root.resize(800, 600)  # 设置窗口大小

# 设置全局样式表
app.setStyleSheet("""
    QWidget {
        font-family: "HarmonyOS Sans SC", "Segoe UI", Arial, sans-serif;
        background-color: #f9f9f9; /* 主窗口背景颜色 */
        color: #333; /* 主窗口字体颜色 */
    }
    QTabWidget::pane {
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 10px;
        background-color: #fff; /* 标签页内容区域背景颜色 */
    }
    QTabBar::tab {
        background-color: #e0e0e0; /* 未选中标签背景颜色 */
        border: 1px solid #ccc;
        border-bottom: none;
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
        padding: 5px 10px;
        color: #333; /* 未选中标签字体颜色 */
    }
    QTabBar::tab:selected {
        background-color: #fff; /* 选中标签背景颜色 */
        color: #007BFF; /* 选中标签字体颜色 */
    }
    QPushButton {
        background-color: #007BFF;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 8px 15px;
    }
    QPushButton:hover {
        background-color: #0056b3;
    }
    QLineEdit {
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 5px;
        background-color: #fff; /* 输入框背景颜色 */
        color: #333; /* 输入框字体颜色 */
    }
    QLabel {
        margin-bottom: 5px;
        color: #333; /* 标签字体颜色 */
    }
    QMessageBox {
        background-color: #fff; /* 消息框背景颜色 */
        color: #333; /* 消息框字体颜色 */
    }
    QMessageBox QPushButton {
        background-color: #007BFF;
        color: white;
    }
    QMessageBox QPushButton:hover {
        background-color: #0056b3;
    }
""")

# 创建 Notebook 组件
notebook = QTabWidget(root)

# 设置密码界面
set_window = QWidget()
notebook.addTab(set_window, "设置密码")

# 创建选择目录按钮和输入框
directory_var = QLineEdit()
directory_button = QPushButton("选择存储目录", set_window)
directory_button.clicked.connect(select_directory)

set_layout = QVBoxLayout(set_window)
set_layout.setSpacing(20)  # 调整间距
set_layout.addWidget(directory_button)
set_layout.addWidget(directory_var)

# 创建标签和输入框
label_label = QLabel("请输入密码标签:")
label_entry = QLineEdit()
set_layout.addWidget(label_label)
set_layout.addWidget(label_entry)

# 创建账号和输入框
account_label = QLabel("请输入对应账号:")
account_entry = QLineEdit()
set_layout.addWidget(account_label)
set_layout.addWidget(account_entry)

password_label = QLabel("请输入密码:")
password_entry = QLineEdit()
password_entry.setEchoMode(QLineEdit.EchoMode.Password)
set_layout.addWidget(password_label)
set_layout.addWidget(password_entry)

# 创建设置密码按钮
set_button = QPushButton("设置密码", set_window)
set_button.clicked.connect(set_password)
set_layout.addWidget(set_button)

# 查询密码界面
query_window = QWidget()
notebook.addTab(query_window, "查询密码")

# 创建选择查询目录按钮和输入框
query_directory_var = QLineEdit()
query_directory_button = QPushButton("选择查询目录", query_window)
query_directory_button.clicked.connect(select_query_directory)

query_layout = QVBoxLayout(query_window)
query_layout.setSpacing(20)  # 调整间距
query_layout.addWidget(query_directory_button)
query_layout.addWidget(query_directory_var)

# 创建查询标签和输入框
query_label_label = QLabel("请输入要查询的密码标签:")
query_label_entry = QLineEdit()
query_layout.addWidget(query_label_label)
query_layout.addWidget(query_label_entry)

# 创建查询密码按钮
verify_button = QPushButton("查看密码", query_window)
verify_button.clicked.connect(verify_password)
query_layout.addWidget(verify_button)

# 显示 Notebook
main_layout = QVBoxLayout(root)
main_layout.addWidget(notebook)

# 添加标签切换动画
def fade_in_out():
    current_widget = notebook.widget(notebook.currentIndex())
    next_index = (notebook.currentIndex() + 1) % notebook.count()
    next_widget = notebook.widget(next_index)

    # 淡出当前页面
    fade_out_animation = QPropertyAnimation(current_widget, b"windowOpacity")
    fade_out_animation.setDuration(300)
    fade_out_animation.setStartValue(1.0)
    fade_out_animation.setEndValue(0.0)
    fade_out_animation.setEasingCurve(QEasingCurve.InOutQuad)

    # 淡入下一个页面
    fade_in_animation = QPropertyAnimation(next_widget, b"windowOpacity")
    fade_in_animation.setDuration(300)
    fade_in_animation.setStartValue(0.0)
    fade_in_animation.setEndValue(1.0)
    fade_in_animation

# 显示主窗口
root.show()

# 运行主循环
sys.exit(app.exec())
