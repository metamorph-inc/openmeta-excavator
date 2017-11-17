#include "controller_sl.h"



/* SIMPLIFIED PROGRAM FUNCTIONS */
void controller_main( controller_100000002_context *context, double Desired_L_1_2, double measured_L_1_3, double *valve_Flowfraction_1_4 ) {
  controller_100000002_main( context, Desired_L_1_2, measured_L_1_3, valve_Flowfraction_1_4 );
}

void controller_init( controller_100000002_context *context ) {
  controller_100000002_init( context );
}

void proportionalGain_100000003_main( proportionalGain_100000003_context *context, double Desired_L_2, double measured_L_3, double *valve_Flowfraction_4 );
void proportionalGain_100000003_init( proportionalGain_100000003_context *context );


void controller_100000002_main( controller_100000002_context *context, double Desired_L_1_2, double measured_L_1_3, double *valve_Flowfraction_1_4 )
{
  proportionalGain_100000003_main( &( *context ).proportionalGain_100000003_class_member0, Desired_L_1_2, measured_L_1_3, &*valve_Flowfraction_1_4 );
}

void controller_100000002_init( controller_100000002_context *context )
{
  proportionalGain_100000003_init( &( *context ).proportionalGain_100000003_class_member0 );
}

void proportionalGain_100000003_main( proportionalGain_100000003_context *context, double Desired_L_2, double measured_L_3, double *valve_Flowfraction_4 )
{
  double sig_0;

  sig_0 = Desired_L_2 - measured_L_3;
  *valve_Flowfraction_4 = sig_0 * ( *context ).Gain106;
}

void proportionalGain_100000003_init( proportionalGain_100000003_context *context )
{
  ( *context ).Gain106 = 1.000000000000000000000000000000000000000;
}

