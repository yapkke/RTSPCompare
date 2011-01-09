#include "yuvfile.hh"
#include <stdlib.h>
#include <stdio.h>
#include <cstring>

yuvframe::yuvframe(int width_, int height_, char* buffer)
{
  width = width_;
  height = height_;
  int pixel = width_*height_;

  y = new char[pixel];
  memcpy(y, buffer, pixel);
  buffer += pixel;

  u = new char[(int) pixel/4];
  memcpy(u, buffer, (int) pixel/4);
  buffer += ((int) pixel/4);

  v = new char[(int) pixel/4];
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

yuvstream::yuvstream(char* filename, int width, int height)
{
  int pixel = width*height*1.5;
  char buffer[pixel];
  FILE* f = fopen(filename, "rb");

  while (fread(buffer, 1, pixel, f) == ((unsigned int) pixel))
    frames.push_back(new yuvframe(width, height, buffer));
  
  fclose(f);
}
