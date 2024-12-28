class TrendLine:
    def __init__(self, k=1, b=0):
        self.k = k
        self.b = b

    def construct_by_points(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2

        # 应当考虑斜率不存在，实际中不会出现，故不考虑
        self.k = (y2 - y1) / (x2 - x1)
        self.b = y1 - self.k * x1


def trend_line_cross(tl1: TrendLine, tl2: TrendLine):
    x = - (tl1.b - tl2.b) / (tl1.k - tl2.k)
    y = tl1.k * x + tl1.b

    return x, y


tl1 = TrendLine()
tl2 = TrendLine()

tl1.construct_by_points((0, 1.063), (30, 1.148))
tl2.construct_by_points((19, 1.397), (41, 1.309))

c = trend_line_cross(tl1, tl2)

print(c)