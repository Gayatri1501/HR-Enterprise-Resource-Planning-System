


# how to legend create a pie chart
import matplotlib.pyplot as plt
import numpy as np

x = np.array([60 , 30, 10 ])
mylable = ['Submit', 'Pending', 'Progress']


plt.pie(x, labels=mylable)
plt.legend(title='Task Report')
plt.show()