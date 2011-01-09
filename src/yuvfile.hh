#include <list>

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
  char* y;
  /** \brief U data
   */
  char* u;
  /** \brief V data
   */
  char* v;

  /** \brief Constructor
   * @param width width of frame
   * @param height height of frame
   * @param buffer buffer containing frame
   */
  yuvframe(int width, int height, char* buffer);

  /** \brief Destructor
   */
  ~yuvframe();

private:
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

private:
};
