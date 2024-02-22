import sys

class generate_wwn():
    def __init__(self,noofwwn):
        self.no_reqwwn = noofwwn
        self.start_wwnno = 0
        self.end_wwnno = self.start_wwnno + self.no_reqwwn

    def pairwise(self,it):
        it = iter(it)
        while True:
            yield next(it), next(it)

    def get_wwn(self):
        wwns = {}
        for i in range(self.start_wwnno, self.end_wwnno):
            wwn = format(i, 'X').zfill(16)
            w=[]
            for a, b in self.pairwise(wwn):
                byte = "%s%s"%(a,b)
                w.append(byte)
            wwns.update({i:w})
        replace_wwn = []
        for each in wwns.values():
            replace_wwn.append((":").join(each))
        return replace_wwn

