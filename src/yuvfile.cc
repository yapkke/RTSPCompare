#include "yuvfile.hh"
#include <stdlib.h>
#include <stdio.h>
#include <cstring>
#include <cmath>

yuvframe::yuvframe(int width_, int height_, 
		   unsigned char* buffer)
{
  width = width_;
  height = height_;
  int pixel = width_*height_;

  y = new unsigned char[pixel];
  memcpy(y, buffer, pixel);
  buffer += pixel;

  u = new unsigned char[(int) pixel/4];
  memcpy(u, buffer, (int) pixel/4);
  buffer += ((int) pixel/4);

  v = new unsigned char[(int) pixel/4];
  memcpy(v, buffer, (int) pixel/4);
}

yuvframe::~yuvframe()
{
  if (y != NULL)
    delete y;
  if (u != NULL)
    delete u;
  if (v != NULL)
    delete v;
}

yuvpsnr yuvframe::psnr(yuvframe* reference)
{
  return yuvpsnr(frame_psnr(y, reference->y, width*height),
		 frame_psnr(u, reference->u, width*height/4),
		 frame_psnr(v, reference->v, width*height/4));
}

double yuvframe::frame_psnr(unsigned char* frame, 
			    unsigned char* reference, int size)
{
  double errSq = 0;
  for (int i = 0; i < size; i++)
  {
    errSq += pow(((int) *frame)-((int) *reference), 2.0);
    frame++;
    reference++;
  }
  return 20.0*log10( 255.0 / sqrt(errSq/((double) size)));
}

yuvstream::yuvstream(char* filename, int width, int height)
{
  int pixel = width*height*1.5;
  unsigned char buffer[pixel];
  FILE* f = fopen(filename, "rb");

  while (fread(buffer, 1, pixel, f) == ((unsigned int) pixel))
    frames.push_back(new yuvframe(width, height, buffer));
  
  fclose(f);
}


std::list<yuvpsnr> yuvstream::psnr(yuvstream* reference)
{
  std::list<yuvpsnr> psnrlist;
  std::list<yuvframe*>::iterator r = reference->frames.begin();
  for (std::list<yuvframe*>::iterator i = frames.begin();
       i != frames.end(); i++)
  {
    psnrlist.push_back((*i)->psnr(*r));
    r++;
  }

  return psnrlist;
}
