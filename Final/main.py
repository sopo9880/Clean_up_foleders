import os
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "정리_로그.txt")

# 로그 저장
def write_log(message):
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

# 정리 함수들
def organize_by_extension(folder_path):
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath):
            ext = os.path.splitext(filename)[-1][1:].lower() or "no_extension"
            ext_folder = os.path.join(folder_path, ext)
            os.makedirs(ext_folder, exist_ok=True)
            shutil.move(filepath, os.path.join(ext_folder, filename))
            write_log(f"{filename} → {ext}/")

def organize_by_date(folder_path):
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath):
            timestamp = os.path.getctime(filepath)
            date_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
            date_folder = os.path.join(folder_path, date_str)
            os.makedirs(date_folder, exist_ok=True)
            shutil.move(filepath, os.path.join(date_folder, filename))
            write_log(f"{filename} → {date_str}/")

def organize_by_size(folder_path):
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath):
            size = os.path.getsize(filepath)
            if size < 1 * 1024 * 1024:
                size_folder = "Small(<1MB)"
            elif size < 10 * 1024 * 1024:
                size_folder = "Medium(1-10MB)"
            else:
                size_folder = "Large(10MB+)"
            folder = os.path.join(folder_path, size_folder)
            os.makedirs(folder, exist_ok=True)
            shutil.move(filepath, os.path.join(folder, filename))
            write_log(f"{filename} → {size_folder}/")

# 기준 선택 및 실행
def organize():
    folder = filedialog.askdirectory(title="정리할 폴더를 선택하세요")
    if not folder:
        return
    option = sort_var.get()
    if option == "ext":
        organize_by_extension(folder)
    elif option == "date":
        organize_by_date(folder)
    elif option == "size":
        organize_by_size(folder)
    messagebox.showinfo("완료", "파일 정리가 완료되었습니다.")

# GUI
app = tk.Tk()
app.title("파일 정리 도우미")
app.geometry("350x230")
app.resizable(False, False)

label = tk.Label(app, text="정리 기준을 선택하세요", font=("맑은 고딕", 12))
label.pack(pady=15)

sort_var = tk.StringVar(value="ext")

radio1 = tk.Radiobutton(app, text="확장자 기준", variable=sort_var, value="ext")
radio2 = tk.Radiobutton(app, text="날짜 기준", variable=sort_var, value="date")
radio3 = tk.Radiobutton(app, text="파일 크기 기준", variable=sort_var, value="size")

radio1.pack(anchor="w", padx=30)
radio2.pack(anchor="w", padx=30)
radio3.pack(anchor="w", padx=30)

button = tk.Button(app, text="폴더 선택 및 정리", command=organize, bg="#2196F3", fg="white", height=2)
button.pack(pady=20)

app.mainloop()
