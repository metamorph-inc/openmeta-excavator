import sys
import os
import numpy


def find_first_max_violation_reverse(self, name, value, tol,start_index=0, end_index=-1):
    """ Starting from end_index it looks for the first index where the
    time-series has a value greater than value. Then finds the time between that index and when the step occured.

    If it never occurs, it returns -1
    """

    time_series = self.data_array(name)[:end_index]
    i = end_index
    for x in reversed(time_series):            
        if x>value+tol or x<value-tol:
            time = self.delta_t(start_index, i)
            print'x:{0}'.format(time)
            return time
        i-=1

    return -1

def findRiseTime(pp, uri, desired, enter_index, exit_index):
    
    current = pp.get_data_by_index(uri, enter_index)
    print'current:{0}'.format(current)
    stepSize = desired - current
    print'Step Size:{0}'.format(stepSize)
    rise_start = pp.get_time_for_crossing(uri, current+stepSize*.1, enter_index, exit_index)
    print'rise start:{0}'.format(rise_start)
    rise_end = pp.get_time_for_crossing(uri, current+stepSize*.9, enter_index, exit_index)
    print'rise end:{0}'.format(rise_end)
    if rise_end!= -1:
        riseTime = rise_end - rise_start         
    else:
        riseTime = pp.delta_t(0, -1) - rise_start
    print 'Rise time:{0}'.format(riseTime)
    return riseTime 
                

def findOvershoot( pp,uri, desired, enter_index, exit_index):       
    maxovershoot = 0;
    cross_time = pp.get_time_for_crossing(uri, desired, enter_index, exit_index)
    print 'cross time:{0}'.format(cross_time)
    if cross_time != -1:
        cross_index = pp.get_index_from_time(cross_time)
        print 'cross index:{0}'.format(cross_index)
        localmax = pp.get_local_max(uri, cross_index, exit_index-1)
        print 'max:{0}'.format(localmax)
        localmin = pp.get_local_min(uri, cross_index, exit_index-1)
        print 'min:{0}'.format(localmin)  
        overshoot = abs(localmax - desired)
        print 'overshoot:{0}'.format(overshoot)
        undershoot = abs(localmin - desired)
        print 'undershoot:{0}'.format(undershoot)
        absmax = max(overshoot, undershoot)
        print 'absmax:{0}'.format(absmax)            
        return absmax