from finnn import FinNN

from numpy import arange, asarray

# define the dataset
x = asarray([i for i in arange(-50, 50, 0.1)])
print (type(x))
y = asarray([i**2.0 for i in x])
print("Distribution of original data ", x.min(), x.max(), y.min(), y.max())

trainer = FinNN(x, y)
trainer.normalize()

trainer.addInputLayer(1, 10, 'sigmoid')
trainer.addHiddenLayer(10, 'sigmoid')
trainer.addOutputLayer(1)

trainer.compileModel('mse', 'adam')
trainer.fit(500, 10, 0)

trainer.predict()
trainer.reverseNormalization()

trainer.plot()
