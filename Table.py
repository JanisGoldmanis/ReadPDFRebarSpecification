class Table:
    def __init__(self, min_x, max_x, min_y, max_y, row_height=5.75, blank_height=2.3):
        self.min_x = round(min_x, 1)
        self.max_x = round(max_x, 1)
        self.min_y = round(min_y, 1)
        self.max_y = round(max_y, 1)

        self.height = round(max_y-min_y, 1)

        self.row_height = row_height
        self.blank_height = blank_height

        self.n = int(self.height / (self.row_height + self.blank_height))

        self.x_domains = []
        self.y_domains = []
