import pandas as pd
from finmarkets import generate_dates
from datetime import date
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt

from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
#from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler

start_date = date(2017, 10, 1)
periods = 9 
dates = generate_dates(start_date, "24m", "3m")

data = pd.read_pickle("./bond_issuer_data.pkl")

current_date_rating = dict(zip(data.index + '_' + data['Date'].astype(str), data['Rating']))

rating_future = data[['Date']].reset_index().apply(
    lambda x : current_date_rating.get(x[0] + '_' + str(x[1] + relativedelta(months=+3)), ''), axis = 1)

data.insert(data.columns.tolist().index('Rating') + 1, 'Rating Future', rating_future.values)


current_date_spread = dict(zip(data.index + '_' + data['Date'].astype(str), data['OAS']))
spread_future = data[['Date']].reset_index().apply( lambda x : current_date_spread.get(x[0] + '_' + str(x[1] + relativedelta(months=+3)), np.nan), axis = 1)
data.insert(data.columns.tolist().index('OAS') + 1, 'OAS Future', spread_future.values)

#data_reg = data_reg.dropna(subset=['OAS', 'OAS Future'])
#data_reg = data_reg[(data_reg['OAS'] >0) & (data_reg['OAS Future'] >0) ]

data.insert(data.columns.tolist().index('OAS Future')+1, 'OAS Future Change', data['OAS Future']/data['OAS']-1)
data['OAS Future Change'] = data['OAS Future Change'].clip(upper=3)









#data = data[~(data['Date'] == dates[-1])]

#print (pd.DataFrame(data['Rating Future'].value_counts()).sort_index())

#data = data[ ~data['Rating Future'].isin(['CCC+', 'CCC', 'CCC-', 'CC+', 'CC', 'CC-', 'C+', 'C', 'C-', 'DD+', 'DDD+', ''])]

#rating_map = { 'AAA' : 'IG High', 'AA+' : 'IG High', 'AA' : 'IG High', 'AA-' : 'IG High', 'A+' : 'IG High', 'A' : 'IG High', 'A-' : 'IG High',
#               'BBB+' : 'IG Low', 'BBB' : 'IG Low', 'BBB-' : 'IG Low', 
#               'BB+' : 'HY', 'BB' : 'HY', 'BB-' : 'HY', 'B+' : 'HY', 'B' : 'HY', 'B-' : 'HY'  }

rating_map = { 'AAA' : 1, 'AA+' : 1, 'AA' : 1, 'AA-' : 1, 'A+' : 1, 'A' : 1, 'A-' : 1,
               'BBB+' : 2, 'BBB' : 2, 'BBB-' : 2, 
               'BB+' : 3, 'BB' : 3, 'BB-' : 3, 'B+' : 3, 'B' : 3, 'B-' : 3  }

data.insert(data.columns.tolist().index('Rating Future') + 1, 'Category Future', data['Rating Future'].apply( lambda x : rating_map[x] ))

print(pd.DataFrame( data['Category Future'].value_counts()))

data_to_display = data[data['Date'] == dates[-2]] #check only one date for performance issues
data_to_display = data_to_display.drop(columns = ['Date', 'Rating Future', 'Industry', 'Rating'])





data.to_csv("bond_rating.csv")
quit()
#plt.scatter(data_to_display["OAS"], data_to_display["Duration"])#, color="Category Future")
#plt.ylabel("Duration")
#plt.xlabel("OAS")
#plt.show()

X = [ 'OAS', 'Prob of Default', 'Yield', 'Coupon', 'Amount Outstanding', 'Duration',
      'Maturity Years', 'EBITDA Margin', 'ROA', 'Current Ratio', 'Quick Ratio',
      'Debt to EBITDA', 'Debt to Assets', 'Debt to Equity', 'ROE']
#['OAS', 'Duration']
y = 'Category Future'

scaleX = MinMaxScaler()

# set the first six quarters as the train set
data_dropna = data.dropna(subset=X)
X_train = data_dropna.loc[~data_dropna['Date'].isin(dates[-3:]), X]
y_train = data_dropna.loc[~data_dropna['Date'].isin(dates[-3:]), y]

X_train = scaleX.fit_transform(X_train)

# set the last six quarters as the test set
X_test  = data_dropna.loc[data_dropna['Date'].isin(dates[-3:]), X]
y_test  = data_dropna.loc[data_dropna['Date'].isin(dates[-3:]), y]

#X_train, X_test, y_train, y_test = train_test_split(X_sm, y_sm, test_size=0.2)

model = Sequential()
model.add(Dense(20, input_dim=15, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(4, activation='softmax'))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=["categorical_accuracy"])

model.fit(X_train, to_categorical(y_train), epochs=1000, batch_size=100, verbose=1)
model.save("bond_rating")

#X_test = scaleX.transform(X_test)
#model.evaluate(X_test, y_test)



start_date = date(2017, 10, 1)
periods = 9 
dates = generate_dates(start_date, "24m", "3m")

data = pd.read_pickle("./bond_issuer_data.pkl")

## prepare the dict with security + date key and rating as a value
#current_date_spread = dict( zip(data_reg.index + '_' + data_reg['Date'].astype(str), data_reg['OAS']) )
#
## create a column with next period\quarter spread (future spread)
## tech details: find in prepared current_date_spread a key, which is equal security + date+3months
#spread_future = data_reg[['Date']].reset_index().apply( lambda x : current_date_spread.get(x[0] + '_' + str(x[1] + relativedelta(months=+3)), np.nan), axis = 1)
#data_reg.insert(data_reg.columns.tolist().index('OAS') + 1, 'OAS Future', spread_future.values)
#
#data_reg = data_reg.dropna(subset=['OAS', 'OAS Future'])
#data_reg = data_reg[(data_reg['OAS'] >0) & (data_reg['OAS Future'] >0) ]
#
#data_reg.insert(data_reg.columns.tolist().index('OAS Future') + 1, 'OAS Future Change', data_reg['OAS Future'] / data_reg['OAS'] -1  )
#
#data_reg['OAS Future Change'] = data_reg['OAS Future Change'].clip(upper=3)
#
#data_reg.head()
#
#plt.figure(figsize=(10,5))
#
#sns.kdeplot(data_reg['OAS Future Change'], shade=True)
#
#plt.legend(fontsize=14)
#plt.title('Distribution of OAS Spread change', fontsize=14)
#plt.show()
#
#
## Features or independent variables
#features = ['OAS', 'Duration']
## Our target or dependent variable
#target = 'OAS Future Change'
#
## set the first six quarters as the train set
#data_dropna = data_reg.dropna(subset=features)
#X_train = data_dropna.loc[ ~data_dropna['Date'].isin(dates[-3:]), features]
#y_train = data_dropna.loc[ ~data_dropna['Date'].isin(dates[-3:]), target]
#
## set the last six quarters as the test set
#X_test  = data_dropna.loc[ data_dropna['Date'].isin(dates[-3:]), features]
#y_test  = data_dropna.loc[ data_dropna['Date'].isin(dates[-3:]), target]
#tree_regressor = DecisionTreeRegressor(max_depth=3, random_state=63)
## fit the model on training data
#tree_regressor.fit(X_train, y_train)
#
## make a prediction
#prediction = tree_regressor.predict( X_test )
#print('DecisionTreeRegressor prediction:', prediction)
