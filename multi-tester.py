'''
tests creation of many lavalamps
and charts the data in a csv file
'''

import lavalamp

# We'll want to increment the size of these lavalamps and
# check how long it takes to make them based on their size
# I'd say 10 of each size would be ok, and we can go up to like
# 1000x1000, maybe starting from 100x100, in increments of 10
SAVE_PATH = "../lavalamp-samples"

for size_incr in range(350,1001,10):

    # For each size we want to create 10 samples...
    g = lavalamp.LampGen(size=size_incr)

    for sample_cnt in range(10):
        json_data = g.createGIF(filepath=SAVE_PATH)

        with open('data.txt', 'a') as f:
            f.write(json_data)
            f.write('\n')
