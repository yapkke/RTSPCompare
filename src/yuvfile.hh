#include <list>

/** \brief YUV PSNR
 */
struct yuvpsnr
{
  /** \brief Y PNSR
   */
  double y;
  /** \brief U PNSR
   */
  double u;
  /** \brief V PNSR
   */
  double v;

  /** \brief Constructor
   * @param y_ Y-PSNR
   * @param u_ U-PSNR
   * @param v_ V-PSNR
   */
  yuvpsnr(double y_=0.0, double u_=0.0, double v_=0.0):
    y(y_), u(u_), v(v_)
  {}

  /** \brief Constructor
   * @param psnr_ PSNR
   */
  yuvpsnr(const yuvpsnr& psnr_):
    y(psnr_.y), u(psnr_.u), v(psnr_.v)
  {}

  /** \brief Add YUV PSNR
   * @param add YUV PSNR to add
   */
  void add(yuvpsnr* add);

  /** \brief Average PSNR
   */
  double average()
  {
    return (4.0*y+u+v)/6.0;
  }
};


/** \brief YUV Stream PSNR
 */
struct streampsnr
{
  /** \brief Number of identical frames
   */
  size_t identical;
  /** \brief PSNR of non-identical frames
   */
  yuvpsnr psnr;

  /** \brief Constructor
   * @param identical_ number of identical frames
   * @param psnr_ PSNR
   */
  streampsnr(size_t identical_, yuvpsnr psnr_):
    identical(identical_), psnr(psnr_)
  {}
};

bool operator> (streampsnr &s1, streampsnr &s2);

/** \brief YUV frame
 *
 * @author ykk
 * @date January 2011
 */
class yuvframe
{
public:
  /** \brief Width of frame
   */
  int width;
  /** \brief Height of frame
   */
  int height;
  /** \brief Y data
   */
  unsigned char* y;
  /** \brief U data
   */
  unsigned char* u;
  /** \brief V data
   */
  unsigned char* v;

  /** \brief Constructor
   * @param width width of frame
   * @param height height of frame
   * @param buffer buffer containing frame
   */
  yuvframe(int width, int height, 
	   unsigned char* buffer);

  /** \brief Destructor
   */
  ~yuvframe();

  /** \brief Calculate PSNR with reference frame
   * @param reference reference frame
   * @return YUV PSNR in dB
   */
  yuvpsnr psnr(yuvframe* reference);

private:
  /** \brief Calculate PSNR with frame.
   * @param frame frame
   * @param reference reference frame
   * @param size size of frame and reference frame
   */
  double frame_psnr(unsigned char* frame, 
		    unsigned char* reference, int size);
};

/** \brief YUV Stream
 *
 * @author ykk
 * @date January 2011
 */
class yuvstream
{
public:
  /** \brief List of frames
   */
  std::list<yuvframe*> frames;

  /** \brief Constructor
   * @param filename name of file containing stream
   * @param width width of frame
   * @param height height of frame
   */
  yuvstream(char* filename, int width, int height);

  /** \brief Destructor
   */
  ~yuvstream()
  {
    frames.clear();
  }

  /** \brief Write stream to file
   * @param filename filename to write to
   */
  void write_to_file(char* filename);

  /** \brief PSNR of stream with reference
   * @param reference reference stream
   * @param offset offset to apply to reference stream
   * @return list YUV PSNR
   */
  std::list<yuvpsnr> psnr(yuvstream* reference, int offset=0);

  /** \brief Average PSNR
   * @param psnrlist list of YUV PSNR
   * @return average PSNR 
   */
  static streampsnr avPSNR(std::list<yuvpsnr> psnrlist); 

  /** \brief Average PSNR
   * @param reference stream
   * @return average PSNR 
   */
  streampsnr avPSNR(yuvstream* reference)
  {
    return avPSNR(psnr(reference));
  }

  /** \brief Extend stream by one to maximize average PSNR
   * Find the PSNR values of stream,
   * and the PSNR values by displacing it by one.
   * Each possibility is a sum of the two.
   * @param reference reference stream
   * @return frame duplicated
   */
  int maximal_extend(yuvstream* reference);

private:
  /** \brief Average PSNR for duplicate frame k
   * @param offset0 PSNR values without offset
   * @param offset1 PSNR values with offset 1
   * @param k frame number of duplicate
   * @return resulting average PSNR
   */
  streampsnr avpsnr_dup_k(std::list<yuvpsnr> offset0,
		      std::list<yuvpsnr> offset1,
		      int k);

  /** \brief Duplicate Frame
   * @param index frame index to duplicate
   */
  void dup_frame(int index);
};
