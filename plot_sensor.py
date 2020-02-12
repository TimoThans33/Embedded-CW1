#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import time
import matplotlib.animation as animation

angle_back = np.random.rand(100) *360 - 180
angle_neck = np.random.rand(100) *360 - 180
x = np.arange(100)
timer = time.time()
"""
Lets say an hour is 10 datapoints: how many data points are higher
"""
xax = np.array(["30 s"])
bad_sit = 0
good_sit = 0
bad_lay = 0
good_lay = 0
bad_sit_per = np.array([0])
good_sit_per = np.array([0])
bad_lay_per = np.array([0])
good_lay_per = np.array([0])
k = 0


def valuePercent(val1, val2):
    per1 = val1/(val1+val2)*100
    per2 = val2/(val1+val2)*100
    return per1, per2


for i in range(len(x)):
    if angle_back[i] > 150 or angle_back[i] < -150:
        laying = True
        sitting = False
    else:
        laying = False
        sitting = True

    if sitting == True:
        if angle_back[i] > 70 and angle_back[i] < 100 and angle_neck[i] < 30:
            good_sit += 1 #depends on frequency of the data in our case this is 6
        else:
            bad_sit += 1
    if laying == True:
        if angle_back[i] > 0 and angle_neck[i] < 30:
            good_lay += 1
        else:
            bad_lay += 1
    if time.time() - timer >= 2:
        sit_per1, sit_per2 = valuePercent(good_sit, bad_sit)
        lay_per1, lay_per2 = valuePercent(good_lay, bad_lay)
        if k == 0:
            good_sit_per = sit_per1
            bad_sit_per = sit_per2
            good_lay_per = lay_per1
            bad_lay_per = lay_per2
        else:
            bad_sit_per = np.append(bad_sit_per, sit_per2)
            good_sit_per = np.append(good_sit_per, sit_per1)
            bad_lay_per = np.append(bad_lay_per, lay_per2)
            good_lay_per = np.append(good_lay_per, lay_per1)
        timer = time.time()
        xax = np.append(xax,'30 s')
        bad_sit = 0
        good_sit = 0
        bad_lay = 0
        good_lay = 0
        k += 1
        print(bad_sit_per, good_sit_per,bad_lay_per,good_lay_per)
    time.sleep(0.1)


index = np.arange(len(bad_sit_per))
bar_width = 0.2
opacity = 0.6
plt.figure(0,figsize=(12, 8))

plt.bar(index, good_sit_per, bar_width, alpha = 0.6, label = 'Good: sitting position')
plt.bar(index + bar_width, bad_sit_per, bar_width,
        alpha = opacity, label = 'Bad: sitting position')
plt.bar(index + 2*bar_width, good_lay_per, bar_width,
        alpha = opacity, label = 'Good: laying position' )
plt.bar(index + 3*bar_width, bad_lay_per, bar_width, alpha = 0.6, label = 'Bad: laying position' )
plt.xlabel('Time')
plt.ylabel('Percent')
plt.ylim(0,100)
plt.title('Time spent in position')
plt.xticks(index + bar_width, xax)
plt.legend()

plt.tight_layout()
plt.show()





plt.figure(0)
plt.plot(x, angle_back, label='back')
plt.plot(x, angle_neck, label='neck')
plt.legend()
plt.ylabel('Angle')
plt.xlabel('Time')

"""
Time spent in bad posture?
"""
