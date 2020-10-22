#!/usr/bin/env python3
# coding: utf8
import argparse
import csv
import sys

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
class Cell:
    def __init__(self):
        self.__textMap = []
        self.__textLenMap = []
        self.__spanLenMap = []
        self.__row_header_num = 0
        self.__col_header_num = 0
    @property
    def RowHeaderNum(self): return self.__row_header_num
    @property
    def ColumnHeaderNum(self): return self.__col_header_num
    @property
    def TextMap(self): return self.__textMap
    @property
    def TextLenMap(self): return self.__textLenMap
    @property
    def SpanLenMap(self): return self.__spanLenMap
    def merge(self, tsv):
        self.__calcTextLen(tsv)
        self.__calcSpanLen()
    def __calcTextLen(self, tsv):
        for cols in csv.reader(tsv, delimiter='\t'):
            self.__textMap.append([ col for col in cols ])
            self.__textLenMap.append([ len(col) for col in cols ])
        print(self.__textMap)
        print(self.__textLenMap)
    def __calcSpanLen(self):
        for ri, row in enumerate(self.__textLenMap):
            self.__spanLenMap.append([])
            for ci, col in enumerate(self.__textLenMap[ri]):
                if 0 == col: self.__spanLenMap[-1].append((0,0))
                else:
                    rs = self.__RowSpanLen(ri, ci)
                    cs = self.__ColSpanLen(ri, ci)
                    if self.__isZeroRect(ri, ci, rs, cs): self.__spanLenMap[-1].append((rs,cs))
                    else: self.__spanLenMap[-1].append((1,1))
                print(self.__spanLenMap[-1][-1], end=',')
            print()
        self.__LeftTopSpanLen()
        print(self.__spanLenMap)
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
    def __isZeroRect(self, ri, ci, rs, cs):
        if 1 < rs and 1 < cs:
            for R in range(ri, ri+rs):
                for C in range(ci, ci+cs):
                    if not 0 == self.__textLenMap[R][C]: return False
        return True
    def __LeftTopSpanLen(self):
        rs = self.__RowSpanLen(0, 0)
        cs = self.__ColSpanLen(0, 0)
        if self.__isZeroRect(0, 0, rs, cs):
            self.__spanLenMap[0].pop(0)
            self.__spanLenMap[0].insert(0, (rs,cs))
            self.__row_header_num = rs
            self.__col_header_num = cs

class ToTable:
    def __init__(self, cell):
        self.cell = cell
    def make(self):
        return Html.enclose('table', self.__make_row_header() + self.__make_body())
    def __make_row_header(self):
        html = ''
        for ri in range(len(self.cell.TextMap)):
            tr = ''
            for ci in range(len(self.cell.TextMap[ri])):
                if (0,0) == self.cell.SpanLenMap[ri][ci]: continue
                tr += Html.enclose('th', self.cell.TextMap[ri][ci], self.__make_attr(ri, ci))
            html += Html.enclose('tr', tr)
        return html
    def __make_body(self):
        html = ''
        for ri in range(self.cell.RowHeaderNum, len(self.cell.TextMap)-self.cell.RowHeaderNum):
            th = ''
            td = ''
            for chi in range(self.cell.ColumnHeaderNum):
                if (0,0) == self.cell.SpanLenMap[ri][chi]: continue
                th += Html.enclose('th', self.cell.TextMap[ri][chi], self.__make_attr(ri, chi))
            for cdi in range(self.cell.ColumnHeaderNum, len(self.cell.TextMap)):
                if (0,0) == self.cell.SpanLenMap[ri][chi]: continue
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
