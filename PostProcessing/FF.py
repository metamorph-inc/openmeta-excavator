import sys
import os
from common import PostProcess, update_metrics_in_report_json
from common import read_limits, check_limits_and_add_to_report_json
from common.stability import *


def main():
    mat_file_name = sys.argv[1]
    if not os.path.exists(mat_file_name):
        raise IOError('Given result file does not exist: {0}'.format(sys.argv[1]))

    ## First limit part
    limit_dict, filter = read_limits()
    ## End of first limit part

    ## Post processing part
    #--------Angle-----------------------------------------------
    boomAngle_uri = 'Excavator_.boomAngle'
    filter.append(boomAngle_uri)

    #---------------------------------------------------------------------------------
    #                  Processing
    #---------------------------------------------------------------------------------
    # loads results with the filtered out variables (and 'time' which is default)
    pp = PostProcess(mat_file_name, filter)   
    #---------------------------------------------------------------------------------
    #                  change in angle during time slice
    #---------------------------------------------------------------------------------
    startAngle = pp.get_data_by_time(boomAngle_uri, 1)
    endAngle = pp.get_data_by_time(boomAngle_uri,2)
    deltaAngle = endAngle[0] - startAngle[0]

    #---------------------------------------------------------------------------------
    #                  Metrics
    #---------------------------------------------------------------------------------
    metrics = {}
    metrics.update({'deltaAngle':{'value':deltaAngle, 'unit':'rad'},
                    })

    cwd = os.getcwd()
    os.chdir('..')
    # print 'Plot saved to : {0}'.format(pp.save_as_svg(vehicle_speed,
                                                      # pp.global_abs_max(vehicle_speed),
                                                      # 'VehicleSpeed',
                                                      # 'max(FTP_Driver.driver_bus.vehicle_speed)',
                                                      # 'kph'))
    dur = 40
    time_inc = .1
    numSamples = int(dur/time_inc)
    #pp.store_data_to_csv(boomAngle_uri, '{0}.csv'.formatboomAngle_uri), 0, time_inc, numSamples)
    #pp.store_data_to_csv(armCyl_uri, '{0}.csv'.format(armCyl_uri), 0, time_inc, numSamples)
    #pp.store_data_to_csv(boomCyl_uri, '{0}.csv'.format(boomCyl_uri), 0, time_inc, numSamples)
    #pp.store_data_to_csv(boomCylLength_uri, '{0}.csv'.format(boomCylLength_uri), 0, time_inc, numSamples)
    #pp.store_data_to_csv(armCylLength_uri, '{0}.csv'.format(armCylLength_uri), 0, time_inc, numSamples)
    #pp.store_data_to_csv(bucketCylLength_uri, '{0}.csv'.format(bucketCylLength_uri), 0, time_inc, numSamples)
    #pp.store_data_to_csv(boomCylRPressure_uri, '{0}.csv'.format(boomCylRPressure_uri), 0, 0.1, dur)
    #pp.store_data_to_csv(arm_ang_vel_uri, '{0}.csv'.format(arm_ang_vel_uri), 0, 0.1, dur)
    #pp.store_data_to_csv(max_Y_uri, '{0}.csv'.format(max_Y_uri), 0, 0.1, dur)
    #pp.store_data_to_csv(max_reach_uri, '{0}.csv'.format(max_reach_uri), 0, 0.1, dur)
    #pp.store_data_to_csv(State_uri, '{0}.csv'.format(State_uri), 0, 0.1, dur)
    ## end of postprocessing part

    ## Second limit part
    check_limits_and_add_to_report_json(pp, limit_dict)
    update_metrics_in_report_json(metrics)
    ## end of Second limit part
    os.chdir(cwd)

if __name__ == '__main__':
    root_dir = os.getcwd()
    try:
        main()
    except:
        os.chdir(root_dir)
        import traceback
        trace = traceback.format_exc()
        # Generate this file on failed executions, https://github.com/scipy/scipy/issues/1840
        with open(os.path.join('..', '_POST_PROCESSING_FAILED.txt'), 'wb') as f_out:
            f_out.write(trace)