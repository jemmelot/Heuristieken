import numpy as np

test = np.zeros((22, 22))
test[0][0] += 1
#print(test)

aah = np.zeros((22, 22))
aah[1][0] += 5
#print(aah)

print(test + aah)