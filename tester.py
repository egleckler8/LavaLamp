'''
tests creation of one lavalamop
'''
import json

from lavalamp import LampGen


g = LampGen()
response = g.createGIF(filepath="/Users/eli/Desktop/stuff")

print(response)


# # Let's store the data
# with open('data.txt', 'w') as f:
#     f.write(response)
#     f.write('\n')
#
# # Get it back
# with open('data.txt', 'r') as f:
#     line = f.readline()
#
#     j = json.loads(line)
#
#     new_seed = [j['seed']['r_seed'], j['seed']['g_seed'], j['seed']['b_seed']]
#
#     print('New seed:', new_seed)
#
#
# # And create an identical lavalamp?
# g.createGIF(s=new_seed, filepath="/Users/eli/Desktop/stuff")
