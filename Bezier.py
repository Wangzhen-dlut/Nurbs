# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 20:18 2018

aimed at plotting bezier curve
C(u)=sum(Bi,n(u))Pi

@author: Wangzhen
"""
import matplotlib.pyplot as plt
import numpy as np
import logging
import time
import os
import traceback
import sys
import math

logging.basicConfig(level=logging.DEBUG, filemode='a', format='%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

current_dirname = os.getcwd()
if not os.path.isdir(current_dirname + "/logs"):
    os.mkdir(current_dirname + "/logs")

logfile_name = os.getcwd() + '/logs/' + time.strftime("%Y%m%d_%H%M%S", time.localtime()) + ".log"
handler = logging.FileHandler(logfile_name)
# handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(handler)


def main():
    t_start = time.time()
    # -----------------------initialization---------------------------------
    # input points
    # control_points = [[0.0, 0.0], [1.0, 1.0], [2.0, 1.0], [3.0, 0.0]]
    control_points = [[0.0, 0.0], [-1.0, 1.0], [0.0, 2.0], [1.0, 3.0], [2.0, 1.5], [3.0, 0.0], [1.0, -1.0], [0.0, 0.0]]

    num_points = np.shape(control_points)[0]
    order_curve = num_points - 1
    logger.info("The order of bezier curve is:%d" % (order_curve,))
    u_list = np.linspace(0, 1, 101, endpoint=True)


    B = {}
    for i in range(num_points):
        B_=[]
        for u in u_list:
            B_.append((math.factorial(order_curve)*(u ** i)* ((1 - u) ** (order_curve - i))) / math.factorial(i) / math.factorial(order_curve - i))
        B[i]=B_

    x_curve, y_curve = np.zeros(len(u_list)), np.zeros(len(u_list))
    for k, v in B.items():
        x_curve += np.asarray(v) * control_points[k][0]
        y_curve += np.asarray(v) * control_points[k][1]

    x_line,y_line=[],[]
    for v in control_points:
        x_line.append(v[0])
        y_line.append(v[1])

    # --------------------------------plot figure-------------------------------------------------
    plt.figure(figsize=(8, 4), dpi=200)
    plt.plot(x_curve,y_curve,'c-')
    plt.plot(x_line,y_line,'g--*')
    t_end = time.time()
    logger.info("The procedure all is done")
    logger.info("all time is:%8.4f" % (t_end - t_start,))
    plt.show()
    # -------------------------plot B func------------------------
    plt.figure(2)
    for i in range(num_points):
        plt.plot(B[i])
    plt.show()
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        # exc_type, exc_value, exc_trackback_obj = sys.exc_info()
        # logger.info("exc_type:%s" % (exc_type,))
        # logger.info("exc_value:%s" % (exc_value,))
        logger.info(traceback.format_exc(limit=1))
