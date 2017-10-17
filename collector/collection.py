import csv

class Collection:
    def __init__(self):
        self.rows = []
        self.colnames = []
        self.index = {}
    
    def readCsv(self, fname):
        with open(fname, "r") as f_obj:
            reader = csv.DictReader(f_obj)
            self.colnames = reader.fieldnames
            for line in reader:
                self.rows.append(line)

    def buildIndex(self):
        rownum = 0
        rownums = set()
        for row in self.rows:
            for k, v in row.items():
                words = v.lower().split()
                for word in words:         
                    if word in self.index:
                        rownums = self.index[word]
                        rownums.append(rownum)
                    else:
                        rownums = [rownum]
                    self.index[word] = rownums
            rownum = rownum + 1

    def displayIndex(self):
        for k, v in self.index.items():
            print(k,v)

    def find(self, query):
        # Fast find of all terms but each word must match exactly
        # Although not case-sensitive, plural form not same as singular
        results = set()
        words = query.lower().split()
        for word in words:
            if word in self.index:
                rownums = self.index[word]
                if len(results) == 0:
                    results.update(rownums)
                else:
                    results = results.intersection(rownums)
            else:
                # stop when any word from query is not in index - each word must be found
                break
        return list(results)

    def displayHeader(self):
        print('Id      Country          Catalog   Title                           Album')
        print('------  ---------------  --------  ------------------------------  ---------------')

    def displayRow(self, row):
        print('{:6}'.format(row['Id'])),
        print(' {:15}'.format(row['Country'])),
        print(' {:8}'.format(row['Catalog'])),
        print(' {:30}'.format(row['Title'])),
        print('{:15}'.format(row['Album']))       
            
    def displayResults(self, results):
        if len(results) == 0:
            print("None")
        else:
            self.displayHeader()
            for rownum in results:
                self.displayRow(self.rows[rownum])

    def displayRows(self):
        self.displayHeader()
        for row in self.rows:
            self.displayRow(row)

    def writeCsv(self, fname):
        with open(fname, "w") as f_obj:
            writer = csv.DictWriter(f_obj, fieldnames=self.colnames)
            writer.writeheader()
            for row in self.rows:
                writer.writerow(row)

    def getRows(self):
        return self.rows

    def getColnames(self):
        return self.colnames

 