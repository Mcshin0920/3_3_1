import matplotlib.pyplot as plt
import pandas as pd
import numpy

final_data = pd.read_csv("final.csv", header=0)   
plt.scatter(final_data['Max SAT'], final_data['Average House Price'], color='gray')
plt.ylabel('Average District House Price')
plt.xlabel('Max Average District SAT')
plt.title('District SAT Scores vs Surrounding House Prices')

z = numpy.polyfit(final_data['Max SAT'], final_data['Average House Price'], 1)
p = numpy.poly1d(z)
plt.plot(final_data['Max SAT'],p(final_data['Max SAT']),"r--")
print("y=%.6fx+(%.6f)"%(z[0],z[1]))
plt.show()
