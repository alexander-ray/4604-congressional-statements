import matplotlib.pyplot as plt
import numpy as np

# Code mostly from HW2
class Plotting:
    @staticmethod
    def plot_single(x, y, x_label, y_label, title):
        plt.plot(x, y)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.show()

    @staticmethod
    def plot_double(x, y1, y2, x_label, y_label, title, diff1, diff2):
        plt.plot(x, y1, color='blue', lw=2, marker='o', label=diff1)
        plt.plot(x, y2, color='red', lw=2, marker='o', label=diff2)

        ax = plt.gca()
        ax.set_xscale('log')

        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.legend(loc='upper right')
        plt.show()

    # https://matplotlib.org/examples/api/barchart_demo.html
    @staticmethod
    def bar_chart(r_data, d_data, labels, y_label, title, legend):
        n = len(labels)
        ind = np.arange(n)  # the x locations for the groups
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(ind, r_data, width, color='red')

        rects2 = ax.bar(ind + width, d_data, width, color='blue')
        # add some text for labels, title and axes ticks
        ax.set_ylabel(y_label)
        ax.set_title(title)
        ax.set_xticks(ind + width / 2)
        ax.set_xticklabels(labels)

        ax.legend((rects1[0], rects2[0]), legend)

        plt.show()
