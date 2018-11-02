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
    current_dir = os.path.abspath(os.getcwd())
    # -----------------------initialization---------------------------------
    # input points
    # control_points = [[0.0, 0.0], [1.0, 1.0], [2.0, 1.0], [3.0, 0.0]]
    control_points = [[0.0, -0.5], [2.0, 0.0], [0.0, -2.0], [-2.0, 0.0], [0.0, -0.5]]
    w_func = [1, 5, 5, 5, 1]
    U = [0, 0, 0, 1 / 5, 2 / 5, 3 / 5, 4 / 5, 1, 1, 1]

    num_points = np.shape(control_points)[0]
    order_curve = len(U) - num_points - 1
    logger.info("The order of Bspline is:%d" % (order_curve,))
    u_num = 501
    u_list = np.linspace(np.min(np.asarray(U)), np.max(np.asarray(U)), u_num, endpoint=True)
    order_list = [i + 1 for i in range(order_curve)]

    N = {}
    for i in range(len(U) - 1):
        if U[i] == U[i + 1]:
            N[f"N{i}{0}"] = np.zeros(u_num)
        else:
            Ni_append = []
            for u in u_list:
                if U[i] <= u < U[i + 1]:
                    Ni_append.append(1)
                else:
                    Ni_append.append(0)
            N[f"N{i}{0}"] = Ni_append
    # for i in range(len(U) - 1):
    #     logger.info(f"N{i}{0}:%s" % (N[f'N{i}{0}'],))

    for p in order_list:
        for i in range(len(U) - p - 1):
            if U[i + p] == U[i] and U[i + p + 1] == U[i + 1]:
                Ni_append = []
                for k, u in enumerate(u_list):
                    Ni_append.append((u - U[i]) * N[f'N{i}{p-1}'][k] + (U[i + p + 1] - u) * N[f'N{i+1}{p-1}'][k])
                N[f'N{i}{p}'] = Ni_append
            elif U[i + p] == U[i] and U[i + p + 1] != U[i + 1]:
                Ni_append = []
                for k, u in enumerate(u_list):
                    Ni_append.append(
                        (u - U[i]) * N[f'N{i}{p-1}'][k] + (U[i + p + 1] - u) * N[f'N{i+1}{p-1}'][k] / (
                                U[i + p + 1] - U[i + 1]))
                N[f'N{i}{p}'] = Ni_append

            elif U[i + p] != U[i] and U[i + p + 1] == U[i + 1]:
                Ni_append = []
                for k, u in enumerate(u_list):
                    Ni_append.append((u - U[i]) * N[f'N{i}{p-1}'][k] / (U[i + p] - U[i]) + (U[i + p + 1] - u) *
                                     N[f'N{i+1}{p-1}'][k])
                N[f'N{i}{p}'] = Ni_append

            else:
                Ni_append = []
                for k, u in enumerate(u_list):
                    Ni_append.append((u - U[i]) * N[f'N{i}{p-1}'][k] / (U[i + p] - U[i]) + (U[i + p + 1] - u) *
                                     N[f'N{i+1}{p-1}'][k] / (U[i + p + 1] - U[i + 1]))
                N[f'N{i}{p}'] = Ni_append
    # for p in order_list:
    #     for i in range(len(U) - p - 1):
    #         logger.info(f"N{i}{p}:%s" % (N[f'N{i}{p}'],))

    W = np.zeros(len(u_list))
    for i in range(num_points):
        W += w_func[i] * np.asarray(N[f'N{i}{order_curve}'])

    R = {}
    for i in range(num_points):
        R[i] = w_func[i] * np.asarray(N[f'N{i}{order_curve}']) / W

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
    plt.title("Nurbs", fontsize="12")
    plt.xlabel("x", color='gray')
    plt.ylabel("y", color='gray')
    plt.grid(True, linestyle=':', axis="both")
    plt.plot(x_curve, y_curve, 'c-')
    plt.plot(x_line, y_line, 'g--*')
    plt.legend(["Bspline", "Points"], loc=0, fontsize="8")

    # -------------------------plot N func------------------------
    plt.subplot(122)
    plt.title("N func", fontsize="12")
    plt.grid(True, linestyle=':')

    for i in range(num_points):
        plt.plot(N[f"N{i}{order_curve}"])
        plt.text(np.argmax(N[f"N{i}{order_curve}"])-5,np.max(N[f"N{i}{order_curve}"]),f"N{i}{order_curve}",fontsize="8")
    # plt.legend([f"R{i}" for i in range(num_points)], loc=0,fontsize="6")

    if not os.path.isdir(os.path.join(current_dir, 'picture')):
        os.mkdir(os.path.join(current_dir, 'picture'))

    plt.savefig(os.path.join(current_dir, "picture", "Nurbs.png"))
    plt.show()

    t_end = time.time()
    logger.info("The procedure all is done")
    logger.info("all time is:%8.4f" % (t_end - t_start,))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        # exc_type, exc_value, exc_trackback_obj = sys.exc_info()
        logger.info(traceback.format_exc())
