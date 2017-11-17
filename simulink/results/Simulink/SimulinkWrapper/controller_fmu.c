// define class name and unique id
#define MODEL_IDENTIFIER controller
#define MODEL_GUID "{d779210e-dc6f-47de-90ba-5b2cb720d380}"

// define model size
#define NUMBER_OF_REALS 3
#define NUMBER_OF_INTEGERS 0
#define NUMBER_OF_BOOLEANS 0
#define NUMBER_OF_STRINGS 0
#define NUMBER_OF_STATES 0
#define NUMBER_OF_EVENT_INDICATORS 0

// include fmu header files, typedefs and macros
#include "fmuTemplate.h"
#include "controller_sl.h"

#define Desired_L_1_2_ 	2
#define measured_L_1_3_ 	3
#define valve_Flowfraction_1_4_ 	4

static controller_context context;

// called by fmiInstantiateModel
// Set values for all variables that define a start value
// Settings used unless changed by fmiSetX before fmiInitialize
void setStartValues(ModelInstance *comp) {
	r(Desired_L_1_2_) = 0.0;
	r(measured_L_1_3_) = 0.0;
	r(valve_Flowfraction_1_4_) = 0.0;

}

// called by fmiInitialize() after setting eventInfo to defaults
// Used to set the first time event, if any.
void initialize(ModelInstance* comp, fmiEventInfo* eventInfo) {
	eventInfo->upcomingTimeEvent   = fmiFalse;
	eventInfo->nextEventTime       = 0;
}
// called by fmiGetReal, fmiGetContinuousStates and fmiGetDerivatives
fmiReal getReal(ModelInstance* comp, fmiValueReference vr){
	switch (vr) {
		case Desired_L_1_2_	: return r(Desired_L_1_2_);
		case measured_L_1_3_	: return r(measured_L_1_3_);
		case valve_Flowfraction_1_4_	: return r(valve_Flowfraction_1_4_);
		default: return 0.0;
	}
}

// called by fmiEventUpdate() after setting eventInfo to defaults
void eventUpdate(ModelInstance* comp, fmiEventInfo* eventInfo) {
} 

// include code that implements the FMI based on the above definitions
#include "fmuTemplate.c"
