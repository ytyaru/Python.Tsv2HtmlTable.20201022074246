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
        Cell().merge(self.__stdin)
class Cell:
    def __init__(self):
        self.__textMap = []
        self.__textLenMap = []
        self.__spanLenMap = []
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
#                    print('rc:', rs, cs)
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

class ToTable:
    def to_table(self, textMap, spanMap):
        for sr in spanMap:
            for sc in spanMap[sr]:
                pass

        
#    def __make_row_header(self):
        
#    def __make_body(self):
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
    TsvToTable().parse()
