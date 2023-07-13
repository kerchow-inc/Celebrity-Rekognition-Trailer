# Celebrity-Rekognition-Trailer
Utilizing AWS Rekognition to showcase possible functionalities
#### YouTube: https://www.youtube.com/watch?v=iric7m71y30&t=12s&ab_channel=Kerchow
***
### Three functionalities demonstrated in rekog.py are: ###
1. Detecting all celebrities in a given image
2. Draw a bounding box and insert the name below the bounding box of each celebrity recognized in the photo
3. Detect celebrities in a movie trailer, insert photo and name of the celebrity for each frame the celebrity appears on, and combine frames back together to be close to Amazon Prime Video X-Ray
***
### Below is a list of functions that are included in the rekog.py file: ###
* recognize_celebrities - takes a local image file string and returns a dictionary of celebrities with bounding box coordinates
* celebrity_bounding_boxes - takes a celebrity dictionary and local image file string and displays a photo with bounding box around celebrity faces with names listed below
* celebrity_bounding_boxes_trailer - takes a celebrity dictionary and local image file string and puts the celebrity photo and name onto a single frame when recognized
* turn_trailer_to_frames - takes a local video file string and converts the video file to image frames and stores them in the local folder, then utilizes recognize_celebrities and celebrity_bounding_boxes_trailer to generate a trailer with celebrity image and name to be shown when they appear in the trailer
* turn_trailer_back_to_movie - converts all frames with the celebrity's faces and names back to AVI format so the video can be watched
