# openmeta-excavator
An example OpenMETA model for design space exploration of an excavator.

This model is currently "under restoration" and may not yet work properly.

## Test Benches

### DynamicsTestBench
A simple testbench that does not make use of the cyber tools. 

### DynamicsTestBench_OperatorLoad
This test bench is currently designed to see how much the cylinders deflect under increasing load.

It also serves to examine the torque around the excavator swing axis that may result in tipping.

### DynamicsTestBench_positionTable 
The purpose of this testbench is to sweep through the maximum and minimum reach of the excavator by extending the arm and boom cylinders to their max and min. 

DynamicsTestBench_OperatorROM has the same purpose with the addition of being able to loop through the dig cycle.

### DynamicsTestBench_positionTable2
The idea of this test bench is to 1) go to max reach 2)Scoop 3) lift at max reach

Normally the arm retracts to scoop more dirt, this also reduces the force required to lift the load. 