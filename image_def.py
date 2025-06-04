import cv2  # import OpenCV for image handling
import os
import math


# define Image class
class Image:

    def __init__(self, img, filepath):
        '''initialise new Image object'''

        self.img = img
        # .img holds the image array

        self.filepath = filepath
        # .filepath holds the filepath of the image

        self.max_lsb_length()
        # calculate maximum length of message that can be stored in the image

    def max_lsb_length(self):
        '''calculates the maximum length of a message that can be stored in the chosen image using least significant bit'''

        bits = 0
        # initialise bits

        # for each pixel in the image
        for x in self.img:
            for y in x:
                for z in y:

                    bits += 1
                    # number of bits that can be stored increases by 1

        self.max_chars = math.floor((bits / 8) - 3)
        # calculate maximum whole number of characters that can be stored (1 byte per character)
        # minus 3 for end of message string

    def save_image(self):
        '''saves encoded image'''

        new_file = os.path.splitext(self.filepath)[0] + "_encoded" + os.path.splitext(self.filepath)[1]
        # add suffix '_encoded' to file name

        count = 1
        # initialise count

        # if file name has already been used
        while os.path.isfile(new_file):

            new_file = os.path.splitext(self.filepath)[0] + "_encoded({})".format(count) + os.path.splitext(self.filepath)[1]
            # add number in brackets to file name

            count += 1
            # increase number by 1

        cv2.imwrite(new_file, self.img)
        # save image with new file name

        print("\nEncoded image has been saved as " + new_file)
        # print message telling user where image has been saved

    def display_image(self):
        '''displays image'''

        cv2.imshow(self.filepath, self.img)
        # create window to show image

        cv2.waitKey(5000)
        # wait five seconds before closing window

        cv2.destroyAllWindows()
        # delete window

