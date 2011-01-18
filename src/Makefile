CC=g++
CFLAGS=-Wall

all: count_frame psnr extend trim

count_frame: count_frame.cc yuvfile.cc yuvfile.hh
	$(CC) $(CFLAGS) $^ -o $@

psnr: psnr.cc yuvfile.cc yuvfile.hh
	$(CC) $(CFLAGS) $^ -o $@

extend: extend.cc yuvfile.cc yuvfile.hh
	$(CC) $(CFLAGS) $^ -o $@

trim: trim.cc yuvfile.cc yuvfile.hh
	$(CC) $(CFLAGS) $^ -o $@
