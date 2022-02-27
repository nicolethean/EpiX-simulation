# hack-22
Authors: 
Nicole Thean  (nicole@thean.com)
Jeff Zhou  (jffzhou@gmail.com)

Health Hackathon 2022
Model for prototype for epilepsy-triggering events on desktop. 

Other Team Members:
Priscilla Liu, Lisa Wang, Yashshree Shah

//////////////////////////////////////////////////////////////////////////////
Our Program:

Transforms sequence of images to RGB tuple 2D arrays for frame-by-frame pixel analysis.
Implements luminosity difference as criteria for filtering. 
Criteria taken from https://www.researchgate.net/publication/282936402_Automatic_detection_of_flashing_video_content 

Filtering is defined by changing a "flashing" pixel to solid color, i.e. grey. 
The filtered pixels must meet criteria: positive difference with a neigboring pixel in one frame followed by a negative difference at that same pixel where n frames in between can have minimal difference.

After the first detection of a flashing pixel, that pixel is kept at constant color for t frames (based on allowable epilepsy times). 

The sequence of inputed images are first animated without filtering.
The filtered images are also animated after the program finishes.