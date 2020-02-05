from statistics import *

# Time series methods


def print_ts(my_list: list, label: str = '') -> None:
    data_elements = lambda x: str('%8.3f - %d' % (x['time'], x['value']))
    data = list(map(data_elements, my_list))
    if label != '':
        print('=== %s ===' % label)
    print(*data, sep="\n")


def get_max_ts(my_list: list) -> float:
    seq = [x['value'] for x in my_list]
    return max(seq)


def get_min_ts(my_list: list) -> float:
    seq = [x['value'] for x in my_list]
    return min(seq)


# Object methods

def print_obj_list(my_list: list, my_method: str, label: str = '') -> None:
    report = lambda x: getattr(x, my_method)()
    reporter = list(map(report, my_list))
    if label != '':
        print('=== %s ===' % label)
    print(*reporter, sep="\n")


def _get_map_values(my_objs: list, my_attr: str) -> map:
    values = lambda x: getattr(x, my_attr)
    return map(values, my_objs)


def objects_as_str(my_objs: list) -> str:
    strings = lambda x: str(x)
    return str(list(map(strings, my_objs)))


def get_max_obj(my_objs: list, my_attr: str) -> float:
    return max(_get_map_values(my_objs, my_attr))


def get_min_obj(my_objs: list, my_attr: str) -> float:
    return min(_get_map_values(my_objs, my_attr))


def get_mean_obj(my_objs: list, my_attr: str) -> float:
    return mean(_get_map_values(my_objs, my_attr))


def get_mode_obj(my_objs: list, my_attr: str) -> float:
    return mean(_get_map_values(my_objs, my_attr))


def get_mean_obj(my_objs: list, my_attr: str) -> float:
    return mean(_get_map_values(my_objs, my_attr))


def get_median_obj(my_objs: list, my_attr: str) -> float:
    return median(_get_map_values(my_objs, my_attr))


def get_mode_obj(my_objs: list, my_attr: str) -> float:
    return mode(_get_map_values(my_objs, my_attr))


def get_stdev_obj(my_objs: list, my_attr: str) -> float:
    return stdev(_get_map_values(my_objs, my_attr))


def get_variance_obj(my_objs: list, my_attr: str) -> float:
    return variance(_get_map_values(my_objs, my_attr))


def get_matching_value_obj(my_objs: list, my_attr: str, value: float) -> list:
    return list(filter(lambda x: getattr(x, my_attr) == value, my_objs))



