#!/usr/bin/env python3
"""
扫雷游戏测试脚本
"""

from minesweeper import Minesweeper

def test_basic_functionality():
    """测试基本功能"""
    print("测试扫雷游戏基本功能...")

    # 创建一个简单的测试游戏
    game = Minesweeper(5, 5, 5)

    print("初始游戏板:")
    for row in game.board:
        print(row)

    print("\n可见状态:")
    for row in game.revealed:
        print(row)

    print(f"\n游戏状态: 行数={game.rows}, 列数={game.cols}, 地雷数={game.mines}")
    print(f"剩余需要揭开的格子: {game.cells_to_reveal}")

def test_flood_fill():
    """测试洪水填充功能"""
    print("\n\n测试洪水填充功能...")

    # 创建一个没有地雷的小游戏板来测试洪水填充
    game = Minesweeper(5, 5, 0)  # 0个地雷，所有格子都是空格

    print("游戏板 (0表示空格):")
    for row in game.board:
        print(row)

    # 揭开中间的格子
    print("\n揭开格子(2,2)后:")
    game.reveal_cell(2, 2)

    for row in game.revealed:
        print(row)

    print(f"剩余需要揭开的格子: {game.cells_to_reveal}")

def test_flagging():
    """测试标记功能"""
    print("\n\n测试标记功能...")

    game = Minesweeper(5, 5, 3)

    print("初始标记数:", game.flagged_mines)

    # 标记几个格子
    game.toggle_flag(0, 0)
    game.toggle_flag(1, 1)
    game.toggle_flag(2, 2)

    print("标记3个格子后的可见状态:")
    for row in game.revealed:
        print(row)
    print("当前标记数:", game.flagged_mines)

    # 取消标记
    game.toggle_flag(1, 1)
    print("\n取消标记(1,1)后的可见状态:")
    for row in game.revealed:
        print(row)
    print("当前标记数:", game.flagged_mines)

def test_adjacent_mine_counting():
    """测试地雷计数功能"""
    print("\n\n测试地雷计数功能...")

    # 创建一个已知配置的游戏来测试地雷计数
    game = Minesweeper(3, 3, 1)

    # 手动设置一个地雷在中心位置
    game.board = [[0, 0, 0],
                  [0, -1, 0],
                  [0, 0, 0]]

    # 重新计算周围的地雷数
    for i in range(3):
        for j in range(3):
            if game.board[i][j] != -1:
                count = 0
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0:
                            continue
                        ni, nj = i + di, j + dj
                        if 0 <= ni < 3 and 0 <= nj < 3 and game.board[ni][nj] == -1:
                            count += 1
                game.board[i][j] = count

    print("游戏板配置:")
    for row in game.board:
        print(row)

    # 测试揭开周围格子
    print("\n揭开周围格子:")
    game.reveal_cell(0, 0)
    game.reveal_cell(0, 1)
    game.reveal_cell(1, 0)

    for row in game.revealed:
        print(row)

if __name__ == "__main__":
    test_basic_functionality()
    test_flood_fill()
    test_flagging()
    test_adjacent_mine_counting()

    print("\n\n所有测试完成!")