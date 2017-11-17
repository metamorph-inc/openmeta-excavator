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
    #--------Length-----------------------------------------------
    bucketCyl_uri = 'Excavator_.upper_cyl.cylLength'
    filter.append(bucketCyl_uri)
    armCyl_uri = 'Excavator_.armCylinder.cylLength'
    filter.append(armCyl_uri)
    boomCyl_uri = 'Excavator_.boomCylL.cylLength'
    filter.append(boomCyl_uri)
    #--------Normalized Length------------------------------------
    boomCylLength_uri = 'Excavator_.boomCylL_Length_unit'
    filter.append(boomCylLength_uri)    
    armCylLength_uri = 'Excavator_.armCyl_Length_unit'
    filter.append(armCylLength_uri)    
    bucketCylLength_uri = 'Excavator_.bucketCyl_Length_unit'
    filter.append(bucketCylLength_uri)
    
    #--------Pressure---------------------------------------------
    boomCylLPressureA_uri = 'Excavator_.boomCylLPressure_a'
    filter.append(boomCylLPressureA_uri)    
    armCylPressureA_uri = 'Excavator_.armCylPressure_a'
    filter.append(armCylPressureA_uri)
    bucketCylPressureA_uri = 'Excavator_.bucketCylPressure_a'
    filter.append(bucketCylPressureA_uri)
    #--------Reach------------------------------------------------
    reachY_uri = 'Excavator_.yDistance'
    filter.append(reachY_uri)
    max_reach_uri = 'Excavator_.xDistance'
    filter.append(max_reach_uri)
    #--------State------------------------------------------------
    State_uri = 'Excavator_.State'
    filter.append(State_uri)
    #--------Cylinder Length Set Point----------------------------
    desiredBoom_uri = 'BoomCombiTable.y1'
    filter.append(desiredBoom_uri)
    desiredArm_uri = 'armCombiTable.y1'
    filter.append(desiredArm_uri)
    desiredBucket_uri = 'bucketCombiTable.y1'
    filter.append(desiredBucket_uri)
    tol_uri = 'Excavator_.cylinder_position_tolerance'
    #--------Cylinder Length Position Tolerance------------------
    filter.append(tol_uri)

    #---------------------------------------------------------------------------------
    #                  Processing
    #---------------------------------------------------------------------------------
    # loads results with the filtered out variables (and 'time' which is default)
    pp = PostProcess(mat_file_name, filter)   
    
    #---------------------------------------------------------------------------------
    #                  CYCLE TIME
    #---------------------------------------------------------------------------------
    initTime = pp.get_index_from_time(1) #ignore data while system falls into place.    
    BeginCycle = pp.get_time(State_uri, 2)
    print 'BeginCycle : {0}'.format(BeginCycle)
    nextState = pp.get_time(State_uri, 3)
    CycleIndex = pp.get_index_from_time(nextState)
    EndCycle = pp.get_time(State_uri,2,1e-4,1e-4,CycleIndex+1)
    print 'EndCycle : {0}'.format(EndCycle)
    if EndCycle != -1:
        cycleTime = EndCycle - BeginCycle
    else: cycleTime = pp.delta_t(0,-1)
    print 'Cycle Time : {0}'.format(cycleTime)
    
    #----------------------------------------------------------------------
    #             Rise time, Overshoot, Settling Time
    #----------------------------------------------------------------------
    numStates = pp.last_value(State_uri)    
    enterState_time = 1
    maxBoomOvershoot = 0;
    maxArmOvershoot = 0;
    maxBucketOvershoot = 0;
    maxBoomRiseTime = 0;
    maxArmRiseTime =0;
    maxBucketRiseTime = 0;
    maxBoomSettleTime = 0;
    maxArmSettleTime = 0;
    maxBucketSettleTime =0;
    
    print 'Number of states : {0}'.format(numStates)
    for i in xrange(1, int(numStates)+1):
        print 'in for loop:{0}'.format(i)
        enter_index = pp.get_index_from_time(enterState_time)
        print 'Enter state time:{0}'.format(enterState_time)
        print 'Enter state index:{0}'.format(enter_index)
        desiredBoom = pp.get_data_by_time(desiredBoom_uri,enterState_time+.001)
        print 'desiredBoom:{0}'.format(desiredBoom)
        desiredArm = pp.get_data_by_time(desiredArm_uri, enterState_time + .001)
        desiredBucket = pp.get_data_by_time(desiredBucket_uri, enterState_time + .001)
        
        exitState_time = pp.get_time(State_uri,i+1, 1e-4, 1e-4)
        if exitState_time != -1:
            exit_index = pp.get_index_from_time(exitState_time)
        else: 
            exit_index = -1
        print 'Exit state time:{0}'.format(exitState_time)
        print 'Exit state index:{0}'.format(exit_index)
        
        
        #---- Rise Time -------------
        preBoom = pp.get_data_by_time(desiredBoom_uri, enterState_time)
        print 'pre boom:{0}'.format(preBoom)
        if preBoom[0] != desiredBoom[0]:
            boomRiseTime = findRiseTime(pp, boomCylLength_uri, desiredBoom[0], enter_index, exit_index)
            if maxBoomRiseTime<boomRiseTime:
                maxBoomRiseTime = boomRiseTime     
        print 'maxBoomRiseTime:{0}'.format(maxBoomRiseTime)

        preArm = pp.get_data_by_time(desiredArm_uri, enterState_time)
        print 'pre Arm:{0}'.format(preArm)
        if preArm[0] != desiredArm[0]:
            armRiseTime = findRiseTime(pp, armCylLength_uri, desiredArm[0], enter_index, exit_index)
            if maxArmRiseTime<armRiseTime:
                maxArmRiseTime = armRiseTime  
        print 'maxArmRiseTime:{0}'.format(maxArmRiseTime)
                
        preBucket = pp.get_data_by_time(desiredBucket_uri, enterState_time)
        print 'pre Bucket:{0}'.format(preBucket)
        if preBucket[0] != desiredBucket[0]:
            bucketRiseTime = findRiseTime(pp, bucketCylLength_uri, desiredBucket[0], enter_index, exit_index)
            if maxBucketRiseTime<bucketRiseTime:
                maxBucketRiseTime = bucketRiseTime 
        print 'maxBucketRiseTime:{0}'.format(maxBucketRiseTime)
        
        #---- Overshoot -------------
        boomOvershoot = findOvershoot(pp,boomCylLength_uri, desiredBoom[0], enter_index, exit_index)
        print'BoomOvershoot:{0}'.format(boomOvershoot)
        if (boomOvershoot>maxBoomOvershoot):
            maxBoomOvershoot = boomOvershoot
        
        armOvershoot = findOvershoot(pp, armCylLength_uri, desiredArm[0], enter_index, exit_index)
        print'Arm Overshoot:{0}'.format(armOvershoot)
        if (armOvershoot>maxArmOvershoot):
            maxArmOvershoot = armOvershoot
        
        bucketOvershoot = findOvershoot(pp, bucketCylLength_uri, desiredBucket[0], enter_index, exit_index)
        print'Bucket Overshoot:{0}'.format(bucketOvershoot)
        if (bucketOvershoot>maxBucketOvershoot):
            maxBucketOvershoot = bucketOvershoot
            
        enterState_time = exitState_time #get time when next state is entered     
        print 'Enter state time:{0}'.format(enterState_time)
        
        #---- Settling Time -------------        
        tol = pp.get_data_by_index(tol_uri, 1)
        print'tolerance:{0}'.format(tol)
        if preBoom[0] != desiredBoom[0]:
            boomSettleTime = find_first_max_violation_reverse(pp, boomCylLength_uri, desiredBoom[0], tol, enter_index, exit_index)
            if maxBoomSettleTime < boomSettleTime:
                maxBoomSettleTime = boomSettleTime
            print 'Boom settle Time:{}'.format(boomSettleTime)
        
        if preArm[0] != desiredArm[0]:
            armSettleTime = find_first_max_violation_reverse(pp, armCylLength_uri, desiredArm[0], tol, enter_index, exit_index)
            if maxArmSettleTime < armSettleTime:
                maxArmSettleTime = armSettleTime
            print 'Arm settle Time:{}'.format(armSettleTime)
            
        if preBucket[0] != desiredBucket[0] and exit_index!=-1:
            bucketSettleTime = find_first_max_violation_reverse(pp, bucketCylLength_uri, desiredBucket[0], tol, enter_index, exit_index)
            if maxBucketSettleTime < bucketSettleTime:
                maxBucketSettleTime = bucketSettleTime
            print 'Bucket settle Time:{}'.format(bucketSettleTime)
        #elif preBucket[0] != desiredBucket[0] and exit_index==-1: maxBucketSettleTime = pp.delta_t(0, -1)
        
        
        print'------------------------HERE-----------------------------------------'
        
        
    print'Max Boom overshoot:{0}'.format(maxBoomOvershoot)
    print'Max Arm overshoot:{0}'.format(maxArmOvershoot)
    print'Max Bucket overshoot:{0}'.format(maxBucketOvershoot)
    
    print 'Max Boom settle Time:{}'.format(maxBoomSettleTime) 
    print 'Max Arm settle Time:{}'.format(maxArmSettleTime ) 
    print 'Max Bucket settle Time:{}'.format(maxBucketSettleTime) 
    
    maxOvershoot = max(maxBoomOvershoot, maxArmOvershoot, maxBucketOvershoot)
    
    #----------------------------------------------------------------------
    #             Check Relief Valve
    #----------------------------------------------------------------------
    reliefPressure = 100 * 100000;
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
    #how close to relief pressure
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
    #---------------------------------------------------------------------------------
    #                  Metrics
    #---------------------------------------------------------------------------------
    metrics = {}
    metrics.update({'boomCylLength_unit': {'value': pp.get_data_by_time(boomCylLength_uri, pp.global_max_time(boomCylLPressureA_uri))[0], 'unit': 'm'},
                    'armCylLength_unit': {'value': pp.get_data_by_time(armCylLength_uri, pp.global_max_time(armCylPressureA_uri))[0], 'unit': 'm'},
                    'bucketCylLength_unit': {'value': pp.get_data_by_time(bucketCylLength_uri, pp.global_max_time(bucketCylPressureA_uri))[0], 'unit': 'm'},                
                    'boomCylRPressure': {'value': pp.global_abs_max(boomCylLPressureA_uri)*0.00001, 'unit': 'bar'},                    
                    'armCylPressure': {'value': pp.get_local_max(armCylPressureA_uri,initTime,-1)*0.00001, 'unit': 'bar'},	
                    'bucketCylPressure': {'value': pp.global_abs_max(bucketCylPressureA_uri)*0.00001, 'unit': 'bar'},                   				
                    'max_reach':{'value':pp.global_max(max_reach_uri),'unit':'m'},
                    'max_high_reach' : {'value': pp.global_max(reachY_uri), 'unit':'m'},
                    'max_low_reach': {'value': pp.global_min(reachY_uri), 'unit':'m'},
                    'cycle_time':{'value':cycleTime,'unit':'s'},
                    'overshoot':{'value': maxOvershoot, 'unit':'m'},
                    'boomRiseTime':{'value':maxBoomRiseTime, 'unit':'s'},
                    'armRiseTime':{'value':maxArmRiseTime, 'unit':'s'},
                    'bucketRiseTime':{'value':maxBucketRiseTime, 'unit':'s'},
                    'BoomSettlingTime':{'value':maxBoomSettleTime, 'unit':'s'},
                    'ArmSettlingTime':{'value':maxArmSettleTime, 'unit':'s'},
                    'BucketSettlingTime':{'value':maxBucketSettleTime, 'unit':'s'},
                    'BoomCylA_ExceedsRelief': {'value': BoomAExceedsRelief*.00001, 'unit': 'bar'},                    
                    'BoomCylB_ExceedsRelief': {'value': BoomBExceedsRelief*.00001, 'unit': 'bar'},
                    'ArmCylA_ExceedsRelief': {'value': ArmAExceedsRelief*.00001, 'unit': 'bar'},  
                    'ArmCylB_ExceedsRelief': {'value': ArmBExceedsRelief*.00001, 'unit': 'bar'},      
                    'BucketCylA_ExceedsRelief': {'value': BucketAExceedsRelief*.00001, 'unit': 'bar'},
                    'BucketCylB_ExceedsRelief': {'value': BucketBExceedsRelief*.00001, 'unit': 'bar'},
                    'StaticLoad' : {'value': pp.get_data_by_index(Load_uri, minVal), 'unit' : 'kg'},
                    'overloaded_cylinder' : {'value': culprit, 'unit': 'null'},
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
    #pp.store_data_to_csv(bucketCyl_uri, '{0}.csv'.format(bucketCyl_uri), 0, time_inc, numSamples)
    #pp.store_data_to_csv(armCyl_uri, '{0}.csv'.format(armCyl_uri), 0, time_inc, numSamples)
    #pp.store_data_to_csv(boomCyl_uri, '{0}.csv'.format(boomCyl_uri), 0, time_inc, numSamples)
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