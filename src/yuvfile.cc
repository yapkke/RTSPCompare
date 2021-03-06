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
    return (s1.psnr.average() > s2.psnr.average());
  else
    return false;
}

void yuvpsnr::add(yuvpsnr* add)
{
  y += add->y;
  u += add->u;
  v += add->v;
}

yuvframe::yuvframe(int width_, int height_, 
		   unsigned char* buffer, bool duplicate_)
{
  duplicate = duplicate_;
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

yuvframe* yuvframe::clone()
{
  int pixel = width*height;
  yuvframe* clone = new yuvframe(width, height);
  clone->duplicate = true;

  clone->y = new unsigned char[pixel];
  memcpy(clone->y, y, pixel);
  
  clone->u = new unsigned char[(int) pixel/4];
  memcpy(clone->u, u, (int) pixel/4);
  
  clone->v = new unsigned char[(int) pixel/4];
  memcpy(clone->v, v, (int) pixel/4);

  return clone;
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

void yuvstream::remove_duplicate()
{
  std::list<yuvframe*>::iterator i = frames.begin();
  while (i != frames.end())
  {
    if ((*i)->duplicate)
      i = frames.erase(i);
    else
      i++;
  }
}

std::list<yuvpsnr> yuvstream::psnr(yuvstream* reference, int offset)
{
  std::list<yuvpsnr> psnrlist;
  std::list<yuvframe*>::iterator r = reference->frames.begin();
  std::list<yuvframe*>::iterator s = frames.begin();
       
  if (offset > 0)
    for (int i = 0; i < offset; i++)
      r++;
  else if (offset < 0)
    for (int i = 0; i < offset; i--)
      s++;

  for (;s != frames.end() ; s++)
  {
    psnrlist.push_back((*s)->psnr(*r));
    r++;
    if (r == reference->frames.end())
      break;
  }

  return psnrlist;
}

streampsnr yuvstream::avPSNR(std::list<yuvpsnr> psnrlist)
{
  size_t identical = 0;
  yuvpsnr avpsnr(0.0, 0.0, 0.0);
  for (std::list<yuvpsnr>::iterator i = psnrlist.begin(); 
       i != psnrlist.end(); i++)
  {
    if (isinf(i->y))
      identical++;
    else
      avpsnr.add(&(*i));
  }

  double size = ((double) (psnrlist.size()-identical));
  avpsnr.y /= size;
  avpsnr.u /= size;
  avpsnr.v /= size;
  return streampsnr(identical,avpsnr);
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

int yuvstream::maximal_trim(yuvstream* reference)
{
  std::list<yuvpsnr> offset0 = psnr(reference);
  std::list<yuvpsnr> offset_1 = psnr(reference, -1);

  int bestFrame = 0;
  streampsnr bestPSNR = avpsnr_rm_k(offset0, offset_1, 0);
  
  for (size_t i = 1; i <= offset0.size(); i++)
  {
    streampsnr framePSNR = avpsnr_rm_k(offset0, offset_1, i);
    if (framePSNR > bestPSNR)
    {
      bestPSNR = framePSNR;
      bestFrame = i;
    }
  }

  rm_frame(bestFrame);
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

  frames.insert(j, (*j)->clone());
}

void yuvstream::rm_frame(int index)
{
  std::list<yuvframe*>::iterator j = frames.begin();
  int i = 0;
  while (i < index)
  {
    i++;
    j++;
  }

  frames.erase(j);
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

streampsnr yuvstream::avpsnr_rm_k(std::list<yuvpsnr> offset0,
				  std::list<yuvpsnr> offset_1,
				  int k)
{
  std::list<yuvpsnr>::iterator i = offset0.begin();
  std::list<yuvpsnr>::iterator j = offset_1.begin();
  size_t identical = 0;
  double avPSNR = 0.0;
  double framepsnr = 0;
  
  for (int index = 0; i != offset0.end(); i++)
  {
    framepsnr = i->average();
    if (index < k)
    {
      if (isinf(framepsnr))
	identical++;
      else
	avPSNR += framepsnr;
    }

    framepsnr = j->average();
    if (index > k)
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
