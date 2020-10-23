#!/usr/bin/env python3
# coding: utf8
import argparse
import csv
import sys
import numpy
from abc import ABCMeta, abstractmethod

class TsvToTable:
    def __init__(self): pass
    def parse(self):
        self.__stdin = [line.rstrip('\n') for line in sys.stdin.readlines()]
        print(self.__stdin)
        parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')
        parser.add_argument('-H', '--header', default='r', help='ヘッダ形式')
        parser.add_argument('-r', '--row', default='r', help='行ヘッダの表示位置')
        parser.add_argument('-c', '--column', default='r', help='列ヘッダの表示位置')
        parser.add_argument('-m', '--merge', action='store_false', help='セル結合しない。')
        self.__args = parser.parse_args()

        cell = Cell()
        cell.merge(self.__stdin)
        return ToTable(cell).make()

class RowHeader:
    def __init__(self, textLenMap):
        self.__len = self.__inferLength(textLenMap)
        self.__calcSpanMap(textLenMap)
    @property
    def Length(self): return self.__len
    @property
    def SpanMap(self): return self.__spanMap
    def __inferLength(self, textLenMap):
        is_exist_map = numpy.full(len(textLenMap), False)
        for ri, row in enumerate(textLenMap):
            for ci, col in enumerate(textLenMap[ri]):
                if not 0 == col: is_exist_map[ci] = True
            if all(is_exist_map): return ri if 0 < ri else 1
    def __calcSpanMap(self, textLenMap):
        self.__spanLenMap = []
        for ri in range(self.Length):
            self.__spanLenMap.append([])
            for ci in range(len(textLenMap[ri])):
                if 0 == textLenMap[ri][ci]: self.__spanLenMap[-1].append([0,0])
                else:
#                    rs = self.__RowSpanLen(ri, ci)
#                    cs = self.__ColSpanLen(ri, ci)
                    rs = Merger.getRowZeroLen(textLenMap, ri, ci)
                    cs = Merger.getColZeroLen(textLenMap, ri, ci)
                    self.__spanLenMap[-1].append([rs,cs])
                print(self.__spanLenMap[-1][-1], end=',')
            print()
        self.__LeftTopSpanLen(textLenMap)
        Merger.setColspanStopByRowspan(self.__spanLenMap)
        Merger.setRowspanStopByColspan(self.__spanLenMap)
#        self.__ColspanStopByRowspan()
#        self.__RowspanStopByColspan()
        self.__CrossSpanHeader()
#        self.__ZeroRect()
        print()
        for ri in range(len(self.__spanLenMap)):
            print(*self.__spanLenMap[ri])

    def __LeftTopSpanLen(self, textLenMap):
        if 0 == self.__spanLenMap[0][0][0] and 0 == self.__spanLenMap[0][0][1]:
            rs = Merger.getRowZeroLen(textLenMap, 0, 0)
            cs = Merger.getColZeroLen(textLenMap, 0, 0)
            if Merger.isZeroRect(textLenMap, 0, 0, rs, cs):
                self.__spanLenMap[0][0][0] = rs
                self.__spanLenMap[0][0][1] = cs

    def __CrossSpanHeader(self):
        self.__CrossSpanR()
    def __CrossSpanR(self):
        for ri in range(self.Length):
            for ci in range(len(self.__spanLenMap[ri])):
                if 1 < self.__spanLenMap[ri][ci][1]:
                    C = self.__CrossSpanRC(ri, ci, self.__spanLenMap[ri][ci][1])
                    if C is not None: self.__spanLenMap[ri][ci][1] = C
    def __CrossSpanRC(self, ri, ci, cs):
        for C in range(ci+1, ci+cs):
            for R in reversed(range(ri)):
                if ri <= self.__spanLenMap[R][C][0] - 1 - R + ri: return C - ci
        return None

class ColumnHeader:
    def __init__(self, textLenMap, row_header_len):
        self.__row_header_len = row_header_len
        self.__len = self.__inferLength(textLenMap)
        self.__calcSpanMap(textLenMap)
    @property
    def Length(self): return self.__len
    @property
    def SpanMap(self): return self.__spanMap
    def __inferLength(self, textLenMap):
        col_len = 0
        for ci, col in enumerate(textLenMap[0]):
            if 0 == col: col_len += 1
            else: break
        return col_len
    def __calcSpanMap(self, textLenMap):
        self.__spanLenMap = []
        for ri in range(self.__row_header_len, len(textLenMap)):
            self.__spanLenMap.append([])
            for ci in range(self.Length):
                if 0 == textLenMap[ri][ci]: self.__spanLenMap[-1].append([0,0])
                else:
#                    rs = self.__RowSpanLen(ri, ci)
#                    cs = self.__ColSpanLen(ri, ci)
                    rs = Merger.getRowZeroLen(textLenMap, ri, ci)
                    cs = Merger.getColZeroLen(textLenMap, ri, ci)
                    self.__spanLenMap[-1].append([rs,cs])
                print(self.__spanLenMap[-1][-1], end=',')
            print()
        Merger.setColspanStopByRowspan(self.__spanLenMap)
        Merger.setRowspanStopByColspan(self.__spanLenMap)
#        self.__LeftTopSpanLen()
#        self.__ColspanStopByRowspan()
#        self.__RowspanStopByColspan()
        self.__CrossSpanHeader()
#        self.__ZeroRect()
        print()
        for ri in range(len(self.__spanLenMap)):
            print(*self.__spanLenMap[ri])

    def __CrossSpanHeader(self):
#        self.__CrossSpanR()
        self.__CrossSpanC()
    def __CrossSpanR(self):
        for ri in range(self.Length):
            for ci in range(len(self.__spanLenMap[ri])):
                if 1 < self.__spanLenMap[ri][ci][1]:
                    C = self.__CrossSpanRC(ri, ci, self.__spanLenMap[ri][ci][1])
                    if C is not None: self.__spanLenMap[ri][ci][1] = C
    def __CrossSpanRC(self, ri, ci, cs):
        for C in range(ci+1, ci+cs):
            for R in reversed(range(ri)):
                if ri <= self.__spanLenMap[R][C][0] - 1 - R + ri: return C - ci
        return None
    def __CrossSpanC(self):
        for ri in range(len(self.__spanLenMap)):
            for ci in range(self.Length):
                if 1 < self.__spanLenMap[ri][ci][0]:
                    R = self.__CrossSpanCR(ri, ci, self.__spanLenMap[ri][ci][0])
                    if R is not None: self.__spanLenMap[ri][ci][0] = R
    def __CrossSpanCR(self, ri, ci, rs):
        for R in range(ri+1, ri+rs):
            for C in reversed(range(ci)):
                if ci <= self.__spanLenMap[R][C][1] - 1 - C + ci: return R - ri
        return None

class Merger:
    @staticmethod
    def getRowZeroLen(textLenMap, ri, ci):
        row_len = 1
        if len(textLenMap) <= ri+row_len: return row_len
        while ri+row_len < len(textLenMap):
            if 0 == textLenMap[ri+row_len][ci]: row_len += 1
            else: break
        return row_len
    @staticmethod
    def getColZeroLen(textLenMap, ri, ci):
        col_len = 1
        if len(textLenMap[ri]) <= ci+col_len: return col_len
        while ci+col_len < len(textLenMap[ri]):
            if 0 == textLenMap[ri][ci+col_len]: col_len += 1
            else: break
        return col_len
    @staticmethod
    def isZeroRect(textLenMap, ri, ci, rs, cs):
        if 1 < rs and 1 < cs:
            for R in range(ri, ri+rs):
                for C in range(ci, ci+cs):
                    if not 0 == textLenMap[R][C]: return False
        return True
    @staticmethod
    def setColspanStopByRowspan(spanLenMap):
        for ri in range(len(spanLenMap)):
            for ci in range(len(spanLenMap[ri])):
                Merger.__setColspanMinus(spanLenMap, ri, ci, spanLenMap[ri][ci][0])
    @staticmethod
    def __setColspanMinus(spanLenMap, ri, ci, rlen):
        if 1 < spanLenMap[ri][ci][0]:
            for R in range(ri+1, ri+rlen):
                spanLenMap[R][ci][1] = -1
    @staticmethod
    def setRowspanStopByColspan(spanLenMap):
        for ri in range(len(spanLenMap)):
            for ci in range(len(spanLenMap[ri])):
                Merger.__setRowspanMinus(spanLenMap, ri, ci, spanLenMap[ri][ci][1])
    @staticmethod
    def __setRowspanMinus(spanLenMap, ri, ci, clen):
        if 1 < spanLenMap[ri][ci][1]:
            for C in range(ci+1, ci+clen):
                spanLenMap[ri][C][0] = -1


class Cell:
    def __init__(self):
        self.__textMap = []
        self.__textLenMap = []
        self.__spanLenMap = []
#        self.__header = Header()
    @property
    def RowHeaderNum(self): return self.__row_header.Length
    @property
    def ColumnHeaderNum(self): return self.__col_header.Length
    @property
    def TextMap(self): return self.__textMap
    @property
    def TextLenMap(self): return self.__textLenMap
    @property
    def SpanLenMap(self): return self.__spanLenMap
    def merge(self, tsv):
        self.__calcTextLen(tsv)
#        self.__calcSpanLen()
#        self.__calcHeaderSpanLen()
    def __calcTextLen(self, tsv):
        for cols in csv.reader(tsv, delimiter='\t'):
            self.__textMap.append([ col for col in cols ])
            self.__textLenMap.append([ len(col) for col in cols ])
        print(self.__textMap)
        print(self.__textLenMap)
#        self.__header.infer(self.__textLenMap)
#        print(self.RowHeaderNum, self.ColumnHeaderNum)
        self.__row_header = RowHeader(self.__textLenMap)
        self.__col_header = ColumnHeader(self.__textLenMap, self.__row_header.Length)


    def __calcHeaderSpanLen(self):
        for ri in range(self.RowHeaderNum):
            for ci in range(self.ColumnHeaderNum):
                if 0 == self.__spanLenMap[ri][ci]: self.__spanLenMap[-1].append([0,0])
                else:
                    rs = self.__RowSpanLen(ri, ci)
                    cs = self.__ColSpanLen(ri, ci)
                    self.__spanLenMap[-1].append([rs,cs])
                print(self.__spanLenMap[-1][-1], end=',')
            print()
        self.__LeftTopSpanLen()
        self.__ColspanStopByRowspan()
        self.__RowspanStopByColspan()
        self.__CrossSpanHeader()
        self.__ZeroRect()
                
    def __calcSpanLen(self):
        for ri, row in enumerate(self.__textLenMap):
            self.__spanLenMap.append([])
            for ci, col in enumerate(self.__textLenMap[ri]):
                if 0 == col: self.__spanLenMap[-1].append([0,0])
                else:
                    rs = self.__RowSpanLen(ri, ci)
                    cs = self.__ColSpanLen(ri, ci)
                    self.__spanLenMap[-1].append([rs,cs])
                print(self.__spanLenMap[-1][-1], end=',')
            print()
        self.__LeftTopSpanLen()
        self.__ColspanStopByRowspan()
        self.__RowspanStopByColspan()
        self.__CrossSpanHeader()
        self.__ZeroRect()
#        self.__ColspanLengthRetry()
#        self.__RowspanLengthRetry()

        print()
        for ri in range(len(self.__spanLenMap)):
            print(*self.__spanLenMap[ri])
#        for ri in range(len(self.__spanLenMap)):
#            for ci in range(len(self.__spanLenMap[ri])):
#                print(self.__spanLenMap[ri][ci].format())
#                print(f'{self.__spanLenMap[ri][ci]:02}')
#        print()

    def __RowSpanLen(self, ri, ci):
        row_len = 1
        if len(self.__textLenMap) <= ri+row_len: return row_len
        while ri+row_len < len(self.__textLenMap):
            if 0 == self.__textLenMap[ri+row_len][ci]: row_len += 1
            else: break
        return row_len
    def __ColSpanLen(self, ri, ci):
        col_len = 1
        if len(self.__textLenMap[ri]) <= ci+col_len: return col_len
        while ci+col_len < len(self.__textLenMap[ri]):
            if 0 == self.__textLenMap[ri][ci+col_len]: col_len += 1
            else: break
        return col_len

    def __CrossSpanHeader(self):
        self.__CrossSpanR()
        self.__CrossSpanC()
    def __CrossSpanR(self):
        for ri in range(self.RowHeaderNum):
            for ci in range(len(self.__spanLenMap[ri])):
                if 1 < self.__spanLenMap[ri][ci][1]:
                    C = self.__CrossSpanRC(ri, ci, self.__spanLenMap[ri][ci][1])
                    if C is not None: self.__spanLenMap[ri][ci][1] = C
    def __CrossSpanRC(self, ri, ci, cs):
        for C in range(ci+1, ci+cs):
            for R in reversed(range(ri)):
                if ri <= self.__spanLenMap[R][C][0] - 1 - R + ri: return C - ci
        return None
    def __CrossSpanC(self):
        for ri in range(self.RowHeaderNum, len(self.__spanLenMap)):
            for ci in range(self.ColumnHeaderNum):
                if 1 < self.__spanLenMap[ri][ci][0]:
                    R = self.__CrossSpanCR(ri, ci, self.__spanLenMap[ri][ci][0])
                    if R is not None: self.__spanLenMap[ri][ci][0] = R
    def __CrossSpanCR(self, ri, ci, rs):
        for R in range(ri+1, ri+rs):
            for C in reversed(range(ci)):
                if ci <= self.__spanLenMap[R][C][1] - 1 - C + ci: return R - ri
        return None

        
#    def __isZeroRect(self, ri, ci, rs, cs):
#        if 1 < rs and 1 < cs:
#            for R in range(ri, ri+rs):
#                for C in range(ci, ci+cs):
#                    if not 0 == self.__textLenMap[R][C]: return False
#        return True
    def __LeftTopSpanLen(self):
        if 0 == self.__spanLenMap[0][0][0] and 0 == self.__spanLenMap[0][0][1]:
            rs = self.__RowSpanLen(0, 0)
            cs = self.__ColSpanLen(0, 0)
            if self.__isZeroRect(0, 0, rs, cs):
                self.__spanLenMap[0][0][0] = rs
                self.__spanLenMap[0][0][1] = cs


    def __setSpanStop(self):
        for ri in range(len(self.__spanLenMap)):
            for ci in range(len(self.__spanLenMap[ri])):
                rr = self.__setSpanStopRC(ri, ci)
                cc = self.__setSpanStopCR(ri, ci)
                  
    def __setSpanStopRC(self):
        if 1 < self.__spanLenMap[ri][ci][0]:
            for R in range(1, self.__spanLenMap[ri][ci][0]):
                return self.__isCrossSpanRC(ri+R, ci)

    def __checkRowSpanLenCells(self, ri, ci):
        for R in range(1, self.__spanLenMap[ri][ci][0]):
            rr = self.__isCrossSpan(ri+R, ci)
            if rr is not None: return rr
        
    def __isCrossSpanRC(self, ri, ci):
        for C in range(1, ci):
            if ci <= self.__spanLenMap[ri][ci-C][1] - 1 - C + ci: return ri
        return None

    def __ColspanStopByRowspan(self):
        for ri in range(len(self.__spanLenMap)):
            for ci in range(len(self.__spanLenMap[ri])):
                self.__setColspanMinus(ri, ci, self.__spanLenMap[ri][ci][0])
    def __setColspanMinus(self, ri, ci, rlen):
        if 1 < self.__spanLenMap[ri][ci][0]:
            for R in range(ri+1, ri+rlen):
                self.__spanLenMap[R][ci][1] = -1
    def __ColspanLengthRetry(self):
        for ri in range(len(self.__spanLenMap)):
            for ci in range(len(self.__spanLenMap[ri])):
                if 1 < self.__spanLenMap[ri][ci][1]:
                    self.__spanLenMap[ri][ci][1] = self.__ColSpanLenRetry(ri, ci)
    def __ColSpanLenRetry(self, ri, ci):
        col_len = 1
        if len(self.__spanLenMap[ri]) <= ci+col_len: return col_len
        while ci+col_len < len(self.__spanLenMap[ri]):
            if 0 == self.__spanLenMap[ri][ci+col_len][1]: col_len += 1
            else: break
        return col_len
    def __RowspanStopByColspan(self):
        for ri in range(len(self.__spanLenMap)):
            for ci in range(len(self.__spanLenMap[ri])):
                self.__setRowspanMinus(ri, ci, self.__spanLenMap[ri][ci][1])
    def __setRowspanMinus(self, ri, ci, clen):
        if 1 < self.__spanLenMap[ri][ci][1]:
            for C in range(ci+1, ci+clen):
                self.__spanLenMap[ri][C][0] = -1
    def __RowspanLengthRetry(self):
        for ri in range(len(self.__spanLenMap)):
            for ci in range(len(self.__spanLenMap[ri])):
                if 1 < self.__spanLenMap[ri][ci][0]:
                    self.__spanLenMap[ri][ci][0] = self.__RowSpanLenRetry(ri, ci)
    def __RowSpanLenRetry(self, ri, ci):
        row_len = 1
        if len(self.__spanLenMap) <= ri+row_len: return row_len
        while ri+row_len < len(self.__spanLenMap):
            if 0 == self.__spanLenMap[ri+row_len][ci][0]: row_len += 1
            else: break
        return row_len
    def __ZeroRect(self):
        for ri in range(len(self.__spanLenMap)):
            for ci in range(len(self.__spanLenMap[ri])):
                if not self.__isZeroRect(ri, ci, *self.__spanLenMap[ri][ci]):
                    self.__setSpanAllOne(ri, ci, *self.__spanLenMap[ri][ci])
    def __isZeroRect(self, ri, ci, rs, cs):
        if 1 < rs and 1 < cs:
            for R in range(ri, ri+rs):
                for C in range(ci, ci+cs):
                    if not 0 == self.__textLenMap[R][C]: return False
        return True
    def __setSpanAllOne(self, ri, ci, rs, cs):
        self.__spanLenMap[ri][ci][0] = 1
        self.__spanLenMap[ri][ci][1] = 1
        for R in range(ri, ri+rs):
            for C in range(ci, ci+cs):
                if self.__spanLenMap[R][C][0] < 1 and self.__spanLenMap[R][C][1] < 1:
                    self.__spanLenMap[R][C][0] = 1
                    self.__spanLenMap[R][C][1] = 1

class ToTable:
    def __init__(self, cell):
        self.cell = cell
    def make(self):
        return Html.enclose('table', self.__make_row_header() + self.__make_body())
    def __make_row_header(self):
        html = ''
        for ri in range(self.cell.RowHeaderNum):
            tr = ''
            for ci in range(len(self.cell.TextMap[ri])):
                if self.cell.SpanLenMap[ri][ci][0] < 1 and self.cell.SpanLenMap[ri][ci][1] < 1: continue
                tr += Html.enclose('th', self.cell.TextMap[ri][ci], self.__make_attr(ri, ci))
            html += Html.enclose('tr', tr)
        return html
    def __make_body(self):
        html = ''
        for ri in range(self.cell.RowHeaderNum, len(self.cell.TextMap)):
            th = ''
            td = ''
            for chi in range(self.cell.ColumnHeaderNum):
                if self.cell.SpanLenMap[ri][chi][0] < 1 and self.cell.SpanLenMap[ri][chi][1] < 1: continue
                th += Html.enclose('th', self.cell.TextMap[ri][chi], self.__make_attr(ri, chi))
            for cdi in range(self.cell.ColumnHeaderNum, len(self.cell.TextMap)):
                if self.cell.SpanLenMap[ri][cdi][0] < 1 and self.cell.SpanLenMap[ri][cdi][1] < 1: continue
                td += Html.enclose('td', self.cell.TextMap[ri][cdi], self.__make_attr(ri, cdi))
            html += Html.enclose('tr', th+td)
        return html
    def __make_attr(self, ri, ci):
        attrs = {}
        if 1 < self.cell.SpanLenMap[ri][ci][0]: attrs['rowspan'] = self.cell.SpanLenMap[ri][ci][0]
        if 1 < self.cell.SpanLenMap[ri][ci][1]: attrs['colspan'] = self.cell.SpanLenMap[ri][ci][1]
        return attrs
#        attrs = ''
#        if 1 < self.cell.SpanLenMap[ri][ci][0]: attrs += ' rowspan="' + self.cell.SpanLenMap[ri][ci][0] + '"'
#        if 1 < self.cell.SpanLenMap[ri][ci][1]: attrs += ' colspan="' + self.cell.SpanLenMap[ri][ci][1] + '"'
#        return attrs

#    def __make_col_header(self):
#    def __make_data_line(self):

class Html:
    @staticmethod
    def enclose(element, text='', attrs={}):
        return '<' + element + Html.attrs(attrs) + '>' + text + '</' + element + '>'
    @staticmethod
    def attrs(attrs):
        result = ''
        for key in attrs.keys():
            result += ' {}="{}"'.format(key, attrs[key])
        return result

if __name__ == '__main__':
    print(TsvToTable().parse())
