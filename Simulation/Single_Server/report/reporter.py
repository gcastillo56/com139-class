from analysis.analyzer import *
from simulation.config import *
from assets.status import Status
# TODO: Create report of multiple executions


def report_all_by_field_obj(my_objs: list, my_field: str, w_filter: bool = False, val: float = 0.0) -> None:
    print('\n === Report for %s field ===' % my_field)
    is_status = isinstance(getattr(my_objs[0], my_field), Status)
    if not is_status:
        max_time = get_max_obj(my_objs, my_field, w_filter, val)
        min_time = get_min_obj(my_objs, my_field, w_filter, val)
        print('Max %s: %5.3f by %s' %
              (my_field, max_time, objects_as_str(get_matching_value_obj(my_objs, my_field, max_time))))
        print('Min %s: %5.3f by %s' %
              (my_field, min_time, objects_as_str(get_matching_value_obj(my_objs, my_field, min_time))))
        print('Mean %s: %5.3f' % (my_field, get_mean_obj(my_objs, my_field, w_filter, val)))
        print('Median %s: %5.3f' % (my_field, get_median_obj(my_objs, my_field, w_filter, val)))
        try:
            print('Mode %s: %5.3f' % (my_field, get_mode_obj(my_objs, my_field, w_filter, val)))
        except Exception:
            print('No mode found in data')
        print('Stdev %s: %5.3f' % (my_field, get_stdev_obj(my_objs, my_field, w_filter, val)))
        print('Variance %s: %5.3f' % (my_field, get_variance_obj(my_objs, my_field, w_filter, val)))
        # TODO: Calculate the percentage of minimal value
        # TODO: Group std dev customers and display the list
    else:
        print(is_status)
        values = get_map_values(my_objs, my_field)
        print(values)
        # TODO: get a histogram count on every status
        # TODO: graph the histogram
        # TODO: get success rate


def report_all_by_ts(my_ts: list, my_label: str, total_time: float) -> None:
    print('\n === Report for %s resource ===' % my_label)
    if my_ts:
        # print_ts(my_ts, my_label)
        # print('Min queue: %4.3f' % get_min_ts(my_ts))
        print('Max queue: %4.3f' % get_max_ts(my_ts))
        service_vals = get_cumulative_time_ts(my_ts, total_time)
        percent_vals = get_bin_percent_ts(service_vals, total_time, my_label)
        if CREATE_SIM_GRAPHS:
            plot_ts(my_ts, total_time, my_label)
            evolution_bar_ts(my_ts, total_time, my_label)
            cumulative_time_ts(service_vals, my_label)
            hist_bar_ts(my_ts, 'value', my_label)
    else:
        print('%s not used' % my_label)
