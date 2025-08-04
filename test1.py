
import matplotlib.pyplot as plt
import pandas as pd

computation_time = [10, 20, 5, 30]
storage_size = [[10, 15], [20, 5]]

index = []
for i in range(len(computation_time)):
    index.append(i+1)
existing = 0
propose = 0
for i in range(len(storage_size)):
    size = storage_size[i]
    propose = propose + size[1]
    existing = existing + size[0]

df = pd.DataFrame([[existing, propose]], columns=['Existing', 'Propose'])

figure, axis = plt.subplots(nrows=1, ncols=2,figsize=(10,4))
axis[0].set_title("Storage Graph")
axis[1].set_title("Computation Time Graph")
axis[1].plot(index, computation_time, label="Computation Time")
axis[1].legend()
'''
axis[0].bar([existing], [propose], label=['Existing', 'Propose'])
axis[0].set_xlabel("Technique Name")
axis[0].set_ylabel("Storage Size")
axis[0].set_xticklabels(['Existing', 'Propose'], rotation=45)
'''
df.plot(ax=axis[0], kind='bar')
plt.show()
