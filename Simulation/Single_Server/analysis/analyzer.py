from statistics import *
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline


def print_sorted_dict(my_dict: dict, my_label: str = '') -> None:
    if my_label != '':
        print('\n === %s === ' % my_label)
    for key in sorted(my_dict.keys()):
        print("%d :: %7.3f" % (key, my_dict[key]))


def autolabel(rects, ax):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1.006 * height,
                '%5.2f' % height, ha='center', va='bottom')


# Time series methods
def print_ts(my_list: list, label: str = '') -> None:
    def data_elements(x): return str('%8.3f - %d' % (x['time'], x['value']))
    data = list(map(data_elements, my_list))
    if label != '':
        print('\n=== %s ===' % label)
    print(*data, sep="\n")


def plot_ts(my_list: list, total_time: float, my_label: str = '', x_label: str = 'Time ->', y_label: str = '') -> None:
    fig, ax = plt.subplots()

    def plot_x(x): return x['time']
    def plot_y(x): return x['value']

    # Main graph
    ax.set_title("TS plot for %s" % my_label)
    ax.set_ylabel(y_label)
    ax.set_ylim(0, get_max_ts(my_list) * 1.5)
    ax.set_yticks(list(dict.fromkeys(map(plot_y, my_list))))
    ax.set_xlabel(x_label)
    ax.set_xlim(0, total_time)

    plt.plot(list(map(plot_x, my_list)), list(map(plot_y, my_list)))
    plt.scatter(list(map(plot_x, my_list)), list(map(plot_y, my_list)))
    plt.show()


def hist_bar_ts(my_list: list, my_field: str, my_label: str = '', x_label: str = '',
                y_label: str = 'Instances') -> None:
    fig, ax = plt.subplots()

    def plot_y(x): return x[my_field]
    bins = list(dict.fromkeys(map(plot_y, my_list)))
    bins.sort()
    bins.append(bins[len(bins)-1]+1)
    # Main graph
    ax.set_title("Histogram for %s" % my_label)
    # Y-axis settings
    ax.set_ylabel(y_label)

    # X-axis settings
    ax.set_xlabel(x_label)
    ax.set_xticks(bins)  # set the position of the x ticks

    hist = plt.hist(list(map(plot_y, my_list)), bins=bins, rwidth=0.8)
    ax.set_ylim(0, math.ceil(max(hist[0]) * 1.2))
    # Align properly the label for the bins
    bin_w = (max(bins) - min(bins)) / (len(bins) - 1)
    plt.xticks(np.arange(min(bins) + bin_w / 2, max(bins)+1, bin_w), bins)
    plt.xlim(bins[0], bins[-1])
    # Set the labels on top of the bars
    for i in range(len(bins)-1):
        plt.text(hist[1][i] + ((min(bins) + bin_w / 2) * 0.9),
                 0.15 + hist[0][i], str(int(hist[0][i])))
    plt.show()


def evolution_bar_ts(my_list: list, total_time: float, my_label: str = '',
                     x_label: str = 'Time ->', y_label: str = 'Occupation') -> None:
    width = []
    trend_x = []
    trend_y = []
    # Prepare the data for the multiple plots overlay
    list_size = len(my_list)
    for i in range(list_size):
        next_time = my_list[i +
                            1]['time'] if (i + 1) < list_size else total_time
        width.append(next_time - my_list[i]['time'])
        if my_list[i]['time'] != next_time:
            trend_x.append(my_list[i]['time'])
            trend_y.append(my_list[i]['value'])
    trend_x.append(total_time)
    trend_y.append(0.0)
    if trend_x[0] != 0:
        trend_x.insert(0, 0.0)
        trend_y.insert(0, 0.0)
    trend_x = np.array(trend_x)
    trend_y = np.array(trend_y)
    def plot_x(x): return x['time']
    def plot_y(x): return x['value']
    x_values = list(map(plot_x, my_list))
    y_values = list(map(plot_y, my_list))
    fig, ax = plt.subplots()

    # Main graph
    ax.set_title("Evolution over time for %s" % my_label)
    # Y-axis settings
    ax.set_ylabel(y_label)
    ax.set_ylim(0, get_max_ts(my_list) * 1.5)
    # set the position of the x ticks
    ax.set_yticks(list(dict.fromkeys(map(plot_y, my_list))))
    # ax.set_yticklabels(('X1', 'X2', 'X3', 'X4', 'X5'))
    # X-axis settings
    ax.set_xlabel(x_label)
    ax.set_xlim(0.0, total_time)
    # ax.set_xticks(list(values.keys()))  # set the position of the x ticks
    # ax.set_xticklabels(('X1', 'X2', 'X3', 'X4', 'X5'))
    plt.bar(x_values, y_values, width=width, align='edge', zorder=0)

    # Trending line (Smoothed)
    try:
        xnew = np.linspace(trend_x.min(), trend_x.max(), 20)
        spl = make_interp_spline(trend_x, trend_y)  # type: BSpline
        power_smooth = spl(xnew)
        plt.plot(xnew, power_smooth, color='darkgreen',
                 zorder=2, label='Smooth trend')
    except ValueError:
        print("Can't produce smooth curve. There is not enough data or variance.")
    # Plot of actual change of values over time with constant value
    plt.plot(trend_x, trend_y, color='red', zorder=2, label='Trend')

    # Scatter plot to point out change points where final value remain unchanged
    plt.scatter(x_values, y_values, s=15, color='orange',
                zorder=3, label='Change points')

    ax.legend()
    plt.show()


def cumulative_time_ts(my_list: list, total_time: float, my_label: str = '',
                       x_label: str = '', y_label: str = 'Time') -> None:
    cumulative_time_ts(get_cumulative_time_ts(
        my_list, total_time), my_label, x_label, y_label)


def cumulative_time_ts(values: dict, my_label: str = '', x_label: str = '', y_label: str = 'Time') -> None:
    fig, ax = plt.subplots()
    ax.set_ylim(0, math.ceil(max(values.values())) + 2)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title("Cumulative time in states for %s" % my_label)
    ax.set_xticks(list(values.keys()))  # set the position of the x ticks

    bars = plt.bar(values.keys(), values.values())
    autolabel(bars, ax)
    plt.show()


def get_cumulative_time_ts(my_list: list, total_time: float) -> dict:
    values = {}
    if my_list:
        lastTimeMark = 0.0
        lastMark = 0
        for i in range(len(my_list)):
            key = lastMark
            tempVal = 0.0
            if key in values:
                tempVal = values[key]
            tempVal += my_list[i]['time'] - lastTimeMark
            values[key] = tempVal
            lastTimeMark = my_list[i]['time']
            lastMark = my_list[i]['value']
        values[lastMark] += total_time - lastTimeMark
    return values


def get_max_ts(my_list: list) -> float:
    seq = [x['value'] for x in my_list]
    return max(seq) if seq else 0.0


def get_min_ts(my_list: list) -> float:
    seq = [x['value'] for x in my_list]
    return min(seq) if seq else 0.0


def get_bin_percent_ts(my_dict: dict, total_time: float, my_label: str = '') -> dict:
    print_sorted_dict(my_dict, my_label)
    percent_values = {}
    total = 0.0
    for key, value in my_dict.items():
        percent_values[key] = (value * 100.0) / total_time
        total += percent_values[key]
    print_sorted_dict(percent_values, my_label)
    print("Total: %7.2f %%" % total)
    return percent_values


# Object methods
def print_obj_list(my_list: list, my_method: str, label: str = '') -> None:
    def report(x): return getattr(x, my_method)()
    reporter = list(map(report, my_list))
    if label != '':
        print('=== %s ===' % label)
    print(*reporter, sep="\n")


def get_map_values(my_objs: list, my_attr: str) -> list:
    return _get_map_values(my_objs, my_attr, False, 0.0)


def _get_map_values(my_objs: list, my_attr: str, w_filter: bool, val: float) -> list:
    def values(x): return getattr(x, my_attr)
    data = list(map(values, my_objs))
    if w_filter:
        data = list(filter(lambda a: a != val, data))
    return data


def objects_as_str(my_objs: list) -> str:
    def strings(x): return str(x)
    return str(list(map(strings, my_objs)))


def get_max_obj(my_objs: list, my_attr: str, w_filter: bool = False, val: float = 0.0) -> float:
    return max(_get_map_values(my_objs, my_attr, w_filter, val))


def get_min_obj(my_objs: list, my_attr: str, w_filter: bool = False, val: float = 0.0) -> float:
    return min(_get_map_values(my_objs, my_attr, w_filter, val))


def get_mean_obj(my_objs: list, my_attr: str, w_filter: bool = False, val: float = 0.0) -> float:
    return mean(_get_map_values(my_objs, my_attr, w_filter, val))


def get_mode_obj(my_objs: list, my_attr: str, w_filter: bool = False, val: float = 0.0) -> float:
    return mean(_get_map_values(my_objs, my_attr, w_filter, val))


def get_mean_obj(my_objs: list, my_attr: str, w_filter: bool = False, val: float = 0.0) -> float:
    return mean(_get_map_values(my_objs, my_attr, w_filter, val))


def get_median_obj(my_objs: list, my_attr: str, w_filter: bool = False, val: float = 0.0) -> float:
    return median(_get_map_values(my_objs, my_attr, w_filter, val))


def get_mode_obj(my_objs: list, my_attr: str, w_filter: bool = False, val: float = 0.0) -> float:
    try:
        values = _get_map_values(my_objs, my_attr, w_filter, val)
        data = mode(values)
        if values.count(data) == 1:
            raise StatisticsError
        return data
    except StatisticsError:
        raise


def get_stdev_obj(my_objs: list, my_attr: str, w_filter: bool = False, val: float = 0.0) -> float:
    return stdev(_get_map_values(my_objs, my_attr, w_filter, val))


def get_variance_obj(my_objs: list, my_attr: str, w_filter: bool = False, val: float = 0.0) -> float:
    return variance(_get_map_values(my_objs, my_attr, w_filter, val))


def get_matching_value_obj(my_objs: list, my_attr: str, value: float) -> list:
    return list(filter(lambda x: getattr(x, my_attr) == value, my_objs))
