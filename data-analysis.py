'''
Analyzing the json data in data.txt
'''

import json
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

x_pts = [] # number of pixels in the image
y_pts = [] # time of generation in seconds

with open('data.txt', 'r') as f:

    line = f.readline()

    # Loop over the whole file
    while line:
        # Remember, each line is a json string
        data = json.loads(line.strip())

        num_pixels = data['size']['width'] * data['size']['height']
        gen_time = data['gen_time']

        x_pts.append(num_pixels)
        y_pts.append(gen_time)

        line = f.readline()


# Regression analysis:
x_column_vec = np.array(x_pts).reshape(-1, 1) # column vector, now
model = LinearRegression()
model.fit(x_column_vec, y_pts)
# Regression line:
m = model.coef_[0]
b = model.intercept_
print('Slope of linear regression model: {}'.format(m))
print('Intercept: {}'.format(b))


# Make a plot
plt.scatter(x_pts, y_pts)
plt.plot(x_pts, m*x_column_vec + b, color='red', label='Linear Regression')
plt.xlabel('Number of Pixels')
plt.ylabel('Generation Time (seconds')
plt.title('Time of current LavaLamp algo based on requested image size')
plt.legend([f'Slope of linreg: {round(m, 8)}', f'Intercept: {round(b, 8)}'])
plt.show()



