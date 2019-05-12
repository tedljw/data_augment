import pandas as pd
import sys

#import xlrd
#import xlwt
#import sys
#from datetime import date,datetime

def xlsx_to_csv_pd(file_src, file_dest):
    data_xls = pd.read_excel(file_src, index_col=0)
    data_xls.to_csv(file_dest, encoding='utf-8')

'''
def csv_to_xlsx_pd():
    csv = pd.read_csv('1.csv', encoding='utf-8')
    csv.to_excel('1.xlsx', sheet_name='data')

def read_excel(filename):

  workbook = xlrd.open_workbook(filename)
  sheet2 = workbook.sheet_by_index(0)

  for row in xrange(0, sheet2.nrows):
    rows = sheet2.row_values(row)
    def _tostr(cell):
      if type(u'') == type(cell):
        return "\"%s\"" % cell.encode('utf8')
      else:
        return "\"%s\"" % str(cell)

    print (','.join([_tostr(cell) for cell in rows ]))
'''

if len(sys.argv) != 2:
    print("只能输入1个参数\n请输入需要转换的文件名,如python transform.py a.xlsx")
else :
    strtmp = sys.argv[1]
    outfile = strtmp[:strtmp.find('.')]
    outfile = outfile + '.csv'
    xlsx_to_csv_pd(strtmp, outfile)


