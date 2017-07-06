# -*- coding: utf-8 -*-
import numpy as np
from sklearn.externals import joblib
from watchdog.events import *
from watchdog.observers import Observer
import time


class FileEventHandler(FileSystemEventHandler):
    flag = 0

    def __init__(self):
        FileSystemEventHandler.__init__(self)


    def on_moved(self, event):
        if event.is_directory:
            print("directory moved from {0} to {1}".format(event.src_path,event.dest_path))
        else:
            print("file moved from {0} to {1}".format(event.src_path,event.dest_path))

    def on_created(self, event):
        if event.is_directory:
            print("directory created:{0}".format(event.src_path))
        else:
            print("file created:{0}".format(event.src_path))

    def on_deleted(self, event):
        if event.is_directory:
            print("directory deleted:{0}".format(event.src_path))
        else:
            print("file deleted:{0}".format(event.src_path))

    def on_modified(self, event):
        if self.flag == 2:
            test_model()
            self.flag = 0
        if event.is_directory:
            print("directory modified:{0}".format(event.src_path))
        else:
            print("file modified:{0}".format(event.src_path))
            self.flag += 1


def judge_accuracy(predict_array, real_array):
    correct = 0
    for i in range(len(predict_array)):
        if predict_array[i] == real_array[i]:
            # print(predict_array[i], real_array[i])
            correct += 1
    correct_rate = correct / len(predict_array)
    return correct_rate


def test_model():
    data = []
    labels = []
    with open("test/sample2_2.csv") as file:
        for line in file:
            tokens = line.strip().split(',')
            data.append([float(tk) for tk in tokens[1:4]])
            labels.append(tokens[0])
    test_X = np.array(data)
    test_Y = np.array(labels)
    # print("测试输入为：", test_X)
    clf_linear = joblib.load("model/model_linear.m")
    test_X_result = clf_linear.predict(test_X)
    # print("预测结果：", test_X_result)
    # print("正确结果：", test_Y)
    print("linear预测准确率：", judge_accuracy(test_X_result, test_Y))

    clf_linear = joblib.load("model/model_poly.m")
    test_X_result = clf_linear.predict(test_X)
    # print("预测结果：", test_X_result)
    # print("正确结果：", test_Y)
    print("poly预测准确率：", judge_accuracy(test_X_result, test_Y))

    clf_linear = joblib.load("model/model_rbf.m")
    test_X_result = clf_linear.predict(test_X)
    # print("预测结果：", test_X_result)
    # print("正确结果：", test_Y)
    print("rbf预测准确率：", judge_accuracy(test_X_result, test_Y))

    clf_linear = joblib.load("model/model_sigmoid.m")
    test_X_result = clf_linear.predict(test_X)
    # print("预测结果：", test_X_result)
    # print("正确结果：", test_Y)
    print("sigmoid预测准确率：", judge_accuracy(test_X_result, test_Y))

    '''
    with open("ATM/result/ATM34_test_result_linear_ATM12_time.txt", 'w') as file2:
        for line in test_X_result:
            file2.write(line)
            file2.write('\n')
    '''

if __name__ == "__main__":
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler, "D:/Github/ML-SVM/model", True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

