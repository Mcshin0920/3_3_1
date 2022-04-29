import matplotlib.pyplot as plt
import pandas as pd


# Load in the data with read_csv()
# TODO #1: change the file name to your data file name
Data_file = pd.read_csv("insertdatafilehere.csv", header=0)   # identify the header row

# TODO #2: Use matplotlib to make a line graph
plt.plot(Data_file['decimal_year'], Data_file['Average'], color='gray')
plt.ylabel('SAT scores')
plt.xlabel('Home prices')
plt.title('SAT scores vs Home prices')
plt.show()
