#! /usr/bin/env python

class Table(object):
    def __init__(self, *headings):
        self.data = list()
        self.data.append([str(heading) for heading in headings])
  
    def add(self, *columns):
        self.data.append(list(map(str, columns)))
  
    def close(self):
        # figure out the max width of each column
        widths = list()
        for col_num in range(len(self.data[0])):
            widths.append(max(len(self.data[row_num][col_num]) for row_num in range(len(self.data))))

        for row_num in range(len(self.data)):
            print('  '.join([self.data[row_num][col_num].ljust(widths[col_num]) for col_num in range(len(self.data[0]))]))

table = Table('1', 'two', 3)
table.add('row 1, cell 1', 'row 1, cell 2', 1.3) 
table.close()
