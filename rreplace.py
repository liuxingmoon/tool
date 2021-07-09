"""从右往左替换函数
用法：
rreplace("lemon tree", "e", "3")
rreplace("lemon tree", "e", "3", 1)
rreplace("lemon tree", "e", "3", 2)
rreplace("lemon tree", "tree", "")
"""

def rreplace(self, old, new, *max):
    count = len(self)
    if max and str(max[0]).isdigit():
        count = max[0]
    return new.join(self.rsplit(old, count))
