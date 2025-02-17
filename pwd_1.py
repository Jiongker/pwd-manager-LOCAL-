import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from cryptography.fernet import Fernet
import json
import os

# 生成加密密钥
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# 初始默认的存储文件名
password_file_name = 'encrypted_passwords.json'

def save_encrypted_password(label, account, password, directory):
    """
    加密并保存密码、账号和标签到指定目录的文件
    :param label: 密码对应的标签
    :param account: 密码对应的账号
    :param password: 明文密码
    :param directory: 存储文件的目录
    """
    encrypted_password = cipher_suite.encrypt(password.encode())
    file_path = os.path.join(directory, password_file_name)
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    data[label] = {
        'account': account,
        'password': encrypted_password.decode()
    }
    with open(file_path, 'w') as f:
        json.dump(data, f)

def load_encrypted_password(label, directory):
    """
    从指定目录的文件中加载指定标签的加密后的密码
    :param label: 密码对应的标签
    :param directory: 存储文件的目录
    :return: 加密后的密码和账号
    """
    file_path = os.path.join(directory, password_file_name)
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        entry = data.get(label)
        if entry:
            return entry.get('account'), entry.get('password')
        return None, None
    except FileNotFoundError:
        return None, None

def set_password():
    """
    设置密码的函数
    """
    label = label_entry.get()
    account = account_entry.get()
    password = password_entry.get()
    directory = directory_var.get()
    if not os.path.exists(directory):
        messagebox.showerror("错误", "指定的目录不存在，请检查！")
        return
    if label and account and password:
        save_encrypted_password(label, account, password, directory)
        messagebox.showinfo("提示", "密码设置成功！")
    else:
        messagebox.showerror("错误", "请输入有效的标签、账号和密码！")

def verify_password():
    """
    验证密码的函数
    """
    label = query_label_entry.get()
    directory = query_directory_var.get()
    if not os.path.exists(directory):
        messagebox.showerror("错误", "指定的目录不存在，请检查！")
        return
    account, encrypted_password = load_encrypted_password(label, directory)
    if encrypted_password:
        try:
            decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
            messagebox.showinfo("验证结果", f"标签 {label} 对应的账号是: {account}，原始密码是: {decrypted_password}")
        except Exception:
            messagebox.showerror("错误", "解密过程中出现错误！")
    else:
        messagebox.showerror("错误", f"未找到标签 {label} 对应的密码，请先设置！")

def select_directory():
    """
    打开资源管理器选择存储目录
    """
    directory = filedialog.askdirectory()
    if directory:
        directory_var.set(directory)

def select_query_directory():
    """
    打开资源管理器选择查询密码的存储目录
    """
    directory = filedialog.askdirectory()
    if directory:
        query_directory_var.set(directory)

# 创建主窗口
root = tk.Tk()
root.title("密码管理系统")

# 创建 Notebook 组件
notebook = ttk.Notebook(root)

# 设置密码界面
set_frame = ttk.Frame(notebook)
notebook.add(set_frame, text="设置密码")

# 创建选择目录按钮和输入框
directory_var = tk.StringVar()
directory_button = tk.Button(set_frame, text="选择存储目录", command=select_directory)
directory_button.pack(pady=10)

directory_label = tk.Label(set_frame, textvariable=directory_var)
directory_label.pack(pady=5)

# 创建标签和输入框
label_label = tk.Label(set_frame, text="请输入密码标签:")
label_label.pack(pady=10)

label_entry = tk.Entry(set_frame)
label_entry.pack(pady=5)

# 创建账号和输入框
account_label = tk.Label(set_frame, text="请输入对应账号:")
account_label.pack(pady=10)

account_entry = tk.Entry(set_frame)
account_entry.pack(pady=5)

password_label = tk.Label(set_frame, text="请输入密码:")
password_label.pack(pady=10)

password_entry = tk.Entry(set_frame, show="*")
password_entry.pack(pady=5)

# 创建设置密码按钮
set_button = tk.Button(set_frame, text="设置密码", command=set_password)
set_button.pack(pady=10)

# 查询密码界面
query_frame = ttk.Frame(notebook)
notebook.add(query_frame, text="查询密码")

# 创建选择查询目录按钮和输入框
query_directory_var = tk.StringVar()
query_directory_button = tk.Button(query_frame, text="选择查询目录", command=select_query_directory)
query_directory_button.pack(pady=10)

query_directory_label = tk.Label(query_frame, textvariable=query_directory_var)
query_directory_label.pack(pady=5)

# 创建查询标签和输入框
query_label_label = tk.Label(query_frame, text="请输入要查询的密码标签:")
query_label_label.pack(pady=10)

query_label_entry = tk.Entry(query_frame)
query_label_entry.pack(pady=5)

# 创建查询密码按钮
verify_button = tk.Button(query_frame, text="查看密码", command=verify_password)
verify_button.pack(pady=10)

# 显示 Notebook
notebook.pack(expand=True, fill="both")

# 运行主循环
root.mainloop()
