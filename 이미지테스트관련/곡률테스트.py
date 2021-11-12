import matplotlib.pyplot as plt
import matplotlib 

test_list = [[4, 2], [5, 1], [6, 3], [7, 11]]
print(list(zip(*test_list))[0])
plt.scatter(list(zip(*test_list))[0], list(zip(*test_list))[1])

plt.show()