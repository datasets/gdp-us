import urllib
import csv
import dataconverters.xls  as xls

levels = 'http://www.bea.gov/national/xls/gdplev.xls'
change = 'http://www.bea.gov/national/xls/gdpchg.xls'

def process():
    # headers atm are [ 'Date', '... current', '... chained' ]
    yearl, quarterl = extract(levels)
    yearc, quarterc = extract(change)
    year = combine(yearl, yearc)
    quarter = combine(quarterl, quarterc)
    headers = [ 'date', 'level-current', 'level-chained', 'change-current', 'change-chained' ]
    writedata('year', headers, year)
    writedata('quarter', headers, quarter)
    
def combine(levels, change):
    out = zip(*levels)
    out = out + zip(*change)[1:]
    out = [ list(r) for r in zip(*out) ]
    return out

def extract(url):
    fo = urllib.urlopen(url)
    records, metadata = xls.parse(fo)
    def rerowify(dict_):
        return [ dict_[f['id']] for f in metadata['fields'] ]
    rows = [ rerowify(r) for r in records ]
    del rows[:8]
    transposed = zip(*rows)
    annual = zip(*transposed[:3])
    annual = [ [int(r[0])] + list(r[1:]) for r in annual if r[0] ]
    quarterly = zip(*transposed[4:7])
    # 1947q1 etc
    def fixquarters(date):
        mapping = [
            ['q1', '-01-01'],
            ['q2', '-04-01'],
            ['q3', '-07-01'],
            ['q4', '-10-01']
        ]
        for x in mapping:
            date = date.replace(x[0], x[1])
        return str(date)
    quarterly = [ [fixquarters(r[0])] + list(r[1:]) for r in quarterly ]
    return (annual, quarterly)

def writedata(name, headers, data):
    fo = open('%s.csv' % name, 'w')
    writer = csv.writer(fo)
    writer.writerow(headers)
    writer.writerows(data)


if __name__ == '__main__':
    process()

