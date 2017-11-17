#ifndef _controller_sl_H_
#define _controller_sl_H_

#ifndef NO_MATH_H
#include <math.h>
#endif
#ifndef min
#define min(x,y) (((x)>(y)) ? (y) : (x))
#endif

#ifndef sign
#define sign(x) ( ((x) > 0.0) ? (1.0)  : (((x) < 0.0 ) ? (-1.0) : (0.0)) )
#endif

#ifndef max
#define max(x,y) (((x)<(y)) ? (y) : (x))
#endif



#ifndef proportionalGain_100000003_context_GUARD
#define proportionalGain_100000003_context_GUARD
typedef struct {
  double Gain106;
} proportionalGain_100000003_context;
#endif

#ifndef controller_100000002_context_GUARD
#define controller_100000002_context_GUARD
typedef struct {
  proportionalGain_100000003_context proportionalGain_100000003_class_member0;
} controller_100000002_context;
#endif

#ifndef proportionalGain_100000003_context_GUARD
#define proportionalGain_100000003_context_GUARD
typedef struct {
  double Gain106;
} proportionalGain_100000003_context;
#endif

/* SIMPLIFIED PROGRAM CONTEXT */
typedef controller_100000002_context controller_context;

void controller_100000002_main( controller_100000002_context *context, double Desired_L_1_2, double measured_L_1_3, double *valve_Flowfraction_1_4 );
void controller_100000002_init( controller_100000002_context *context );



/* SIMPLIFIED PROGRAM FUNCTIONS */
void controller_main( controller_100000002_context *context, double Desired_L_1_2, double measured_L_1_3, double *valve_Flowfraction_1_4 );
void controller_init( controller_100000002_context *context );
#endif
