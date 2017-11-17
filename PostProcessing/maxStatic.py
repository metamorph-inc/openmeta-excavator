import sys
import os
from common import PostProcess, update_metrics_in_report_json
from common import read_limits, check_limits_and_add_to_report_json


def main():
    mat_file_name = sys.argv[1]
    if not os.path.exists(mat_file_name):
        raise IOError('Given result file does not exist: {0}'.format(sys.argv[1]))

    ## First limit part
    limit_dict, filter = read_limits()
    ## End of first limit part

    ## Post processing part
    bucketCylLength_uri = 'Excavator_.bucketCylLength_unit'
    filter.append(bucketCylLength_uri)
    armCylLength_uri = 'Excavator_.armCylLength_unit'
    filter.append(armCylLength_uri)
    boomCylLength_uri = 'Excavator_.boomCylLength_unit'
    filter.append(boomCylLength_uri)
    #--------------------------------------
    boomCylLPressureA_uri = 'Excavator_.boomCylLPressure_a'
    filter.append(boomCylLPressureA_uri)    
    boomCylLPressureB_uri = 'Excavator_.boomCylLPressure_b'
    filter.append(boomCylLPressureB_uri)    
    #--------
    armCylPressureA_uri = 'Excavator_.armCylPressure_a'
    filter.append(armCylPressureA_uri)
    armCylPressureB_uri = 'Excavator_.armCylPressure_b'
    filter.append(armCylPressureB_uri)
    #--------
    bucketCylPressureA_uri = 'Excavator_.bucketCylPressure_a'
    filter.append(bucketCylPressureA_uri)
    bucketCylPressureB_uri = 'Excavator_.bucketCylPressure_b'
    filter.append(bucketCylPressureB_uri)
    #--------------------------------------
    Load_uri = 'Excavator_.Load'
    filter.append(Load_uri)
    #--------------------------------------

    # loads results with the filtered out variables (and 'time' which is default)
    pp = PostProcess(mat_file_name, filter)
    
    reliefPressure = 100 * 100000;
    initTime = pp.get_index_from_time(1)
    BoomCylA_ExceedsReliefindex = pp.find_first_max_violation(boomCylLPressureA_uri, reliefPressure, start_index=initTime)
    BoomCylB_ExceedsReliefindex = pp.find_first_max_violation(boomCylLPressureB_uri, reliefPressure, start_index=initTime)
    ArmCylA_ExceedsReliefindex = pp.find_first_max_violation(armCylPressureA_uri, reliefPressure, start_index=initTime)
    ArmCylB_ExceedsReliefindex = pp.find_first_max_violation(armCylPressureB_uri, reliefPressure, start_index=initTime)
    BucketCylA_ExceedsReliefindex = pp.find_first_max_violation(bucketCylPressureA_uri, reliefPressure, start_index=initTime)
    BucketCylB_ExceedsReliefindex = pp.find_first_max_violation(bucketCylPressureB_uri, reliefPressure, start_index=initTime)
    print 'BoomCylA_ExceedsRelief:{0}'.format(BoomCylA_ExceedsReliefindex)
    print 'BoomCylB_ExceedsRelief:{0}'.format(BoomCylB_ExceedsReliefindex)
    print 'ArmCylA_ExceedsRelief:{0}'.format(ArmCylA_ExceedsReliefindex)
    print 'ArmCylB_ExceedsRelief:{0}'.format(ArmCylB_ExceedsReliefindex)
    print 'BucketCylA_ExceedsRelief:{0}'.format(BucketCylA_ExceedsReliefindex)
    print 'BucketCylB_ExceedsRelief:{0}'.format(BucketCylB_ExceedsReliefindex)
    
    BoomAExceedsRelief = pp.global_max(boomCylLPressureA_uri) - reliefPressure
    BoomBExceedsRelief = pp.global_max(boomCylLPressureB_uri) - reliefPressure
    ArmAExceedsRelief = pp.global_max(armCylPressureA_uri) - reliefPressure
    ArmBExceedsRelief = pp.global_max(armCylPressureB_uri) - reliefPressure
    BucketAExceedsRelief = pp.global_max(bucketCylPressureA_uri) - reliefPressure
    BucketBExceedsRelief = pp.global_max(bucketCylPressureB_uri) - reliefPressure
    
    
    
    a = {'BoomCylA':BoomCylA_ExceedsReliefindex, 'BoomCylB':BoomCylB_ExceedsReliefindex, 'ArmCylA':ArmCylA_ExceedsReliefindex, 'ArmCylB':ArmCylB_ExceedsReliefindex, 'BucketCylA':BucketCylA_ExceedsReliefindex, 'BucketCylB':BucketCylB_ExceedsReliefindex}
    print 'a:{0}'.format(a)
    #minVal = 0
    #culprit = 'none'
    if any(v>0 for v in a.itervalues()):
        minVal = min(el for el in a.itervalues() if el>0)
        culprit =[k for k, v in a.iteritems() if v==minVal]
    else: 
        minVal = pp.delta_t(0, -1)
        culprit = 'none'
    
    print 'minVal:{0}'.format(minVal)
    
    print 'Cylinder that exceeded pressure is: {0}'.format(culprit)
    
    max_p_time = pp.global_max_time(boomCylLPressureA_uri)
    #max_p_time = pp.global_max_time(armCylPressure_uri)
    #max_p_time = pp.global_max_time(bucketCylPressure_uri)
    #print 'Maximum pressure obtained at : {0}'.format(max_p_time)
  
    # time = pp.get_time(State_uri,2)
    # print 'First entry of State 2 at : {0}'.format(time)
    
    # index = pp.get_index_from_time(time)
    # print 'first entry of state2 index : {0}'.format(index)
    
    # time2 = pp.get_time(State_uri, 4)
    # print 'Exit of state 2 at : {0}'.format(time2)
    
    # index2 = pp.get_index_from_time(time2)
    # print 'Exit of state 2 index : {0}'.format(index2)    
    
    # time3 = pp.get_time(State_uri,2,1e-4,1e-4,index2+1)
    # print '2nd entry of state 2 : {0}'.format(time3)
    
    # index3 = pp.get_index_from_time(time3)
    # print 'index of second entry of state 2 : {0}'.format(index3)    
    
    # dt = pp.delta_t(index, index3)
    # print 'Cycle Time : {0}'.format(dt)
    armPressure = pp.get_local_max(armCylPressureA_uri,initTime,-1)*0.00001
    #print 'arm Pressure : {0}'.format(armPressure)
    
    
	
    metrics = {}
    metrics.update({'BoomCylA_ExceedsRelief': {'value': BoomAExceedsRelief*.00001, 'unit': 'bar'},
                    'StaticLoad' : {'value': pp.get_data_by_index(Load_uri, minVal), 'unit' : 'kg'},
                    'overloaded_cylinder' : {'value': culprit, 'unit': 'null'},
                    'BoomCylB_ExceedsRelief': {'value': BoomBExceedsRelief*.00001, 'unit': 'bar'},
                    'ArmCylA_ExceedsRelief': {'value': ArmAExceedsRelief*.00001, 'unit': 'bar'},  
                    'ArmCylB_ExceedsRelief': {'value': ArmBExceedsRelief*.00001, 'unit': 'bar'},      
                    'BucketCylA_ExceedsRelief': {'value': BucketAExceedsRelief*.00001, 'unit': 'bar'},
                    'BucketCylB_ExceedsRelief': {'value': BucketBExceedsRelief*.00001, 'unit': 'bar'},
                    #'arm_angVel' : {'value': pp.global_abs_max(arm_ang_vel_uri), 'unit':'rads/s'},					
                    #'max_reach':{'value':pp.global_max(max_reach_uri),'unit':'m'},
                    #'max_high_reach' : {'value': pp.global_max(max_Y_uri), 'unit':'m'},
                    #'max_low_reach': {'value': pp.global_min(max_Y_uri), 'unit':'m'}
                    # 'cycle_time': {'value': dt, 'unit':'s'},
                    #'swing_speed': {'value': pp.last_value(swing_uri), 'unit':'rad/s'},
                    })

    cwd = os.getcwd()
    os.chdir('..')
    # print 'Plot saved to : {0}'.format(pp.save_as_svg(vehicle_speed,
                                                      # pp.global_abs_max(vehicle_speed),
                                                      # 'VehicleSpeed',
                                                      # 'max(FTP_Driver.driver_bus.vehicle_speed)',
                                                      # 'kph'))
    dur = 100
    # pp.store_data_to_csv(bucketCylLength_uri, '{0}.csv'.format(bucketCylLength_uri), 0, 0.1, dur)
    # pp.store_data_to_csv(armCylLength_uri, '{0}.csv'.format(armCylLength_uri), 0, 0.1, dur)
    # pp.store_data_to_csv(boomCylLength_uri, '{0}.csv'.format(boomCylLength_uri), 0, 0.1, dur)
    # pp.store_data_to_csv(boomCylRPressure_uri, '{0}.csv'.format(boomCylRPressure_uri), 0, 0.1, dur)
    # pp.store_data_to_csv(arm_ang_vel_uri, '{0}.csv'.format(arm_ang_vel_uri), 0, 0.1, dur)
    # pp.store_data_to_csv(max_Y_uri, '{0}.csv'.format(max_Y_uri), 0, 0.1, dur)
    # pp.store_data_to_csv(max_reach_uri, '{0}.csv'.format(max_reach_uri), 0, 0.1, dur)
    # pp.store_data_to_csv(State_uri, '{0}.csv'.format(State_uri), 0, 0.1, dur)
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