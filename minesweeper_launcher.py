#!/usr/bin/env python3
"""
扫雷游戏启动器
可以选择启动命令行版本或GUI版本
"""

import tkinter as tk
from tkinter import messagebox, font
import subprocess
import sys
import os

class MinesweeperLauncher:
    def __init__(self, master):
        self.master = master
        self.setup_ui()

    def setup_ui(self):
        """设置启动器界面"""
        self.master.title("扫雷游戏 - 版本选择")
        self.master.resizable(False, False)
        self.master.configure(bg='#f0f0f0')

        # 设置窗口位置在屏幕中央
        self.master.update_idletasks()
        width = 500
        height = 400
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry(f'{width}x{height}+{x}+{y}')

        # 主框架
        main_frame = tk.Frame(self.master, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 标题
        title_label = tk.Label(
            main_frame,
            text="🎮 扫雷游戏 🎮",
            font=('Arial', 24, 'bold'),
            bg='#f0f0f0',
            fg='#333333'
        )
        title_label.pack(pady=(0, 30))

        # 副标题
        subtitle_label = tk.Label(
            main_frame,
            text="选择你喜欢的游戏版本",
            font=('Arial', 14),
            bg='#f0f0f0',
            fg='#666666'
        )
        subtitle_label.pack(pady=(0, 40))

        # 按钮框架
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(expand=True)

        # GUI版本按钮
        gui_btn = tk.Button(
            button_frame,
            text="🖥️  GUI版本\n图形化界面，鼠标操作\n推荐新手使用",
            font=('Arial', 12),
            bg='#4CAF50',
            fg='white',
            width=25,
            height=6,
            relief=tk.RAISED,
            bd=3,
            command=self.launch_gui,
            activebackground='#45a049'
        )
        gui_btn.pack(pady=10)

        # 命令行版本按钮
        cli_btn = tk.Button(
            button_frame,
            text="💻  命令行版本\n终端界面，键盘输入\n适合命令行爱好者",
            font=('Arial', 12),
            bg='#2196F3',
            fg='white',
            width=25,
            height=6,
            relief=tk.RAISED,
            bd=3,
            command=self.launch_cli,
            activebackground='#0976d2'
        )
        cli_btn.pack(pady=10)

        # 说明文字
        info_frame = tk.Frame(main_frame, bg='#f0f0f0')
        info_frame.pack(pady=20)

        info_text = """版本说明：
• GUI版本：点击左键揭开格子，右键标记地雷
• 命令行版本：输入坐标进行操作，支持标记功能"""

        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=('Arial', 10),
            bg='#f0f0f0',
            fg='#888888',
            justify=tk.LEFT
        )
        info_label.pack()

    def launch_gui(self):
        """启动GUI版本"""
        try:
            self.master.withdraw()  # 隐藏启动器
            subprocess.Popen([sys.executable, "minesweeper_gui.py"])
            self.master.after(500, self.master.quit)  # 延迟关闭启动器
        except Exception as e:
            messagebox.showerror("错误", f"无法启动GUI版本：{e}")

    def launch_cli(self):
        """启动命令行版本"""
        try:
            self.master.withdraw()  # 隐藏启动器
            # 在新的终端窗口中运行
            if sys.platform == "win32":
                subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k',
                                f'python minesweeper.py'], shell=True)
            elif sys.platform == "darwin":  # macOS
                subprocess.Popen(['osascript', '-e',
                               f'tell app "Terminal" to do script "python3 minesweeper.py"'])
            else:  # Linux
                subprocess.Popen(['gnome-terminal', '--', 'python3', 'minesweeper.py'],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.master.after(500, self.master.quit)
        except Exception as e:
            # 如果在新终端中失败，在当前终端中运行
            try:
                self.master.withdraw()
                subprocess.run([sys.executable, "minesweeper.py"])
                self.master.quit()
            except Exception as e2:
                messagebox.showerror("错误", f"无法启动命令行版本：{e2}")

def main():
    """主函数"""
    root = tk.Tk()
    launcher = MinesweeperLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main()