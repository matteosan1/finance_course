from finnn import FinNN
from numpy import arange, array
from sklearn.metrics import mean_squared_error
from matplotlib import pyplot as plt

x = array([i for i in arange(-50, 50, 0.01)])

y = array([i**2.0 for i in x])
print("Distribution of original data ", x.min(), x.max(), y.min(), y.max())

trainer = FinNN()
trainer.setData(x, y)
trainer.normalize()

print("The same data after the normalization ", trainer.x.min(), 
      trainer.x.max(), trainer.y.min(), trainer.y.max())

trainer.addInputLayer(1, 5, 'sigmoid')
trainer.addHiddenLayer(5, 'sigmoid')
trainer.addHiddenLayer(2, 'sigmoid')
trainer.addOutputLayer(1)

trainer.compileModel('mae', 'adam')
trainer.fit(150, 20)


trainer.fullPrediction()
trainer.reverseNormalization()
print('MSE: %.3f' % mean_squared_error(trainer.y, trainer.predictions))

plt.figure(figsize=(8,5))
plt.scatter(trainer.x, trainer.y, label='Actual')
plt.scatter(trainer.x, trainer.predictions, label='Predicted', s=4)
plt.title('Input (x) versus Output (y)')
plt.xlabel('Input Variable (x)')
plt.ylabel('Output Variable (y)')
plt.legend()
plt.show()
