# coding=utf-8
"""
用Python实现一个Rossenblatt神经元感知器percetron类，其中fit方法从数据中学习，而predict方法进行预测
"""
import numpy as np

class perceptron(object):
    """
    Percetron classifier.
    Parameters
    -----------
    eta :float 学习率
        Learning rate(between 0.0 and 1.0)
    n_iter:int 迭代次数
        Passes over the training dataset.
    Attributes:
    ---------
    w_:1d-array
        weights after fitting.训练后的权重数组，是一个一维数组，如果有3个特征（参数），则有3+1=4个值
    errors_:list
        Number of misclassifications in every epoch.每一轮迭代时错误分类的数量
    """
    def __init__(self,eta=0.01,n_iter=10):
        self.eta=eta
        self.n_iter=n_iter

    def fit(self,X,Y):
        """Fit training data:
        Parameters
        -----------
        X: {array-like},shape=[n_samples,n_features]
            Training vectors,where n_samles is the number of samples and
        n_feature is the number of features

        y: array-like,shape=[n_samples]
            target values.
        Returns
        ------
        self:object
        """
        self.w_=np.zeros(1+X.shape[1])
        self.errors_=[]

        for _ in range(self.n_iter):
            errors =0
            for xi,target in zip(X,Y):
                update=self.eta * (target -self.predict(xi))
                self.w_[1:]+= update*xi
                self.w_[0]+=update
                errors+=int(update != 0.0)
            self.errors_.append(errors)
        return self

    def net_input(self,X):
        """Calculate net input对于一个神经元节点，总是将它的值与权重值相乘"""
        return  np.dot(X,self.w_[1:]+self.w_[0])

    def predict(self,X):
        """Return class label after unit step"""
        return np.where(self.net_input(X)>=0.0,1,-1)