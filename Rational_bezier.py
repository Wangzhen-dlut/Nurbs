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
    current_dir=os.path.abspath(os.getcwd())
    # -----------------------initialization---------------------------------
    # input points
    # control_points = [[0.0, 0.0], [1.0, 1.0], [2.0, 1.0], [3.0, 0.0]]
    control_points = [[0.0, 0.0], [-1.0, 1.0], [0.0, 2.0], [1.0, 3.0], [2.0, 1.5], [3.0, 0.0], [1.0, -1.0], [0.0, 0.0]]
    w_func = [1, 1, 1, 1,1, 1, 1, 1]

    num_points = np.shape(control_points)[0]
    order_curve = num_points - 1
    logger.info("The order of bezier curve is:%d" % (order_curve,))
    u_list = np.linspace(0, 1, 201, endpoint=True)

    B = {}
    for i in range(num_points):
        B_ = []
        for u in u_list:
            B_.append((math.factorial(order_curve) * (u ** i) * ((1 - u) ** (order_curve - i))) / math.factorial(
                i) / math.factorial(order_curve - i))
        B[i] = B_

    W=np.zeros(len(u_list))
    for i in range(num_points):
        W+=w_func[i]*np.asarray(B[i])

    R = {}
    for i in range(num_points):
        R[i]=w_func[i]*np.asarray(B[i])/W

    x_curve, y_curve = np.zeros(len(u_list)), np.zeros(len(u_list))
    for k, v in R.items():
        x_curve += np.asarray(v) * control_points[k][0]
        y_curve += np.asarray(v) * control_points[k][1]

    x_line, y_line = [], []
    for v in control_points:
        x_line.append(v[0])
        y_line.append(v[1])

    # --------------------------------plot figure-------------------------------------------------
    plt.figure(figsize=(8, 4), dpi=200)
    plt.subplot(121)
    plt.title("Rational Bezier curve",fontsize="12")
    plt.xlabel("x",color='gray')
    plt.ylabel("y",color='gray')
    plt.grid(True,linestyle=':',axis="both")
    plt.plot(x_curve, y_curve, 'c-')
    plt.plot(x_line, y_line, 'g--*')
    for i in range(len(x_line)-1):
        plt.text(x_line[i]+0.1,y_line[i],f"p{i}",fontsize="8")
    plt.text(x_line[len(x_line)-1]-0.3,y_line[len(x_line)-1],f"p{len(x_line)-1}",fontsize="8")
    plt.legend(labels=["Bezier","Points",],loc=0,fontsize="8")


    # -------------------------plot R func------------------------
    plt.subplot(122)
    plt.title("R func",fontsize="12")
    plt.grid(True,linestyle=':')
    for i in range(num_points):
        plt.plot(R[i])
        plt.text(np.argmax(R[i])-5,np.max(R[i]),f'R{i}',fontsize="8")
    # plt.legend([f"R{i}" for i in range(num_points)], loc=9,fontsize="6")

    if not os.path.isdir(os.path.join(current_dir,'picture')):
        os.mkdir(os.path.join(current_dir,'picture'))

    plt.savefig(os.path.join(current_dir,"picture", "Rational_Bezier_curve.png"))
    plt.show()

    t_end = time.time()
    logger.info("The procedure all is done")
    logger.info("all time is:%8.4f" % (t_end - t_start,))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        # exc_type, exc_value, exc_trackback_obj = sys.exc_info()
        # logger.info("exc_type:%s" % (exc_type,))
        # logger.info("exc_value:%s" % (exc_value,))
        logger.info(traceback.format_exc())
