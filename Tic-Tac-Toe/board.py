import numpy as np


class Board:
    """
    Quản lý bàn cờ và các hàm liên quan
    """

    def __init__(self, size=8):
        """
        Khởi tạo bàn cờ với kích thước size x size
        HEURISTIC: mảng 2 chiều lưu giá trị heuristic cho mỗi ô
        """
        self.size = size
        self.empty = "·"
        self.board = np.full((self.size, self.size), self.empty, dtype=str)
        self.HEURISTIC = self.generate_heuristic(size)

    def generate_heuristic(self, size):
        """
        Tạo mảng 2 chiều lưu giá trị heuristic cho mỗi ô
        Giá trị heuristic = min(i, j, size - i - 1, size - j - 1)
        Example: size = 3
            0 0 0
            0 1 0
            0 0 0
        """
        heuristic = np.zeros((size, size), dtype=int)
        for i in range(size):
            for j in range(size):
                heuristic[i][j] = min(i, j, size - i - 1, size - j - 1)
        return heuristic

    def draw(self):
        """
        Hiển thị bàn cờ trên màn hình console
        """
        header = "  " + " ".join(str(i) for i in range(self.size))
        print(header)
        for i, row in enumerate(self.board):
            print(f"{i} " + " ".join(row))

    def is_valid_move(self, move):
        """
        Kiểm tra nước đi có hợp lệ
        """
        x, y = move
        return 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == self.empty

    def make_move(self, x, y, player):
        """
        Thực hiện nước đi của player
        """
        if self.is_valid_move((x, y)):
            self.board[x][y] = player
            return True
        return False

    def undo_move(self, x, y):
        """
        Xóa nước đi tại vị trí (x, y)
        """
        self.board[x][y] = self.empty

    def get_all_lines(self):
        """
        Lấy tất cả các dòng, cột, đường chéo trên bàn cờ
        """
        lines = []
        for row in self.board:
            lines.append("".join(row))
        for col in range(self.size):
            lines.append("".join(self.board[:, col]))
        for d in range(-self.size + 1, self.size):
            lines.append("".join(self.board.diagonal(d)))
            lines.append("".join(np.fliplr(self.board).diagonal(d)))
        return lines

    def is_full(self):
        """
        Kiểm tra bàn cờ đã đầy chưa
        """
        return not np.any(self.board == self.empty)
