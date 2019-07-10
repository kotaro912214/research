import time
import tqdm

bar = tqdm.tqdm()
a = 0
for i in range(100):
  bar.update(1)
  time.sleep(0.1)
bar.close()