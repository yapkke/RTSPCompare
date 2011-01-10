#include <stdio.h>
#include "yuvfile.hh"
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
    
/** \brief Program to calculate PSNR of stream
 */ 
int main (int argc, char **argv)
{
  int width = 0;
  int height = 0;
  char* reffile = NULL;
  char* filename = NULL;
  int index, c;

  while ((c = getopt (argc, argv, "w:h:r:")) != -1)
    switch (c)
    {
    case 'w':
      width = atoi(optarg);
      break;
    case 'h':
      height = atoi(optarg);
      break;
    case 'r':
      reffile = optarg;
      break;
    case '?':
      if (optopt == 'w' || optopt == 'h')
	fprintf (stderr, "Option -%c requires an argument.\n", optopt);
      else if (isprint (optopt))
	fprintf (stderr, "Unknown option `-%c'.\n", optopt);
      else
	fprintf (stderr,
		 "Unknown option character `\\x%x'.\n",
		 optopt);
      return 1;
    default:
      abort ();
    }

  index = optind;
  if (index < argc)
    filename = argv[index];
     
  printf ("Width = %d, Height = %d\n", width, height);
  printf ("Reference : %s\n", reffile);
  printf ("YUV File : %s\n", filename);
  
  yuvstream ref(reffile, width, height);
  yuvstream stream(filename, width, height);

  int findex = 0;
  std::list<yuvpsnr> psnr = stream.psnr(&ref);
  for (std::list<yuvpsnr>::iterator i = psnr.begin(); 
       i != psnr.end(); i++)
  {
    printf("Frame %d:\tY-PSNR: %2.2f\tU-PSNR: %2.2f\tV-PSNR: %2.2f\n",
	   findex, i->y, i->u, i->v);
    findex++;
  }
  streampsnr sp = yuvstream::avPSNR(psnr);
  printf("Number of Identical Frames : %d\n"
	 "Average PSNR : %2.2f (%2.2f,%2.2f,%2.2f)\n", 
	 sp.identical, sp.psnr.average(),
	 sp.psnr.y, sp.psnr.u, sp.psnr.v);

  return 0;
}
