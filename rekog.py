# import necessary libraries
import boto3
import cv2
# import datetime
from dotenv import load_dotenv
import glob
import os
import re

load_dotenv()

# load key and secret from local .env file
aws_access_key_id = os.getenv('key')
aws_secret_access_key = os.getenv('secret')

# initialize aws credentials with boto3
client = boto3.client("rekognition", aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key, region_name="us-east-2")

# celebrity recognition
'''
    photo(string): local image location
'''


def recognize_celebrities(photo):
    # create a dictionary to keep track of celebrity and location in image
    celeb_location = {}

    # opening local photo and passing to aws for rekognition processing
    with open(photo, 'rb') as image:
        res = client.recognize_celebrities(Image={'Bytes': image.read()})

    # now will loop through all celebrity faces that rekognition recognized
    for celebrity in res['CelebrityFaces']:
        # name of recognized celebrity
        name = celebrity['Name']
        # location of celebrities face
        bounding_box = celebrity['Face']['BoundingBox']

        if name not in celeb_location:
            celeb_location[name] = bounding_box

    # return celebrity location
    return celeb_location


# draw celebrity bounding boxes
'''
    celebrities(dictionary): {celebrity_name: bounding_box_dictionary}
    image(string): location of local image
'''


def celebrity_bounding_boxes(celebrities, image):
    # get local image loaded
    photo = cv2.imread(image)

    # to get opencv bounding boxes we will need to
    # use our photo width and height
    photo_width = photo.shape[1]
    photo_height = photo.shape[0]

    for celeb in celebrities:
        # convert coordinates to opencv by rounding and mulitplying
        # by photo width and height
        left = round(celebrities[celeb]['Left']*photo_width)
        top = round(celebrities[celeb]['Top']*photo_height)
        width = round(celebrities[celeb]['Width']*photo_width)
        height = round(celebrities[celeb]['Height']*photo_height)

        # draw our bounding box onto the photo
        cv2.rectangle(photo, (left, top),
                      (left + width, top + height), (255, 255, 0), 4)

        # insert the celeb name at the bottom left corner
        cv2.putText(photo, celeb, (left+25, top + height+25),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2)

    # show our photo
    cv2.imshow('Celebrity Rekognition', photo)
    # pressing 0 on keyboard will close image
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# draw celebrity bounding boxes
'''
    celebrities(dictionary): {celebrity_name: bounding_box_dictionary}
    image(string): location of local image
'''


def celebrity_bounding_boxes_trailer(celebrities, image):
    # get local image loaded
    photo = cv2.imread(image)

    # celeb dictionary
    celeb_dictionary = {
        'Winston Duke': 'celebs//winston.jpg',
        'Danai Gurirae': 'celebs//danai.jpg',
        'Danai Gurira': 'celebs//danai.jpg',
        'Elizabeth Olsen': 'celebs//elizabeth.jpg',
        'Robert Downey Jr.': 'celebs//robert.jpg',
        'Paul Bettany': 'celebs//paul.jpg',
        'Tor Johnson': 'celebs//tor.jpg',
        'Chadwick Boseman': 'celebs//chadwick.jpg',
        'Sebastian Stan': 'celebs//sebastian.jpg',
        'Letitia Wright': 'celebs//letitia.jpg',
        'Chris Evans': 'celebs//chris.jpg',
        'Tom Holland': 'celebs//tom.jpg',
        'Anthony Mackie': 'celebs//anthony.jpg',
        'Scarlett Johansson': 'celebs//scarlett.jpg',
        'Benedict Cumberbatch': 'celebs//benedict.jpg',
    }

    # initialize celeb photo position
    celeb_photo_position = 50
    for celeb in celebrities:

        # get celebrity photo and text that we will put onto frame if it is in our dictionary
        if celeb in celeb_dictionary:
            celeb_photo = cv2.imread(celeb_dictionary[celeb])
            photo[50:100, celeb_photo_position +
                  50:celeb_photo_position+100, :] = celeb_photo

            # insert the celeb name at the bottom left corner
            cv2.putText(photo, celeb, (celeb_photo_position, 40),
                        cv2.FONT_HERSHEY_COMPLEX, 1/2, (255, 255, 255), 1)
            # create gap between next celeb photo in case there is more than one celeb in the frame
            celeb_photo_position += 300

    save_file_name = image.replace('frames', 'trailer')
    cv2.imwrite(save_file_name, photo)


# turn trailer to frames
'''
    trailer(string): location of trailer
'''


def turn_trailer_to_frames(trailer):
    cap = cv2.VideoCapture(trailer)
    path_to_save = 'frames'

    # count the number of frames
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = round(cap.get(cv2.CAP_PROP_FPS))

    # calculate duration of the video
    seconds = round(frames / fps)
    # video_time = datetime.timedelta(seconds=seconds)

    if (cap.isOpened() == False):
        return {}
    total_frame = 1
    current_frame = fps

    # print(f"duration in seconds: {seconds}")
    # print(f"video time: {video_time}")
    print(f"fps: {fps}")
    print(f"frames: {frames}")

    # bool to decide if the whole video will turn to frames
    # or just on frame per second
    full_vid = True

    # cap opened successfully
    while (cap.isOpened()):

        # capture each frame
        ret, frame = cap.read()
        if (ret == True):
            if full_vid:
                # Save frame as a jpg file
                name = 'frame' + str(total_frame) + '.jpg'
                cv2.imwrite(os.path.join(path_to_save, name), frame)

            else:
                if (current_frame == fps):
                    # Save frame as a jpg file
                    name = 'frame' + str(total_frame) + '.jpg'
                    cv2.imwrite(os.path.join(path_to_save, name), frame)
                    current_frame = 1
                else:
                    # keep track of how many images you end up with
                    current_frame += 1

            total_frame += 1

        else:
            break
    # release capture
    cap.release()

    # make a set for the celebrities because only need to know
    # celebrity appears once
    # celeb_set = set()
    # get all frames and find which celebs are in each frame
    final_frames = glob.glob("frames//*")
    for frame in final_frames:
        celeb_res = recognize_celebrities(frame)
        # for celeb in celeb_res:
        # celeb_set.add(celeb)
        celebrity_bounding_boxes_trailer(celeb_res, frame)

    # write/print out celebs that were found
    # print(celeb_set)
    # with open('celebs.txt', 'w') as f:
    #     f.write(str(celeb_set))

# sort function found at https://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]


# convert all frames with celebrity photos and names back into the original trailer


def turn_trailer_back_to_movie():
    # get all trailer files
    trailer_frames = glob.glob("trailer//*")
    # get the height and width of one frame to initialize VideoWriter
    frames = cv2.imread(trailer_frames[0])
    height, width, layers = frames.shape

    video = cv2.VideoWriter('avengers_with_celebs.avi', 0, 24, (width, height))

    # with glob it will not come out exactly in order ex. frames1,frames100,frames101
    # so this sorting functionality will put frame in order ex. frames1, frames2, frames3
    sort_frames = []
    for f in trailer_frames:
        sort_frames.append(f.replace('.jpg', '').replace('trailer\\', ''))
    sort_frames.sort(key=natural_keys)

    # stitch all frames back together
    for frame in sort_frames:
        video.write(cv2.imread('trailer//'+frame+'.jpg'))

    # close cv
    cv2.destroyAllWindows()
    video.release()


def main():
    # celebrity rekognition
    # celeb_res = recognize_celebrities('photos//selfie.jpg')

    #print out list of celebs from the result
    # for celeb in celeb_res:
    #     print(celeb)

    # print out bounding box and name on image
    # celebrity_bounding_boxes(celeb_res,"photos//selfie.jpg")

    turn_trailer_to_frames('photos//avengers.mp4')
    turn_trailer_back_to_movie()


if __name__ == "__main__":
    main()
