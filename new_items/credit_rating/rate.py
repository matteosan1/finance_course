import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dropout, Dense
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import to_categorical

from imblearn.over_sampling import SMOTE

df = pd.read_csv("corporate_rating.csv")
df.drop(columns=['Name', 'Symbol', 'Rating Agency Name', 'Date', 'Sector'], inplace=True)

mapping = {'A':1, 'BBB':2, 'AA':0, 'BB':3, 'B':4, 'CCC':5, 'D':5, 'CC':5, 'AAA':0, 'C':5}
df['NumRating'] = df["Rating"].apply(lambda x: mapping[x])

def plots(X):
    for c in X.columns:
        for i in range(6):
            plt.hist(X.loc[X['NumRating']==i, c])#, bins=50, histtype="stepfilled")
        plt.show()

X = df[['currentRatio', 'quickRatio', 'cashRatio', 'daysOfSalesOutstanding',
        'netProfitMargin', 'pretaxProfitMargin', 'grossProfitMargin',
        'operatingProfitMargin', 'returnOnAssets', 'returnOnCapitalEmployed',
        'returnOnEquity', 'assetTurnover', 'fixedAssetTurnover',
        'debtEquityRatio', 'debtRatio', 'effectiveTaxRate',
        'freeCashFlowOperatingCashFlowRatio', 'freeCashFlowPerShare',
        'cashPerShare', 'companyEquityMultiplier', 'ebitPerRevenue',
        'enterpriseValueMultiple', 'operatingCashFlowPerShare',
        'operatingCashFlowSalesRatio', 'payablesTurnover', 'NumRating']]

corr_mat = X.corr()
drop_list = {}
for i in range(len(corr_mat.columns)):
    for j in range(i):
        if abs(corr_mat.iloc[i, j]) >= 0.95:
            if corr_mat.columns[j] not in drop_list:
                drop_list.setdefault(corr_mat.columns[j], []) \
                         .append(corr_mat.columns[i])

#for d in drop_list:
#    print (d)

X = X.drop(drop_list, axis=1)
Y = df['NumRating']

oversample = SMOTE()
X, Y = oversample.fit_resample(X, Y)

plots(X)
quit()

scaler = StandardScaler()
X_sm = scaler.fit_transform(X)

X_train, X_test, Y_train, Y_test = train_test_split(X_sm, Y, test_size=0.2)

model = Sequential()
model.add(Dense(50, input_dim=len(X.columns), activation='tanh'))
#model.add(Dropout(0.3))
model.add(Dense(40, activation='tanh'))
model.add(Dense(15, activation='tanh'))
model.add(Dropout(0.3))
model.add(Dense(6, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
early_stop = EarlyStopping(monitor='val_loss', mode='min',
                           verbose=1,
                           patience=50)

history = model.fit(x=X_train, y=to_categorical(Y_train),
                    validation_data=(X_test, to_categorical(Y_test)),
                    epochs=2000, batch_size=10, verbose=1)

model.save("credit_rating_relu")

print (model.evaluate(X_train, to_categorical(Y_train)))
print (model.evaluate(X_test, to_categorical(Y_test)))

plt.plot(history.history['loss'], color='red')
plt.plot(history.history['accuracy'], color='blue')
plt.plot(history.history['val_loss'], linestyle=":", color='red')
plt.plot(history.history['val_accuracy'], linestyle=":", color='blue')

plt.show()

ann_predictions = np.argmax(model.predict(X_sm), axis=1)
cm = confusion_matrix(Y, ann_predictions)
cmd_obj = ConfusionMatrixDisplay(cm)#, display_labels=['No Bankruptcy', 'Bankruptcy'])
cmd_obj.plot()
cmd_obj.ax_.set(title='', xlabel='Predicted', ylabel='Actual')
plt.show()
