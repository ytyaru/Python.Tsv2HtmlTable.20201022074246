#!/usr/bin/env python3
# coding: utf8
import argparse
import csv
import sys
import numpy
import copy
from abc import ABCMeta, abstractmethod

class CLI:
    def __init__(self): pass
    def parse(self):
#        self.__stdin = [line.rstrip('\n') for line in sys.stdin.readlines()]
#        print(self.__stdin)
        parser = argparse.ArgumentParser(description='TSVをHTMLのtableタグに変換する。')
        parser.add_argument('-H', '--header', default='a', help='ヘッダ形式')
        parser.add_argument('-r', '--row', default='t', choices=['t', 'top', 'b', 'bottom', 'B', 'both'], help='行ヘッダの表示位置')
        parser.add_argument('-c', '--column', default='l', choices=['l', 'left', 'r', 'right', 'B', 'both'], help='列ヘッダの表示位置')
        parser.add_argument('-m', '--merge', action='store_false', help='セル結合しない。')
        self.__args = parser.parse_args()

        self.__stdin = [line.rstrip('\n') for line in sys.stdin.readlines()]
        
        pos = self.__getHeaderPos()
        tsv = self.__getTsv()
        tsv.parse(self.__stdin, **pos)
#        print(tsv.ColHeader.Length)
#        return ToTable(tsv).make()
        return ToTable(tsv, **pos).make()
    def __getTsv(self):
        if self.__args.header.lower() in ['a','auto','r','row','m','matrix']:
            return TSV()
        elif self.__args.header.lower() in ['c','col','column']:
            return TSV(hasRowHeader=False)
        else: return TSV()
    def __getHeaderPos(self):
        pos = {}
        if   self.__args.row in ['t','top']: pos['row_header_pos'] = 'top'
        elif self.__args.row in ['b','bottom']: pos['row_header_pos'] = 'bottom'
        elif self.__args.row in ['B','both']: pos['row_header_pos'] = 'both'
        else: pos['row_header_pos'] = 'top'
        if   self.__args.column in ['l','left']: pos['col_header_pos'] = 'left'
        elif self.__args.column in ['r','right']: pos['col_header_pos'] = 'right'
        elif self.__args.column in ['B','both']: pos['col_header_pos'] = 'both'
        else: pos['col_header_pos'] = 'left'
        return pos


class TSV:
    def __init__(self, hasRowHeader=True):
        self.__textMap = []
        self.__textLenMap = []
        self.__hasRowHeader = hasRowHeader
    def parse(self, tsv, row_header_pos, col_header_pos):
        self.__textMap.clear()
        self.__textLenMap.clear()
        for cols in csv.reader(tsv, delimiter='\t'):
            self.__textMap.append([ col for col in cols ])
            self.__textLenMap.append([ len(col) for col in cols ])
        self.__make_reverseMap()
#        print('textMap')
#        print(self.__textMap)
#        print('textLenMap')
#        print(self.__textLenMap)
        self.__row_header = RowHeader(self.__textMap, self.__textLenMap, self.__hasRowHeader)
        self.__col_header = ColumnHeader(self.__textLenMap, self.__row_header.Length)
        self.__mat_header = MatrixHeader(self.__textLenMap, 
                                         row_header_pos, 
                                         col_header_pos, 
                                         self.__row_header.Length, 
                                         self.__col_header.Length)
    def __make_reverseMap(self):
        rev = reversed(self.Map)
        for ri in range(len(self.Map)):
            for ci in range(len(self.Map[ri])):
                if 0 == len(self.Map[ri][ci]):
                    for R in range(ri, len(self.Map)):
                        if not 0 == len(self.Map[ri][ci]):
                            rev[ri][ci] = self.Map[R][ci]
                            rev[R][ci] = self.Map[ri][ci]
        self.__reversed_row_header_map = rev
    @property
    def Map(self): return self.__textMap
    @property
    def ReversedRowHeaderMap(self): return self.__reversed_row_header_map
    @property
    def LenMap(self): return self.__textLenMap
    @property
    def RowHeader(self): return self.__row_header
    @property
    def ColHeader(self): return self.__col_header
    @property
    def MatrixHeader(self): return self.__mat_header

class MatrixHeader:
    def __init__(self, textLenMap, row_header_pos, col_header_pos, row_len, col_len):
        self.__row_pos = row_header_pos
        self.__col_pos = col_header_pos
        if row_len < 1 or col_len < 1: self.__size = (0,0)
        else: self.__size = self.__getSize(textLenMap)
        self.__setPos()
    def __getSize(self, textLenMap):
        rs = Merger.getRowZeroLen(textLenMap, 0, 0)
        cs = Merger.getColZeroLen(textLenMap, 0, 0)
        return (rs, cs)
    def __setPos(self):
        self.__pos = numpy.full((2,2), False)
        if self.__row_pos in ['top', 'both'] and self.__col_pos in ['left', 'both']:
            self.__pos[0][0] = True
        if self.__row_pos in ['top', 'both'] and self.__col_pos in ['right', 'both']:
            self.__pos[0][1] = True
        if self.__row_pos in ['bottom', 'both'] and self.__col_pos in ['left', 'both']:
            self.__pos[1][0] = True
        if self.__row_pos in ['bottom', 'both'] and self.__col_pos in ['right', 'both']:
            self.__pos[1][1] = True
    @property
    def Size(self): return self.__size
    @property
    def Pos(self): return self.__pos

class RowHeader:
    def __init__(self, textMap, textLenMap, hasRowHeader=True):
        if hasRowHeader:
            self.__len = self.__inferLength(textLenMap)
#            print(self.__len)
            self.__calcSpanMap(textLenMap)
            self.__make_textMap(textMap)
            self.__make_rev_textMap()
            self.__make_rev_spanLenMap()
        else:
            self.__len = 0
            self.__spanLenMap = []
            self.__textMap = []
            self.__rev_textMap = []
            self.__rev_spanLenMap = []
    @property
    def Length(self): return self.__len
    @property
    def SpanLenMap(self): return self.__spanLenMap
    @property
    def ReversedSpanLenMap(self): return self.__rev_spanLenMap
    @property
    def Map(self): return self.__textMap
    @property
    def ReversedMap(self): return self.__rev_textMap
    def get_map(self, isReverse=False):
        if isReverse: return self.ReversedMap
        else: return self.Map
    def get_span_len_map(self, isReverse=False):
        if isReverse: return self.ReversedSpanLenMap
        else: return self.SpanLenMap
    def __inferLength(self, textLenMap):
        blank_len = 0
        for ci in range(len(textLenMap[0])):
            if 0 == textLenMap[0][ci]: blank_len += 1
            else: break
        self.__blank_len = blank_len
#        print('blank_len=', blank_len)
        is_exist_map = numpy.full(len(textLenMap[0])-blank_len, False)
#        print(is_exist_map)
        for ri, row in enumerate(textLenMap):
#            print(textLenMap[ri])
            for ci in range(blank_len, len(textLenMap[ri])):
                if not 0 == textLenMap[ri][ci]: is_exist_map[ci-blank_len] = True
#            print(ri, is_exist_map)
            if all(is_exist_map): return ri+1 if 0 < ri else 1
#        print(is_exist_map)
    def __calcSpanMap(self, textLenMap):
        self.__spanLenMap = []
        for ri in range(self.Length):
            self.__spanLenMap.append([])
#            for ci in range(self.__blank_len, len(textLenMap[ri])):
            for ci in range(len(textLenMap[ri])):
#                if ci < self.__blank_len: continue
                if 0 == textLenMap[ri][ci]: self.__spanLenMap[-1].append([0,0])
                else:
                    rs = Merger.getRowZeroLen(textLenMap, ri, ci)
                    cs = Merger.getColZeroLen(textLenMap, ri, ci)
                    self.__spanLenMap[-1].append([rs,cs])
                print(self.__spanLenMap[-1][-1], end=',')
            print()
        self.__removeMatrixHeader()
#        self.__LeftTopSpanLen(textLenMap)
        Merger.setColspanStopByRowspan(self.__spanLenMap)
        Merger.setRowspanStopByColspan(self.__spanLenMap)
        self.__CrossSpanHeader()
        Merger.setZeroRect(self.__spanLenMap)
        print()
        for ri in range(len(self.__spanLenMap)):
            print(*self.__spanLenMap[ri])

    def __removeMatrixHeader(self):
        for ri in range(self.Length):
            del self.__spanLenMap[ri][:self.__blank_len]
#            for ci in range(self.__blank_len):
#                self.__spanLenMap[ri].pop(ci)
        
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

    def __make_textMap(self, textMap):
        self.__textMap = []
        for ri in range(self.Length):
#        for ri in range(len(textMap)):
            self.__textMap.append([])
            for ci in range(self.__blank_len, len(textMap[ri])):
                self.__textMap[-1].append(textMap[ri][ci])

    def __make_rev_textMap(self):
#        rev = reversed(self.Map)
#        self.__rev_textMap = copy.deepcopy(self.__textMap)
#        self.__rev_textMap = reversed(self.Map)
        self.__rev_textMap = list(reversed(copy.deepcopy(self.Map)))
        for ri in range(len(self.__rev_textMap)):
            for ci in range(len(self.__rev_textMap[ri])):
                if '' == self.__rev_textMap[ri][ci]:
                    for R in range(ri, len(self.__rev_textMap)):
                        if not '' == self.__rev_textMap[R][ci]:
                            self.__rev_textMap[ri][ci] = self.__rev_textMap[R][ci]
                            self.__rev_textMap[R][ci] = ''
        print('-----------------')
        for r in self.__textMap:
            print(r)
        print('-----------------')
        for r in self.__rev_textMap:
            print(r)
        print('-----------------')
    def __make_rev_spanLenMap(self):
        self.__rev_spanLenMap = list(reversed(copy.deepcopy(self.SpanLenMap)))
        for ri in range(len(self.__rev_spanLenMap)):
            for ci in range(len(self.__rev_spanLenMap[ri])):
                if self.__rev_spanLenMap[ri][ci][0] < 1 and self.__rev_spanLenMap[ri][ci][1] < 1:
                    for R in range(ri, len(self.__rev_spanLenMap)):
#                        if not (self.__rev_spanLenMap[R][ci][0] < 1 and self.__rev_spanLenMap[R][ci][1] < 1):
                        if 1 < self.__rev_spanLenMap[R][ci][0] or 1 < self.__rev_spanLenMap[R][ci][1]:
#                            tmp = self.__rev_spanLenMap[ri][ci]
                            tmp = copy.deepcopy(self.__rev_spanLenMap[ri][ci])
                            self.__rev_spanLenMap[ri][ci] = self.__rev_spanLenMap[R][ci]
                            self.__rev_spanLenMap[R][ci] = tmp
#                            self.__rev_textMap[R][ci] = self.__rev_textMap[ri][ci]
        print('-----------------')
        for r in self.__spanLenMap:
            print(r)
        print('-----------------')
        for r in self.__rev_spanLenMap:
            print(r)

"""
    def __make_rev_textMap(self):
        rev = reversed(self.Map)
        for ri in range(len(self.Map)):
            for ci in range(len(self.Map[ri])):
                if 0 == len(self.Map[ri][ci]):
                    for R in range(ri, len(self.Map)):
                        if not 0 == len(self.Map[ri][ci]):
                            rev[ri][ci] = self.Map[R][ci]
                            rev[R][ci] = self.Map[ri][ci]
        self.__reversed_row_header_map = rev
"""

        

class ColumnHeader:
    def __init__(self, textLenMap, row_header_len):
        self.__row_header_len = row_header_len
        self.__len = self.__inferLength(textLenMap)
#        print('col_len=', self.__len)
        self.__calcSpanMap(textLenMap)
    @property
    def Length(self): return self.__len
    @property
    def SpanLenMap(self): return self.__spanLenMap
    def __inferLength(self, textLenMap):
        col_len = 0
        if 0 < self.__row_header_len:
            for ci, col in enumerate(textLenMap[0]):
                if 0 == col: col_len += 1
                else: break
            if 0 == self.__row_header_len and 0 == col_len: return 1
            else: return col_len
        else:
            is_exist_map = numpy.full(len(textLenMap)-self.__row_header_len, False)
            for ci in range(len(textLenMap[0])):
                for ri in range(self.__row_header_len, len(textLenMap)):
                    if not 0 == textLenMap[ri][ci]: is_exist_map[ri] = True
#                print(is_exist_map)
                if all(is_exist_map): return col_len+1
                col_len += 1

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
#                print(self.__spanLenMap[-1][-1], end=',')
#            print()
        Merger.setColspanStopByRowspan(self.__spanLenMap)
        Merger.setRowspanStopByColspan(self.__spanLenMap)
        self.__CrossSpanHeader()
        Merger.setZeroRect(self.__spanLenMap)
#        print()
#        for ri in range(len(self.__spanLenMap)):
#            print(*self.__spanLenMap[ri])

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
#                print(R, ci, len(spanLenMap))
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
#                    print(ri, ci, rs, cs, R,C, spanLenMap[R][C])
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
    def __init__(self, tsv, row_header_pos='top', col_header_pos='left'):
        self.tsv = tsv
        self.__col_header_pos = col_header_pos.lower()
        self.__row_header_pos = row_header_pos.lower()
        print(self.__row_header_pos,  self.__col_header_pos)
    def make(self):
        html = ''
        if self.__row_header_pos in ['top', 'both']: html += self.__make_row_header()
        html += self.__make_body()
        if self.__row_header_pos in ['bottom', 'both']: html += self.__make_row_header(isReverse=True)
        return HTML.enclose('table', html)
#        return HTML.enclose('table', self.__make_row_header() + self.__make_body())
    def __make_row_header(self, isReverse=False):
        row_header_tr_inners = []
        for ri in range(self.tsv.RowHeader.Length):
            row_header_tr_inners.append([])
            for ci in range(len(self.tsv.RowHeader.SpanLenMap[ri])):
#                if self.tsv.RowHeader.SpanLenMap[ri][ci][0] < 1 and self.tsv.RowHeader.SpanLenMap[ri][ci][1] < 1: continue
                if '' == self.tsv.RowHeader.get_map(isReverse)[ri][ci]: continue
                row_header_tr_inners[-1].append(
                    HTML.enclose('th', 
                                 self.tsv.RowHeader.get_map(isReverse)[ri][ci], 
                                 self.__make_attr(self.tsv.RowHeader.get_span_len_map(isReverse), ri, ci)))
#        if isReverse: row_header_tr_inners = list(reversed(row_header_tr_inners))
        self.__make_matrix_header(row_header_tr_inners)
        print(row_header_tr_inners)
        return ''.join([HTML.enclose('tr', ''.join(row_header_tr_inners[ri])) for ri in range(len(row_header_tr_inners))])

    """
    def __make_row_header(self, isReverse=False):
        row_header_tr_inners = []
#        for ri in range(self.tsv.RowHeader.Length):
        for ri in reversed(range(self.tsv.RowHeader.Length)) if isReverse else range(self.tsv.RowHeader.Length):
            row_header_tr_inners.append([])
            for ci in range(len(self.tsv.RowHeader.SpanLenMap[ri])):
                if self.tsv.RowHeader.SpanLenMap[ri][ci][0] < 1 and self.tsv.RowHeader.SpanLenMap[ri][ci][1] < 1: continue
                row_header_tr_inners[-1].append(
                    HTML.enclose('th', 
                                 self.tsv.Map[ri][ci+self.tsv.MatrixHeader.Size[1]], 
#                                 self.tsv.Map[self.__reverse_ri(ri, isReverse)][ci+self.tsv.MatrixHeader.Size[1]], 
#                                 self.tsv.Map[self.__not_reverse_ri(ri, isReverse)][ci+self.tsv.MatrixHeader.Size[1]], 
                                 self.__make_attr(self.tsv.RowHeader.SpanLenMap, self.__not_reverse_ri(ri, isReverse), ci)))
#                                 self.__make_attr(self.tsv.RowHeader.SpanLenMap, ri, ci)))
#        if isReverse: row_header_tr_inners = list(reversed(row_header_tr_inners))
#        self.__make_matrix_header(row_header_tr_inners)
        print(row_header_tr_inners)
        return ''.join([HTML.enclose('tr', ''.join(row_header_tr_inners[ri])) for ri in range(len(row_header_tr_inners))])
#        for ri in range(len(row_header_tr_inners)):
#            HTML.enclose('tr', ''.join(row_header_tr_inners[ri]))
    """
    def __not_reverse_ri(self, ri, isReverse=False):
        if isReverse: return self.tsv.RowHeader.Length - 1 - ri
        else: return ri

#    def __reverse_ri(self, ri, isReverse=False):
#        return ri
#        return self.tsv.RowHeader.Length - 1 - ri
#        if isReverse: return self.tsv.RowHeader.Length - 1 - ri
#        else: return ri
    def __make_matrix_header(self, row_header_tr_inners):
        print(self.tsv.MatrixHeader.Pos)
        matrix_header_th = HTML.enclose('th', '', {'rowspan': self.tsv.MatrixHeader.Size[0], 'colspan': self.tsv.MatrixHeader.Size[1]})
        if self.tsv.MatrixHeader.Pos[0][0]:
            row_header_tr_inners[0].insert(0, matrix_header_th)
        if self.tsv.MatrixHeader.Pos[0][1]:
            row_header_tr_inners[0].append(matrix_header_th)
        if self.tsv.MatrixHeader.Pos[1][0]:
            row_header_tr_inners[0].insert(0, matrix_header_th)
        if self.tsv.MatrixHeader.Pos[1][1]:
            row_header_tr_inners[0].append(matrix_header_th)




    def __make_body(self):
        html = ''
        for ri in range(len(self.tsv.ColHeader.SpanLenMap)):
            tr = ''
            if self.__col_header_pos in ['left', 'both']: tr += self.__make_body_th(ri)
#            for chi in range(self.tsv.ColHeader.Length):
#                if self.tsv.ColHeader.SpanLenMap[ri][chi][0] < 1 and self.tsv.ColHeader.SpanLenMap[ri][chi][1] < 1: continue
#                tr += HTML.enclose('th', self.tsv.Map[ri+self.tsv.RowHeader.Length][chi], self.__make_attr(self.tsv.ColHeader.SpanLenMap, ri, chi))
            for cdi in range(self.tsv.ColHeader.Length, len(self.tsv.Map[ri])):
                tr += HTML.enclose('td', self.tsv.Map[ri+self.tsv.RowHeader.Length][cdi])
            if self.__col_header_pos in ['right', 'both']: tr += self.__make_body_th(ri, isReverse=True)
            html += HTML.enclose('tr', tr)
        return html
    def __make_body_th(self, ri, isReverse=False):
        tr = ''
        for chi in reversed(range(self.tsv.ColHeader.Length)) if isReverse else range(self.tsv.ColHeader.Length):
#        for ci in reversed(range(len(self.tsv.RowHeader.SpanLenMap[ri]))) if isReverse else range(len(self.tsv.RowHeader.SpanLenMap[ri])):
#        for chi in range(self.tsv.ColHeader.Length):
            if self.tsv.ColHeader.SpanLenMap[ri][chi][0] < 1 and self.tsv.ColHeader.SpanLenMap[ri][chi][1] < 1: continue
            tr += HTML.enclose('th', self.tsv.Map[ri+self.tsv.RowHeader.Length][chi], self.__make_attr(self.tsv.ColHeader.SpanLenMap, ri, chi))
        return tr
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
