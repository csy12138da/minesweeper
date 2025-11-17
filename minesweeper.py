#!/usr/bin/env python3
"""
一个基于Python的扫雷游戏
A Minesweeper game implemented in Python
"""

import random
import os
import sys
from typing import List, Tuple, Optional

class Minesweeper:
    def __init__(self, rows: int = 10, cols: int = 10, mines: int = 10):
        """
        初始化扫雷游戏

        Args:
            rows: 行数
            cols: 列数
            mines: 地雷数量
        """
        self.rows = rows
        self.cols = cols
        self.mines = mines

        # 游戏板状态: 0-8表示周围地雷数, -1表示地雷
        self.board: List[List[int]] = []
        # 玩家可见状态: ' '未揭开, 'F'已标记, 数字表示已揭开
        self.revealed: List[List[str]] = []
        # 游戏状���
        self.game_over = False
        self.game_won = False
        # 剩余未揭开且非地雷的格子数
        self.cells_to_reveal = rows * cols - mines
        # 已标记的地雷数
        self.flagged_mines = 0

        self.init_board()

    def init_board(self):
        """初始化游戏板"""
        # 初始化空板
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]

        # 放置地雷
        mines_placed = 0
        while mines_placed < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)

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

    def display(self):
        """显示游戏板"""
        os.system('clear' if os.name == 'posix' else 'cls')

        print(f"扫雷游戏 - 剩余地雷: {self.mines - self.flagged_mines}")
        print(f"状态: {'游戏结束' if self.game_over else '胜利!' if self.game_won else '进行中'}")
        print()

        # 显示列号
        print("   " + " ".join(f"{i:2d}" for i in range(self.cols)))
        print("   " + "---" * self.cols)

        for i, row in enumerate(self.revealed):
            # 显示行号
            print(f"{i:2d}|", end="")

            for j, cell in enumerate(row):
                if cell == ' ':
                    print(" ?", end=" ")
                elif cell == 'F':
                    print(" F", end=" ")
                else:
                    print(f" {cell}", end=" ")
            print()
        print()

    def get_valid_input(self, prompt: str) -> Tuple[int, int, str]:
        """获取有效的用户输入"""
        while True:
            try:
                user_input = input(prompt).strip().split()
                if len(user_input) < 2:
                    print("请输入 行 列 [操作]，例如: 0 0 或 0 0 f")
                    continue

                row = int(user_input[0])
                col = int(user_input[1])
                action = user_input[2].lower() if len(user_input) > 2 else 'r'

                if not (0 <= row < self.rows and 0 <= col < self.cols):
                    print(f"请输入有效的坐标 (0-{self.rows-1}, 0-{self.cols-1})")
                    continue

                if action not in ['r', 'f', 'q']:
                    print("操作必须是 'r'(揭开), 'f'(标记), 或 'q'(退出)")
                    continue

                return row, col, action

            except ValueError:
                print("请输入有效的数字坐标")

    def reveal_cell(self, row: int, col: int) -> bool:
        """
        揭开指定位置的格子

        Returns:
            True表示游戏继续, False表示踩雷
        """
        if self.revealed[row][col] != ' ' and self.revealed[row][col] != 'F':
            return True  # 已经揭开的格子

        if self.revealed[row][col] == 'F':
            return True  # 已标记的格子不能揭开

        # 踩雷
        if self.board[row][col] == -1:
            self.revealed[row][col] = '*'
            self.game_over = True
            self.reveal_all_mines()
            return False

        # 揭开格子
        self.revealed[row][col] = str(self.board[row][col])
        self.cells_to_reveal -= 1

        # 如果是空格，使用洪水填充揭开周围的格子
        if self.board[row][col] == 0:
            self.flood_fill(row, col)

        # 检查是否获胜
        if self.cells_to_reveal == 0:
            self.game_won = True
            self.game_over = True
            self.revealed[row][col] = 'W'  # 标记最后一个揭开的格子

        return True

    def flood_fill(self, row: int, col: int):
        """洪水填充算法，揭开空格及其周围的格子"""
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                new_row, new_col = row + dr, col + dc

                if (0 <= new_row < self.rows and
                    0 <= new_col < self.cols and
                    self.revealed[new_row][new_col] == ' '):

                    self.revealed[new_row][new_col] = str(self.board[new_row][new_col])
                    self.cells_to_reveal -= 1

                    # 如果周围也是空格，递归处理
                    if self.board[new_row][new_col] == 0:
                        self.flood_fill(new_row, new_col)

    def toggle_flag(self, row: int, col: int):
        """切换格子的标记状态"""
        if self.revealed[row][col] not in [' ', 'F']:
            print("已揭开的格子不能标记")
            return

        if self.revealed[row][col] == ' ':
            if self.flagged_mines < self.mines:
                self.revealed[row][col] = 'F'
                self.flagged_mines += 1
            else:
                print(f"标记数量已达到地雷总数 {self.mines}")
        else:
            self.revealed[row][col] = ' '
            self.flagged_mines -= 1

    def reveal_all_mines(self):
        """游戏结束时显示所有地雷"""
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == -1:
                    if self.revealed[i][j] != 'F':  # 已正确标记的地雷不覆盖
                        self.revealed[i][j] = '*'
                elif self.revealed[i][j] == 'F':  # 显示错误标记
                    self.revealed[i][j] = 'X'

    def play(self):
        """主游戏循环"""
        print("欢迎来到扫雷游戏!")
        print("输入格式: 行 列 [操作]")
        print("操作: r(揭开, 默认), f(标记), q(退出)")
        print("例如: 0 0   - 揭开(0,0)")
        print("例如: 0 0 f - 标记(0,0)")
        print()

        while not self.game_over:
            self.display()

            try:
                prompt = "请输入坐标和操作 (行 列 [r/f/q]): "
                row, col, action = self.get_valid_input(prompt)

                if action == 'q':
                    print("游戏退出")
                    return

                if action == 'f':
                    self.toggle_flag(row, col)
                else:  # 'r'
                    if not self.reveal_cell(row, col):
                        break  # 踩雷了

            except KeyboardInterrupt:
                print("\n游戏退出")
                return
            except Exception as e:
                print(f"发生错误: {e}")
                continue

        self.display()

        if self.game_won:
            print("🎉 恭喜你，扫雷成功！")
        else:
            print("💣 很遗憾，你踩到地雷了！")

        self.show_solution()

    def display_board_simple(self):
        """简化版的游戏板显示，用于演示"""
        for i, row in enumerate(self.revealed):
            print(f"{i:2d}|", end="")
            for j, cell in enumerate(row):
                if cell == ' ':
                    print(" ?", end=" ")
                elif cell == 'F':
                    print(" F", end=" ")
                elif cell == 'W':
                    print(" W", end=" ")
                else:
                    print(f" {cell}", end=" ")
            print()
        print()

    def show_solution(self):
        """显示最终解答"""
        print("\n最终游戏板:")
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == -1:
                    print("* ", end="")
                else:
                    print(f"{self.board[i][j]} ", end="")
            print()

def main():
    """主函数"""
    print("扫雷游戏设置")
    print("1. 简单 (8x8, 10个地雷)")
    print("2. 中等 (16x16, 40个地雷)")
    print("3. 困难 (16x30, 99个地雷)")
    print("4. 自定义")

    while True:
        try:
            choice = input("请选择难度 (1-4): ").strip()

            if choice == '1':
                game = Minesweeper(8, 8, 10)
                break
            elif choice == '2':
                game = Minesweeper(16, 16, 40)
                break
            elif choice == '3':
                game = Minesweeper(16, 30, 99)
                break
            elif choice == '4':
                rows = int(input("请输入行数 (5-20): "))
                cols = int(input("请输入列数 (5-30): "))
                mines = int(input(f"请输入地雷数 (1-{rows*cols-1}): "))

                if not (5 <= rows <= 20 and 5 <= cols <= 30):
                    print("行数和列数超出范围")
                    continue
                if not (1 <= mines < rows * cols):
                    print("地雷数量无效")
                    continue

                game = Minesweeper(rows, cols, mines)
                break
            else:
                print("请输入1-4之间的数字")

        except ValueError:
            print("请输入有效的数字")
        except KeyboardInterrupt:
            print("\n游戏退出")
            sys.exit(0)

    game.play()

if __name__ == "__main__":
    main()