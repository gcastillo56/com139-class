from analysis.analyzer import *


def report_all_by_field_obj(my_objs: list, my_field: str) -> None:
    print('\n === Report for %s field ===' % my_field)
    max_time = get_max_obj(my_objs, my_field)
    min_time = get_min_obj(my_objs, my_field)
    print('Max %s: %5.3f by %s' % (my_field, max_time, objects_as_str(get_matching_value_obj(my_objs, my_field, max_time))))
    print('Min %s: %5.3f by %s' % (my_field, min_time, objects_as_str(get_matching_value_obj(my_objs, my_field, min_time))))
    print('Mean %s: %5.3f' % (my_field, get_mean_obj(my_objs, my_field)))
    print('Median %s: %5.3f' % (my_field, get_median_obj(my_objs, my_field)))
    print('Mode %s: %5.3f' % (my_field, get_mode_obj(my_objs, my_field)))
    print('Stdev %s: %5.3f' % (my_field, get_stdev_obj(my_objs, my_field)))
    print('Variance %s: %5.3f' % (my_field, get_variance_obj(my_objs, my_field)))


def report_all_by_ts(my_ts: list, my_label: str, total_time: float) -> None:
    # print_ts(my_ts, my_label)
    plot_ts(my_ts, my_label)
    print('Min queue: %4.3f' % get_min_ts(my_ts))
    print('Max queue: %4.3f' % get_max_ts(my_ts))
    evolution_bar_ts(my_ts, my_label)
    service_vals = cumulative_time_ts(my_ts, my_label)
    percent_vals = get_bin_percent_ts(service_vals, total_time, my_label)
    hist_bar_ts(my_ts, 'value', my_label)
