import numpy as np
# import matplotlib
import matplotlib.pyplot as plt

# matplotlib.use('Agg')

t = np.linspace(0, 30, 31)

rsf_non = [1, 2, 2, 2, 2, 2, 3, 6, 6, 7, 9, 9, 16, 20, 25, 27, 32, 34, 37, 40, 41, 43, 44, 44, 45, 46, 46, 46, 46, 46, 46]
rsf_rel = [1, 2, 4, 4, 5, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 10, 11, 14, 15, 15, 15, 15, 15, 15, 17, 17, 17, 17, 17, 17]
rse_non = [1, 6, 11, 15, 20, 21, 24, 32, 34, 37, 39, 40, 46, 48, 51, 52, 52, 52, 52, 54, 54, 55, 55, 55, 57, 57, 57, 57, 57, 57, 57]
rse_rel = [0, 3, 8, 10, 14, 22, 25, 31, 33, 39, 43, 46, 49, 51, 57, 58, 61, 64, 67, 71, 74, 76, 79, 81, 81, 81, 81, 81, 81, 81, 81]
suc_non = [5, 6, 6, 9, 10, 10, 11, 11, 13, 15, 17, 20, 20, 20, 20, 24, 24, 27, 27, 28, 29, 30, 31, 34, 34, 34, 34, 34, 34, 34, 34]
suc_rel = [1, 5, 5, 6, 6, 6, 7, 10, 10, 10, 13, 13, 14, 15, 16, 18, 19, 21, 23, 23, 23, 24, 26, 26, 28, 27, 27, 27, 27, 27, 27]

# plt.plot(t, rsf_non, color="red", label="non_relocation")
# plt.plot(t, rsf_rel, color="blue", label="relocation")
# plt.legend()
# plt.grid()
# plt.title('only rsf considerd')
# plt.xlim(0, 30)
# plt.ylim(0, 50)
# plt.xlabel('time')
# plt.ylabel('a number of rsf')
# plt.show()

# plt.plot(t, rse_non, color="red", label="non_relocation")
# plt.plot(t, rse_rel, color="blue", label="relocation")
# plt.legend()
# plt.grid()
# plt.title('only rsf considerd')
# plt.xlim(0, 30)
# plt.ylim(0, 85)
# plt.xlabel('time')
# plt.ylabel('a number of rse')
# plt.show()

plt.plot(t, suc_rel, color="red", label="non_relocation")
plt.plot(t, suc_non, color="blue", label="relocation")
plt.legend()
plt.grid()
plt.title('only rsf considerd')
plt.xlim(0, 30)
plt.ylim(0, 40)
plt.xlabel('time')
plt.ylabel('a number of success')
plt.show()
