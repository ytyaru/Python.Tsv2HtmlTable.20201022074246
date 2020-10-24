#!/usr/bin/env python3
# coding: utf8
import argparse
import csv
import sys
import numpy
from abc import ABCMeta, abstractmethod

class CLI:
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

        tsv = TSV()
        tsv.parse(self.__stdin)
        return ToTable(tsv).make()

class TSV:
    def __init__(self):
        self.__textMap = []
        self.__textLenMap = []
    def parse(self, tsv):
        self.__textMap.clear()
        self.__textLenMap.clear()
        for cols in csv.reader(tsv, delimiter='\t'):
            self.__textMap.append([ col for col in cols ])
            self.__textLenMap.append([ len(col) for col in cols ])
        print(self.__textMap)
        print(self.__textLenMap)
        self.__row_header = RowHeader(self.__textLenMap)
        self.__col_header = ColumnHeader(self.__textLenMap, self.__row_header.Length)
    @property
    def Map(self): return self.__textMap
    @property
    def LenMap(self): return self.__textLenMap
    @property
    def RowHeader(self): return self.__row_header
    @property
    def ColHeader(self): return self.__col_header

class RowHeader:
    def __init__(self, textLenMap):
        self.__len = self.__inferLength(textLenMap)
        self.__calcSpanMap(textLenMap)
    @property
    def Length(self): return self.__len
    @property
    def SpanLenMap(self): return self.__spanLenMap
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
                    rs = Merger.getRowZeroLen(textLenMap, ri, ci)
                    cs = Merger.getColZeroLen(textLenMap, ri, ci)
                    self.__spanLenMap[-1].append([rs,cs])
                print(self.__spanLenMap[-1][-1], end=',')
            print()
        self.__LeftTopSpanLen(textLenMap)
        Merger.setColspanStopByRowspan(self.__spanLenMap)
        Merger.setRowspanStopByColspan(self.__spanLenMap)
        self.__CrossSpanHeader()
        Merger.setZeroRect(self.__spanLenMap)
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
    def SpanLenMap(self): return self.__spanLenMap
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
                    rs = Merger.getRowZeroLen(textLenMap, ri, ci)
                    cs = Merger.getColZeroLen(textLenMap, ri, ci)
                    self.__spanLenMap[-1].append([rs,cs])
                print(self.__spanLenMap[-1][-1], end=',')
            print()
        Merger.setColspanStopByRowspan(self.__spanLenMap)
        Merger.setRowspanStopByColspan(self.__spanLenMap)
        self.__CrossSpanHeader()
        Merger.setZeroRect(self.__spanLenMap)
        print()
        for ri in range(len(self.__spanLenMap)):
            print(*self.__spanLenMap[ri])

    def __CrossSpanHeader(self):
        self.__CrossSpanC()
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
    @staticmethod
    def setZeroRect(spanLenMap):
        for ri in range(len(spanLenMap)):
            for ci in range(len(spanLenMap[ri])):
                if not Merger.__isZeroRect(spanLenMap, ri, ci, *spanLenMap[ri][ci]):
                    Merger.__setSpanAllOne(spanLenMap, ri, ci, *spanLenMap[ri][ci])
    @staticmethod
    def __isZeroRect(spanLenMap, ri, ci, rs, cs):
        if 1 < rs and 1 < cs:
            for R in range(ri+1, ri+rs):
                for C in range(ci+1, ci+cs):
                    print(ri, ci, rs, cs, R,C, spanLenMap[R][C])
                    if not (spanLenMap[R][C][0] < 1 and spanLenMap[R][C][1] < 1): return False
        return True
    @staticmethod
    def __setSpanAllOne(spanLenMap, ri, ci, rs, cs):
        spanLenMap[ri][ci][0] = 1
        spanLenMap[ri][ci][1] = 1
        for R in range(ri, ri+rs):
            for C in range(ci, ci+cs):
                if spanLenMap[R][C][0] < 1 and spanLenMap[R][C][1] < 1:
                    spanLenMap[R][C][0] = 1
                    spanLenMap[R][C][1] = 1

class ToTable:
    def __init__(self, tsv):
        self.tsv = tsv
    def make(self):
        return HTML.enclose('table', self.__make_row_header() + self.__make_body())
    def __make_row_header(self):
        html = ''
        for ri in range(self.tsv.RowHeader.Length):
            tr = ''
            for ci in range(len(self.tsv.RowHeader.SpanLenMap[ri])):
                if self.tsv.RowHeader.SpanLenMap[ri][ci][0] < 1 and self.tsv.RowHeader.SpanLenMap[ri][ci][1] < 1: continue
                tr += HTML.enclose('th', self.tsv.Map[ri][ci], self.__make_attr(self.tsv.RowHeader.SpanLenMap, ri, ci))
            html += HTML.enclose('tr', tr)
        return html
    def __make_body(self):
        html = ''
        for ri in range(len(self.tsv.ColHeader.SpanLenMap)):
            tr = ''
            for chi in range(self.tsv.ColHeader.Length):
                if self.tsv.ColHeader.SpanLenMap[ri][chi][0] < 1 and self.tsv.ColHeader.SpanLenMap[ri][chi][1] < 1: continue
                tr += HTML.enclose('th', self.tsv.Map[ri+self.tsv.RowHeader.Length][chi], self.__make_attr(self.tsv.ColHeader.SpanLenMap, ri, chi))
            for cdi in range(self.tsv.ColHeader.Length, len(self.tsv.Map)):
                tr += HTML.enclose('td', self.tsv.Map[ri+self.tsv.RowHeader.Length][cdi])
            html += HTML.enclose('tr', tr)
        return html
    def __make_attr(self, spanLenMap, ri, ci):
        attrs = {}
        if 1 < spanLenMap[ri][ci][0]: attrs['rowspan'] = spanLenMap[ri][ci][0]
        if 1 < spanLenMap[ri][ci][1]: attrs['colspan'] = spanLenMap[ri][ci][1]
        return attrs

class HTML:
    @staticmethod
    def enclose(element, text='', attrs={}):
        return '<' + element + HTML.attrs(attrs) + '>' + text + '</' + element + '>'
    @staticmethod
    def attrs(attrs):
        result = ''
        for key in attrs.keys():
            result += ' {}="{}"'.format(key, attrs[key])
        return result

if __name__ == '__main__':
    print(CLI().parse())
