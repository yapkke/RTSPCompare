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
  yuvpsnr(double y_, double u_, double v_):
    y(y_), u(u_), v(v_)
  {}
};

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

  /** \brief PSNR of stream with reference
   * @param reference reference stream
   * @return list YUV PSNR
   */
  std::list<yuvpsnr> psnr(yuvstream* reference);

  /** \brief Extend stream by one to maximize average PSNR
   * Find the PSNR values of stream,
   * and the PSNR values by displacing it by one.
   * Each possibility is a sum of the two.
   * @param reference reference stream
   */
  void maximal_extend(yuvstream* reference);

private:
};
