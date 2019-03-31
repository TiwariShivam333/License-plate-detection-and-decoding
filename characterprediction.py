import segmentletters
import pickle
import pandas as pd
print("Loading model")
filename = 'learned_model.sav'
model = pickle.load(open(filename, 'rb'))

print('Model loaded. Predicting characters of number plate')
classification_result = []
for each in segmentletters.characters:
    each = each.reshape(1, -1);
    result = model.predict(each)
    classification_result.append(result)

print('Classification result')
print(classification_result)

plate = ''
for each in classification_result:
    plate += each[0]

#Arranging plate letters in order
column_list_copy = segmentletters.column_list[:]
segmentletters.column_list.sort()
rightplate = ''
for each in segmentletters.column_list:
    rightplate += plate[column_list_copy.index(each)]

print("\n")
print('License plate')
print(rightplate)
print("\n")
if int(rightplate[-1])%2==0:
    print("To be run on even days only")
else:
    print("To be run on odd days only")
print("\n")
data=pd.read_csv('database.csv',header=None)
arr=data.values
for x in arr:
    if x[0]==rightplate:
        print("Name- %s, Address- %s, Phone- %s"% (x[1],x[2],x[3]))
        print("Year of purchase- %s, Age of Vehicle- %s"% (x[4],2018-int(x[4])))
        break
