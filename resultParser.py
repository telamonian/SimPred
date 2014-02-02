'''
Created on Feb 2, 2014

@author: tel
'''
class resultParser(object):
    def __init__(self, fname='simpredResults.txt'):
        f = open(fname, 'r')
        lines = f.readlines()
        for line in lines:
            if line[0]=='$':
                break
            else:
                tokens = line.split()
                try:
                    if tokens[2]=='0':
                        self.response = 1 - float(tokens[7])
                except IndexError:
                    pass

if __name__=='__main__':
    r = resultParser()
    print r.response