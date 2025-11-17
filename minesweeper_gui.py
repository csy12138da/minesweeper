#!/usr/bin/env python3
"""
扫雷游戏 - GUI版本
使用tkinter实现的图形化扫雷游戏
"""

import tkinter as tk
from tkinter import messagebox, font
import random
import time
from typing import List, Tuple, Optional
from enum import Enum

class GameState(Enum):
    """游戏状态枚举"""
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"

class MinesweeperGUI:
    def __init__(self, master, rows=10, cols=10, mines=10):
        """
        初始化GUI扫雷游戏

        Args:
            master: tkinter主窗口
            rows: 行数
            cols: 列数
            mines: 地雷数量
        """
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines

        # 游戏状态
        self.game_state = GameState.PLAYING
        self.first_click = True
        self.start_time = None
        self.elapsed_time = 0

        # 游戏数据
        self.board: List[List[int]] = []  # -1表示地雷, 0-8表示周围地雷数
        self.revealed: List[List[bool]] = []  # 是否已揭开
        self.flagged: List[List[bool]] = []  # 是否已标记
        self.cells_to_reveal = rows * cols - mines  # 需要揭开的格子数
        self.flag_count = 0  # 已标记的格子数

        # 颜色配置
        self.colors = {
            'default': '#c0c0c0',
            'revealed': '#ffffff',
            'mine': '#ff0000',
            'flag': '#0000ff',
            'text': ['#000080', '#008000', '#ff0000', '#000080', '#800000',
                    '#008080', '#000000', '#808080', '#000000'],
            'hover': '#d0d0d0'
        }

        self.setup_ui()
        self.new_game()

    def setup_ui(self):
        """设置用户界面"""
        self.master.title("扫雷游戏")
        self.master.resizable(False, False)

        # 设置窗口图标和样式
        try:
            self.master.iconname("扫雷")
        except:
            pass

        # 创建主框架
        main_frame = tk.Frame(self.master, bg='#c0c0c0')
        main_frame.pack(padx=10, pady=10)

        # 创建顶部控制面板
        self.create_control_panel(main_frame)

        # 创建游戏面板
        self.create_game_panel(main_frame)

    def create_control_panel(self, parent):
        """创建顶部控制面板"""
        control_frame = tk.Frame(parent, bg='#c0c0c0')
        control_frame.pack(fill=tk.X, pady=(0, 10))

        # 左侧：地雷计数器
        self.mine_counter_var = tk.StringVar()
        self.mine_counter = tk.Label(
            control_frame,
            textvariable=self.mine_counter_var,
            font=('Digital', 16, 'bold'),
            bg='#000000',
            fg='#ff0000',
            width=6,
            relief=tk.SUNKEN,
            anchor='e'
        )
        self.mine_counter.pack(side=tk.LEFT, padx=5)

        # 中间：新游戏按钮（笑脸）
        self.new_game_btn = tk.Button(
            control_frame,
            text='😊',
            font=('Arial', 20),
            width=3,
            height=1,
            command=self.new_game,
            relief=tk.RAISED,
            bd=3
        )
        self.new_game_btn.pack(side=tk.LEFT, padx=20)

        # 右侧：计时器
        self.timer_var = tk.StringVar()
        self.timer = tk.Label(
            control_frame,
            textvariable=self.timer_var,
            font=('Digital', 16, 'bold'),
            bg='#000000',
            fg='#ff0000',
            width=6,
            relief=tk.SUNKEN,
            anchor='e'
        )
        self.timer.pack(side=tk.LEFT, padx=5)

        # 难度选择按钮
        difficulty_frame = tk.Frame(control_frame, bg='#c0c0c0')
        difficulty_frame.pack(side=tk.RIGHT, padx=10)

        tk.Label(difficulty_frame, text="难度:", bg='#c0c0c0').pack(side=tk.LEFT)

        difficulties = [
            ("简单", 8, 8, 10),
            ("中等", 16, 16, 40),
            ("困难", 16, 30, 99)
        ]

        for name, rows, cols, mines in difficulties:
            btn = tk.Button(
                difficulty_frame,
                text=name,
                width=6,
                command=lambda r=rows, c=cols, m=mines: self.change_difficulty(r, c, m)
            )
            btn.pack(side=tk.LEFT, padx=2)

    def create_game_panel(self, parent):
        """创建游戏面板"""
        self.game_frame = tk.Frame(parent, bg='#808080', relief=tk.SUNKEN, bd=3)
        self.game_frame.pack()

        self.buttons = []
        for i in range(self.rows):
            row_buttons = []
            for j in range(self.cols):
                btn = tk.Button(
                    self.game_frame,
                    width=2,
                    height=1,
                    font=('Arial', 10, 'bold'),
                    relief=tk.RAISED,
                    bd=2,
                    bg=self.colors['default'],
                    command=lambda r=i, c=j: self.on_left_click(r, c),
                    activebackground='#e0e0e0'
                )

                # 绑定右键事件
                btn.bind('<Button-3>', lambda e, r=i, c=j: self.on_right_click(r, c))
                btn.bind('<Enter>', lambda e, b=btn: b.config(bg=self.colors['hover']))
                btn.bind('<Leave>', lambda e, b=btn: b.config(bg=self.colors['default']))

                btn.grid(row=i, column=j, padx=1, pady=1)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def new_game(self):
        """开始新游戏"""
        # 重置游戏状态
        self.game_state = GameState.PLAYING
        self.first_click = True
        self.start_time = None
        self.elapsed_time = 0
        self.flag_count = 0

        # 重置计时器
        self.timer_var.set("000")
        self.mine_counter_var.set(f"{self.mines:03d}")

        # 更新笑脸按钮
        self.new_game_btn.config(text='😊')

        # 初始化游戏数据
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.flagged = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.cells_to_reveal = self.rows * self.cols - self.mines

        # 重置按钮外观
        for i in range(self.rows):
            for j in range(self.cols):
                self.buttons[i][j].config(
                    text='',
                    bg=self.colors['default'],
                    fg='black',
                    relief=tk.RAISED,
                    state=tk.NORMAL
                )

    def change_difficulty(self, rows, cols, mines):
        """改变游戏难度"""
        self.rows = rows
        self.cols = cols
        self.mines = mines

        # 重建游戏面板
        self.game_frame.destroy()
        self.create_game_panel(self.master)

        self.new_game()

    def place_mines(self, avoid_row, avoid_col):
        """放置地雷，避开第一次点击的位置"""
        mines_placed = 0

        while mines_placed < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)

            # 避开第一次点击的位置及其周围8格
            if abs(row - avoid_row) <= 1 and abs(col - avoid_col) <= 1:
                continue

            if self.board[row][col] != -1:
                self.board[row][col] = -1
                mines_placed += 1

                # 更新周围格子的地雷计数
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        new_row, new_col = row + dr, col + dc
                        if (0 <= new_row < self.rows and
                            0 <= new_col < self.cols and
                            self.board[new_row][new_col] != -1):
                            self.board[new_row][new_col] += 1

        # 重新计算需要揭开的格子数（实际地雷数量可能因为避开策略而略有调整）
        actual_mines = sum(row.count(-1) for row in self.board)
        self.cells_to_reveal = self.rows * self.cols - actual_mines

    def start_timer(self):
        """开始计时"""
        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        """更新计时器"""
        if self.game_state == GameState.PLAYING and self.start_time:
            self.elapsed_time = int(time.time() - self.start_time)
            self.timer_var.set(f"{min(self.elapsed_time, 999):03d}")
            self.master.after(1000, self.update_timer)

    def on_left_click(self, row, col):
        """处理左键点击"""
        if self.game_state != GameState.PLAYING:
            return

        if self.revealed[row][col] or self.flagged[row][col]:
            return

        # 第一次点击时放置地雷
        if self.first_click:
            self.place_mines(row, col)
            self.first_click = False
            self.start_timer()

        self.reveal_cell(row, col)

    def on_right_click(self, row, col):
        """处理右键点击"""
        if self.game_state != GameState.PLAYING:
            return

        if self.revealed[row][col]:
            return

        self.toggle_flag(row, col)

    def reveal_cell(self, row, col):
        """揭开指定格子"""
        if self.revealed[row][col] or self.flagged[row][col]:
            return

        self.revealed[row][col] = True
        btn = self.buttons[row][col]

        # 踩雷
        if self.board[row][col] == -1:
            btn.config(
                text='💣',
                bg=self.colors['mine'],
                relief=tk.SUNKEN
            )
            self.game_over(False)
            return

        # 正常格子
        self.cells_to_reveal -= 1

        if self.board[row][col] == 0:
            # 空格子 - 洪水填充
            btn.config(
                bg=self.colors['revealed'],
                relief=tk.SUNKEN
            )
            self.flood_fill(row, col)
        else:
            # 数字格子
            btn.config(
                text=str(self.board[row][col]),
                bg=self.colors['revealed'],
                fg=self.colors['text'][self.board[row][col] - 1],
                relief=tk.SUNKEN
            )

        # 检查胜利条件
        if self.cells_to_reveal == 0:
            self.game_over(True)

    def flood_fill(self, row, col):
        """洪水填充算法"""
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                new_row, new_col = row + dr, col + dc

                if (0 <= new_row < self.rows and
                    0 <= new_col < self.cols and
                    not self.revealed[new_row][new_col] and
                    not self.flagged[new_row][new_col]):

                    self.revealed[new_row][new_col] = True
                    self.cells_to_reveal -= 1

                    btn = self.buttons[new_row][new_col]
                    if self.board[new_row][new_col] == 0:
                        btn.config(
                            bg=self.colors['revealed'],
                            relief=tk.SUNKEN
                        )
                        self.flood_fill(new_row, new_col)
                    else:
                        btn.config(
                            text=str(self.board[new_row][new_col]),
                            bg=self.colors['revealed'],
                            fg=self.colors['text'][self.board[new_row][new_col] - 1],
                            relief=tk.SUNKEN
                        )

    def toggle_flag(self, row, col):
        """切换标记状态"""
        btn = self.buttons[row][col]

        if self.flagged[row][col]:
            # 取消标记
            self.flagged[row][col] = False
            self.flag_count -= 1
            btn.config(text='')
        else:
            # 添加标记
            if self.flag_count >= self.mines:
                messagebox.showwarning("提示", "标记数量已达地雷总数！")
                return

            self.flagged[row][col] = True
            self.flag_count += 1
            btn.config(text='🚩', fg=self.colors['flag'])

        self.mine_counter_var.set(f"{self.mines - self.flag_count:03d}")

    def game_over(self, won):
        """游戏结束"""
        self.game_state = GameState.WON if won else GameState.LOST

        # 更新笑脸
        self.new_game_btn.config(text='😎' if won else '😵')

        if won:
            messagebox.showinfo("恭喜", "🎉 恭喜你，扫雷成功！")
        else:
            # 显示所有地雷
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.board[i][j] == -1 and not self.flagged[i][j]:
                        self.buttons[i][j].config(
                            text='💣',
                            bg=self.colors['mine'],
                            relief=tk.SUNKEN
                        )
                    elif self.flagged[i][j] and self.board[i][j] != -1:
                        self.buttons[i][j].config(text='❌')

            messagebox.showwarning("游戏结束", "💣 很遗憾，你踩到地雷了！")

def main():
    """主函数"""
    root = tk.Tk()
    root.configure(bg='#c0c0c0')

    # 设置窗口位置在屏幕中央
    root.update_idletasks()
    width = 400
    height = 500
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    # 创建游戏
    game = MinesweeperGUI(root)

    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    main()