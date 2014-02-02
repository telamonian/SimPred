import numpy as np
import blpapi, math, datetime
from sklearn import svm
from sp100 import sp100
from sp500 import sp500
from djia import djia
dataset = sp500

class tickerDatum(object):
    def __init__(self, VOLATILITY_90D=None, PX_TO_SALES_RATIO=None, PE_RATIO=None, PCT_INSIDER_SHARES_OUT=None, PX_TO_BOOK_RATIO=None):
        self.VOLATILITY_90D = VOLATILITY_90D
        self.PX_TO_SALES_RATIO = PX_TO_SALES_RATIO
        self.PE_RATIO = PE_RATIO 
        self.PCT_INSIDER_SHARES_OUT = PCT_INSIDER_SHARES_OUT
        self.PX_TO_BOOK_RATIO = PX_TO_BOOK_RATIO
        
    def setDays(self, days):
        self.days = days
        
    def setMonths(self, months):
        self.months = months
        
    def truth(self):
        return (self.days[0] - self.days[1])/self.days[1]
    
    def oneDay(self):
        return (self.days[1] - self.days[2])/self.days[2]
    
    def threeDay(self):
        return (self.days[1] - self.days[4])/self.days[4]
    
    def fiveDay(self):
        return (self.days[1] - self.days[6])/self.days[6]
    
    def oneMonth(self):
        return (self.months[0] - self.months[1])/self.months[1]
    
    def sixMonth(self):
        return (self.months[0] - self.months[6])/self.months[6]
    
    def volatility_90d(self):
        return self.VOLATILITY_90D
    
    def px_to_sales_ratio(self):
        return self.PX_TO_SALES_RATIO
    
    def pe_ratio(self):
        return self.PE_RATIO
    
    def pct_insider_shares_out(self):
        return self.PCT_INSIDER_SHARES_OUT
    
    def px_to_book_ratio(self):
        return self.PX_TO_BOOK_RATIO
    
    features = (truth, oneDay, threeDay, fiveDay, oneMonth, sixMonth, volatility_90d, px_to_sales_ratio, pe_ratio, pct_insider_shares_out, px_to_book_ratio)
    featureNames = ('truth', 'oneDay', 'threeDay', 'fiveDay', 'oneMonth', 'sixMonth', 'volatility_90d', 'px_to_sales_ratio', 'pe_ratio', 'pct_insider_shares_out', 'px_to_book_ratio')

class fetchBlp(object):
    tickerSets=[sp100,sp500,djia]
    def __init__(self, tickersSet):
        self.tickers = self.__class__.tickerSets[tickersSet-1]
        self.columnNames = tickerDatum.featureNames
        self.tickerData = {}
        self.go()
        self.output()
    
    def go(self):
        self.fetch()
        self.mat = np.zeros((len(self.tickers), len(tickerDatum.features)))
        for i,ticker in enumerate(self.tickers):
            for j,feature in enumerate(tickerDatum.features):
                self.mat[i,j] = feature(self.tickerData[ticker])
                
    def output(self):
        columnNames = np.array(self.columnNames,dtype='|S20')
        rowNames = np.array(self.tickers,dtype='|S20')
        np.savez('simpredRawData.npz', columnNames=columnNames, rowNames=rowNames, data=self.mat)
    
    def fetch(self):
        self.fetchDays()
        self.fetchMonths()
        self.fetchFields()
        
    def fetchDays(self):
        past = datetime.date.today() + datetime.timedelta(-60)
        today = datetime.date.today()
        start = '%04d%02d%02d'  % (past.year, past.month, past.day)
        end = '%04d%02d%02d' % (today.year, today.month, today.day)
        self.fetchTimePeriod(periodicity='DAILY', start=start, end=end)
        
    def fetchMonths(self):
        past = datetime.date.today()
        today = datetime.date.today()
        start = '%04d%02d%02d'  % (past.year - 1, past.month, past.day)
        end = '%04d%02d%02d' % (today.year, today.month, today.day)
        self.fetchTimePeriod(periodicity='MONTHLY', start=start, end=end)
    
    def fetchTimePeriod(self, periodicity, start, end):
        #temporary dictionary holding all stock tickers with open close pairs stored
        #in a list going from past to present
        #each day has [open, close]

        sessionOptions = blpapi.SessionOptions()
        sessionOptions.setServerHost("10.8.8.1")
        sessionOptions.setServerPort(8194)
    
        # Create a Session
        session = blpapi.Session(sessionOptions)
    
        # Start a Session
        if not session.start():
            print "Failed to start session. Failed to load test data."
            return
    
        if not session.openService("//blp/refdata"):
            print "Failed to open //blp/refdata. Failed to load test data."
            return
    
        refDataService = session.getService("//blp/refdata")
        request = refDataService.createRequest("HistoricalDataRequest")
    
        # append securities to request
#         for ticker in self.tickers:
#             request.append("securities","{0} US Equity".format(ticker))
    
        # append fields to request
        fieldTypes = ('PX_LAST', 'OPEN')
        for fieldType in fieldTypes:
            request.append("fields", fieldType)
        
        for ticker in self.tickers:
            request.getElement("securities").appendValue("%s US Equity" % (ticker))
        request.set("periodicityAdjustment", "ACTUAL")
        request.set("periodicitySelection", periodicity)
        request.set("startDate", start)
        request.set("endDate", end)
        request.set("maxDataPoints", 60)  
 
        #print "Sending Request:", request
        session.sendRequest(request)
    
        try:
            # Process received events
            while(True):
                # We provide timeout to give the chance to Ctrl+C handling:
                ev = session.nextEvent(500)
                if periodicity=='DAILY':
                    for msg in ev:
                        print msg
                        if msg.messageType() == blpapi.Name('HistoricalDataResponse'):
                            fieldDataArray = msg.getElement('securityData').getElement('fieldData')
                            #recover ticker for storage purposes
                            ctick = msg.getElement('securityData').getElementAsString('security').split()[0]
                            fieldData = fieldDataArray.getValueAsElement(1)
                            self.tickerData[ctick] = tickerDatum()
                            tmp = []
                            for i in range(fieldDataArray.numValues()):
                                fieldData = fieldDataArray.getValueAsElement(i)
                                tmp.append(fieldData.getElementAsFloat("PX_LAST"))
                            self.tickerData[ctick].setDays(tmp)
                    # Response completly received, so we could exit
                    if ev.eventType() == blpapi.Event.RESPONSE:
                        break
                elif periodicity=='MONTHLY':
                    for msg in ev:
                        #print msg
                        if msg.messageType() == blpapi.Name('HistoricalDataResponse'):
                            fieldDataArray = msg.getElement('securityData').getElement('fieldData')
                            #recover ticker for storage purposes
                            ctick = msg.getElement('securityData').getElementAsString('security').split()[0]
                            tmp = []
                            for i in range(fieldDataArray.numValues()):
                                fieldData = fieldDataArray.getValueAsElement(i)
                                tmp.append(fieldData.getElementAsFloat("PX_LAST"))
                            self.tickerData[ctick].setMonths(tmp)
                    # Response completly received, so we could exit
                    if ev.eventType() == blpapi.Event.RESPONSE:
                        break
                else:
                    raise
        finally:
            # Stop the session
            session.stop()
        return
    
    def fetchFields(self):
        sessionOptions = blpapi.SessionOptions()
        sessionOptions.setServerHost("10.8.8.1")
        sessionOptions.setServerPort(8194)
    
        # Create a Session
        session = blpapi.Session(sessionOptions)
    
        # Start a Session
        if not session.start():
            print "Failed to start session. Failed to load test data."
            return
    
        if not session.openService("//blp/refdata"):
            print "Failed to open //blp/refdata. Failed to load test data."
            return
    
        refDataService = session.getService("//blp/refdata")
        request = refDataService.createRequest("ReferenceDataRequest")
        
        for ticker in self.tickers:
            request.getElement("securities").appendValue("%s US Equity" % (ticker))
        
        fieldTypes = ('VOLATILITY_90D', 'PX_TO_SALES_RATIO', 'PE_RATIO', 'PCT_INSIDER_SHARES_OUT', 'PX_TO_BOOK_RATIO')
        for fieldType in fieldTypes:
            request.append("fields", fieldType)
        
        print "Sending Request:", request
        session.sendRequest(request)
        
        try:
            # Process received events
            while(True):
                # We provide timeout to give the chance to Ctrl+C handling:
                ev = session.nextEvent(500)
                for msg in ev:
                    print msg
                    if msg.messageType() == blpapi.Name('ReferenceDataResponse'):
                        securityDataArray = msg.getElement('securityData')
                        for securityData in (securityDataArray.getValueAsElement(i) for i in range(securityDataArray.numValues())):
                            #recover ticker for storage purposes
                            ctick = securityData.getElementAsString('security').split()[0]
                            fieldData = securityData.getElement('fieldData')
                            try:
                                self.tickerData[ctick].PX_TO_SALES_RATIO=fieldData.getElementAsFloat("PX_TO_SALES_RATIO")
                                self.tickerData[ctick].VOLATILITY_90D=fieldData.getElementAsFloat("VOLATILITY_90D")
                                self.tickerData[ctick].PE_RATIO=fieldData.getElementAsFloat("PE_RATIO")
                                self.tickerData[ctick].PCT_INSIDER_SHARES_OUT=fieldData.getElementAsFloat("PCT_INSIDER_SHARES_OUT")
                                self.tickerData[ctick].PX_TO_BOOK_RATIO=fieldData.getElementAsFloat("PX_TO_BOOK_RATIO")
                            except blpapi.exception.NotFoundException:
                                self.tickers.pop(self.tickers.index(ctick))
                                del self.tickerData[ctick]
                # Response completly received, so we could exit
                if ev.eventType() == blpapi.Event.RESPONSE:
                    break
        finally:
            # Stop the session
            session.stop()
        return
    
###main testing###

if __name__ == "__main__":
    myTest = fetchBlp()
    print myTest.columnNames
    print myTest.mat
