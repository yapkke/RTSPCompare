#include <stdio.h>
#include "yuvfile.hh"
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
    
/** \brief Program to count number of frames in a file
 */ 
int main (int argc, char **argv)
{
  int width = 0;
  int height = 0;
  char* filename = NULL;
  int index, c;

  while ((c = getopt (argc, argv, "w:h:")) != -1)
    switch (c)
    {
    case 'w':
      width = atoi(optarg);
      break;
    case 'h':
      height = atoi(optarg);
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
  printf ("YUV File : %s\n", filename);
  
  yuvstream stream(filename, width, height);
  printf("%d frames found\n", stream.frames.size());

  return 0;
}
