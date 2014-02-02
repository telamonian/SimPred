from sklearn import svm,tree
from sklearn.metrics import classification_report
import numpy, math

class sixModels:
    def __init__(self,indata,incutoff,inmethod,tokeep):
        self.data = indata
        self.tokeep = tokeep
        self.test_data = []
        self.train_data = []
        self.predict_data = []
        self.cutoff = incutoff
        self.method = inmethod
        self.model = None
        self.clr = None
        self.pred_proba = None
        self.pred = None
        self.run()

    def set_state(self,pchange):
        state = 0
        if pchange > self.cutoff:
            state = 1
        return state

    def run(self):
        newarr = numpy.array([self.data[:,self.tokeep[0]]]).T
        for i in range(1,len(self.tokeep)):
            newarr = numpy.hstack((newarr,numpy.array([self.data[:,self.tokeep[i]]]).T))
        self.data = newarr
        for i in range(len(self.data)):
            self.data[i,0] = self.set_state(self.data[i,0])
        self.predict_data = self.data[0,:]
        self.data = self.data[1:,:]
        split_length = int(math.ceil(0.8*len(self.data)))
        self.train_data =  self.data[:split_length,:]
        self.test_data = self.data[split_length:,:]

        y = self.train_data[:,0]
        X = self.train_data[:,1:]
        self.model = self.method.fit(X,y)
        
        y = self.test_data[:,0]
        X = self.test_data[:,1:]
        try:
            self.pred_proba = self.model.predict_proba(X)
            self.pred = self.model.predict(X)
        except TypeError:
            self.pred = self.model.predict(X)

        self.clr = classification_report(y,self.pred,target_names=['%change<={0}'.format(self.cutoff),'%change>{0}'.format(self.cutoff)])
        
        y = self.predict_data[0]
        X = self.predict_data[1:]
        try:
            self.pred_proba = self.model.predict_proba(X)
            self.pred = self.model.predict(X)
        except TypeError:
            self.pred = self.model.predict(X)

        with open('pred_p{0}.txt'.format(int(100*self.cutoff)),'w') as f:
            if self.pred_proba != None:
                f.write(str(self.pred_proba))
            else:
                f.write(str(self.pred))

        with open('clr_p{0}.txt'.format(int(100*self.cutoff)),'w') as f:
            f.write(str(self.clr))
        return

if __name__ == "__main__":
    #different classifiers: tree.DecisionTreeClassifier(), svm.SVC,
    ta=numpy.load('simpredRawData.npz')['data']
    #ta = numpy.array([[.041,-.01,-.03,-.02,-.02,-.03],[.041,-.01,-.03,-.02,-.02,-.03],[.041,-.01,-.03,-.02,-.02,-.03],[-.1,.01,.03,.02,-.02,-.03],[.041,-.01,-.03,-.02,-.02,-.03],[-.21,.21,.23,.22,-.22,-.23]])
    myTest1 = sixModels(ta,-0.02,svm.SVC(probability=True),[0,1,2,3,4])
    myTest2 = sixModels(ta,-0.01,svm.SVC(probability=True),[0,1,2,3,4])
    myTest4 = sixModels(ta,0.00,svm.SVC(probability=True),[0,1,2,3,4])
    myTest6 = sixModels(ta,0.01,svm.SVC(probability=True),[0,1,2,3,4])
    myTest7 = sixModels(ta,0.02,svm.SVC(probability=True),[0,1,2,3,4])
