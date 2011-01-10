#include <stdio.h>
#include "yuvfile.hh"
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
    
/** \brief Program to calculate extend stream
 */ 
int main (int argc, char **argv)
{
  int width = 0;
  int height = 0;
  char* reffile = NULL;
  char* filename = NULL;
  char* outputfile=NULL;
  int index, c;

  while ((c = getopt (argc, argv, "w:h:r:o:")) != -1)
    switch (c)
    {
    case 'w':
      width = atoi(optarg);
      break;
    case 'h':
      height = atoi(optarg);
      break;
    case 'o':
      outputfile = optarg;
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
  printf ("Output File : %s\n", outputfile);
  
  yuvstream ref(reffile, width, height);
  yuvstream stream(filename, width, height);

  streampsnr ps = stream.avPSNR(&ref);
  printf("Initial\n\tSize : %d\n\tIdentical Frames : %d\n\tAverage PSNR : %2.2f\n",
	 stream.frames.size(),ps.identical, ps.average);
  
  printf("Extending stream\n");
  while (ref.frames.size() > stream.frames.size())
  {
    ps = stream.avPSNR(&ref);
    printf("\tStream with %d identical frames & PSNR %2.2f"
	   " extended to %d by duplicating frame %d\n",
	   ps.identical, ps.average,
	   stream.frames.size(),
	   stream.maximal_extend(&ref));
  }

  ps = stream.avPSNR(&ref);
  printf("Initial\n\tSize : %d\n\tIdentical Frames : %d\n\tAverage PSNR : %2.2f\n",
	 stream.frames.size(),ps.identical, ps.average);

  stream.write_to_file(outputfile);
  
  return 0;
}
