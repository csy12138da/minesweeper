#!/usr/bin/env python3
"""
扫雷游戏演示脚本
展示游戏的主要功能
"""

from minesweeper import Minesweeper

def demo_game():
    """演示游戏功能"""
    print("=== 扫雷游戏演示 ===\n")

    # 创建一个小的演示游戏
    game = Minesweeper(8, 8, 10)

    print("初始游戏板 (调试模式，显示地雷位置):")
    print("* 表示地雷，数字表示周围地雷数")
    for i, row in enumerate(game.board):
        print(f"第{i}行:", row)

    print("\n开始游戏演示...\n")

    # 模拟一些游戏操作
    demo_moves = [
        (0, 0, 'r', "揭开左上角 (0,0)"),
        (1, 1, 'r', "揭开 (1,1)"),
        (2, 2, 'f', "标记 (2,2) 为可疑地雷"),
        (3, 3, 'r', "揭开 (3,3)"),
        (1, 0, 'r', "揭开 (1,0)"),
    ]

    for row, col, action, description in demo_moves:
        if game.game_over:
            break

        print(f"步骤: {description}")
        print(f"操作: 揭开 ({row}, {col})" if action == 'r' else f"操作: 标记 ({row}, {col})")

        if action == 'f':
            game.toggle_flag(row, col)
        else:
            if not game.reveal_cell(row, col):
                print("💥 踩到地雷了！")
                break

        # 显示当前游戏状态
        print("当前游戏板:")
        game.display_board_simple()
        print(f"剩余地雷: {game.mines - game.flagged_mines}")
        print(f"剩余格子: {game.cells_to_reveal}")
        print("-" * 40)

    # 显示最终结果
    if game.game_won:
        print("🎉 游戏胜利！")
    elif game.game_over:
        print("💥 游戏结束！")
    else:
        print("游戏演示结束")

    print("\n最终游戏板 (显示所有地雷):")
    for i, row in enumerate(game.board):
        for j, cell in enumerate(row):
            if cell == -1:
                print("* ", end="")
            else:
                print(f"{cell} ", end="")
        print()

def demo_flood_fill():
    """演示洪水填充功能"""
    print("\n=== 洪���填充演示 ===\n")

    # 创建一个地雷很少的游戏来演示洪水填充
    game = Minesweeper(6, 6, 2)

    print("地雷位置:")
    for i in range(game.rows):
        for j in range(game.cols):
            if game.board[i][j] == -1:
                print(f"地雷在 ({i}, {j})")

    print("\n执行洪水填充演示...")
    # 找一个空格位置进行揭开
    found_empty = False
    for i in range(game.rows):
        for j in range(game.cols):
            if game.board[i][j] == 0:
                print(f"揭开空格 ({i}, {j})")
                game.reveal_cell(i, j)
                found_empty = True
                break
        if found_empty:
            break

    print("\n洪水填充结果:")
    game.display_board_simple()

if __name__ == "__main__":
    demo_game()
    demo_flood_fill()