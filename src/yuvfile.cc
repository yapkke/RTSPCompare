#include "yuvfile.hh"
#include <stdlib.h>
#include <stdio.h>
#include <cstring>
#include <cmath>

bool operator> (streampsnr &s1, streampsnr &s2)
{
  if (s1.identical > s2.identical)
    return true;
  else if (s1.identical == s2.identical)
    return (s1.average > s2.average);
  else
    return false;
}

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

void yuvstream::write_to_file(char* filename)
{
  FILE* f = fopen(filename, "w");
  std::list<yuvframe*>::iterator i = frames.begin();
  int pixel = (*i)->width*(*i)->height;

  for(; i != frames.end(); i++)
  {
    fwrite((*i)->y, 1, pixel, f);
    fwrite((*i)->u, 1, pixel/4, f);
    fwrite((*i)->v, 1, pixel/4, f);
  }

  fclose(f);
}

std::list<yuvpsnr> yuvstream::psnr(yuvstream* reference, int offset)
{
  std::list<yuvpsnr> psnrlist;
  std::list<yuvframe*>::iterator r = reference->frames.begin();
  for (int i = 0; i < offset; i++)
    r++;
  for (std::list<yuvframe*>::iterator i = frames.begin();
       i != frames.end(); i++)
  {
    psnrlist.push_back((*i)->psnr(*r));
    r++;
  }

  return psnrlist;
}

streampsnr yuvstream::avPSNR(std::list<yuvpsnr> psnrlist)
{
  size_t identical = 0;
  double avpsnr = 0.0;
  for (std::list<yuvpsnr>::iterator i = psnrlist.begin(); 
       i != psnrlist.end(); i++)
  {
    double framepsnr = i->average();
    if (isinf(framepsnr))
      identical++;
    else
      avpsnr += framepsnr;
  }

  return streampsnr(identical,
		    avpsnr/((double) (psnrlist.size()-identical)));
}

int yuvstream::maximal_extend(yuvstream* reference)
{
  std::list<yuvpsnr> offset0 = psnr(reference);
  std::list<yuvpsnr> offset1 = psnr(reference, 1);

  int bestFrame = 0;
  streampsnr bestPSNR = avpsnr_dup_k(offset0, offset1, 0);
  
  for (size_t i = 1; i < offset0.size(); i++)
  {
    streampsnr framePSNR = avpsnr_dup_k(offset0, offset1, i);
    if (framePSNR > bestPSNR)
    {
      bestPSNR = framePSNR;
      bestFrame = i;
    }
  }

  dup_frame(bestFrame);
  return bestFrame;
}

void yuvstream::dup_frame(int index)
{
  std::list<yuvframe*>::iterator j = frames.begin();
  int i = 0;
  while (i < index)
  {
    i++;
    j++;
  } 

  frames.insert(j, *j);
}

streampsnr yuvstream::avpsnr_dup_k(std::list<yuvpsnr> offset0,
				   std::list<yuvpsnr> offset1,
				   int k)
{
  std::list<yuvpsnr>::iterator i = offset0.begin();
  std::list<yuvpsnr>::iterator j = offset1.begin();
  size_t identical = 0;
  double avPSNR = 0.0;
  double framepsnr = 0;
  
  for (int index = 0; i != offset0.end(); i++)
  {
    framepsnr = i->average();
    if (index <= k)
    {
      if (isinf(framepsnr))
	identical++;
      else
	avPSNR += framepsnr;
    }

    framepsnr = j->average();
    if (index >= k)
    {
      if (isinf(framepsnr))
	identical++;
      else
	avPSNR += framepsnr;
    }

    index++;
    j++;
  }

  return streampsnr(identical,
		    avPSNR/((double) (offset0.size()+1-identical)));
  
}
