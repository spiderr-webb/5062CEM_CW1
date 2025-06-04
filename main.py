import cv2  # import OpenCV for image handling
import os
from image_def import Image
from message_def import Message


def lsb_encode(img, msg, key):
    '''encodes the user's message into the chosen image using least significant bit method'''

    msg.create_bin_arr()
    # turn user message into binary ascii values and store bits in an array

    new_arr = Image(img.img, img.filepath)
    # create new array that is the same size as the original image array

    msg_count = 0
    key_count = 0
    # initialise byte_count and key_count

    # for each pixel in the image
    for x in range(len(img.img) - 1):
        for y in range(len(img.img[x]) - 1):
            for z in range(len(img.img[x][y]) - 1):

                # if at the correct starting point for the message according to the key
                if key_count >= key:

                    # if not reached the end of the message
                    if msg_count != len(msg.bin_arr):

                        pixel_val = bin(img.img[x][y][z])[2:]
                        # convert value of pixel component to binary

                        new_pixel_val = pixel_val[:-1] + str(msg.bin_arr[msg_count])
                        # change last bit of pixel component value to next message bit

                        msg_count += 1
                        # move to next bit in message array

                        new_arr.img[x][y][z] = int(new_pixel_val, 2)
                        # set value of pixel component in new image array

                key_count += 1
                # next pixel component

    return new_arr
    # return encoded image array


def lsb_decode(img, key):
    '''decodes message from image using least significant bit method'''

    char = ""
    text = ""
    # initialise char and msg

    count = 0
    # initialise count

    # for each pixel in the image
    for x in range(len(img.img) - 1):
        for y in range(len(img.img[x]) - 1):
            for z in range(len(img.img[x][y]) - 1):

                # if reached starting point of the message according to the key
                if count >= key:

                    pixel_val = bin(img.img[x][y][z])[2:]
                    # convert value of pixel component to binary

                    char = char + pixel_val[-1]
                    # add last bit of pixel component value to binary value of character

                    # if char contains a full byte
                    if len(char) == 8:

                        text = text + chr(int(char, 2))
                        # add character represented by binary to message

                        char = ""
                        # clear char

                count += 1
                # next pixel component

    extracted_arr = text.split("xxx")
    # separate additional characters from end of message

    # if extracted text has been successfully separated into message and additional characters
    if len(extracted_arr) == 2:

        msg = Message(extracted_arr[0])
        # message is first part of extracted text

    else:

        msg = Message("")
        # message could not be extracted

    return msg
    # return message


def get_key(img, msg, encode):
    '''gets key based on user input'''

    print("\nWould you like to use a key? Y/N: ", end="")
    # give user the option to use a key

    valid = False
    # initialise valid

    # while input from user is not valid
    while not valid:

        use_key = input().upper()
        # get input from user

        # if user wants to use a key
        if use_key == "Y":

            valid = True
            # user input is valid

            # if encoding a message
            if encode:

                print("Enter an integer to generate key: ", end="")
                key = int(input()) % (img.max_chars - msg.length + 1)
                # get number to generate key from user
                # ensure key leaves enough space for message to be stored in image

                print("Key: {}".format(key))
                # print key to user

            # if decoding a message
            else:

                key_size = False
                # initialise key_size

                print("Enter the key: ", end="")
                # ask user for key

                # while key is not within the correct range
                while not key_size:

                    key = int(input())
                    # get key from user

                    # if key is larger than image size could allow
                    if key > img.max_chars:

                        print("Key is too large for this image, please re-enter: ", end="")
                        # print error message

                        key_size = False
                        # key is not within correct range

                    # if key is less than zero
                    elif key < 0:

                        print("Key must be a positive number, please re-enter: ", end="")
                        # print error message

                        key_size = False
                        # key is not within correct range

                    else:

                        key_size = True
                        # key is within correct range

        # if user does not want to use a key
        elif use_key == "N":

            valid = True
            # user input is valid

            key = 0
            # no key

        else:

            valid = False
            # user input is invalid

            print("Invalid response, please enter Y or N: ", end="")
            # print error message

    return key
    # return key to use for encoding or decoding


def add_image():
    '''finds image to use for encoding specified by the user'''

    print("\nEnter the file path of the image (if you don't have an image enter image.png): ", end="")
    # print message asking user for file path of image

    valid = False
    # initialise valid

    while not valid:
        filepath = input()
        # get file path of image from user

        # if file does not exist
        if not os.path.isfile(filepath):

            print("File does not exist, please enter a different file path: ", end="")
            # print error message

            valid = False
            # get user to re enter file path of image

        # if file is not a png
        elif os.path.splitext(filepath)[1] != ".png":

            print("Only .png files are accepted, please enter a different file path: ", end="")
            # print error message

            valid = False
            # get user to re enter file path of image

        else:
            valid = True
            # use image given by user

    img = Image(cv2.imread(filepath, cv2.IMREAD_COLOR), filepath)
    # read in image and create object

    return img
    # return image object


def add_message():
    '''allows user to enter a message to encode'''

    print("\nEnter the message you would like to hide: ", end="")
    msg = Message(input())
    # get message from user

    return msg
    # return message


def menu():
    '''provides a menu for the user to choose what to do'''

    option = ""
    # initialise option

    # loop until user wants to quit
    while option != "0":

        # display menu options
        print("\nWhat would you like to do?")
        print("1 - Encode an image")
        print("2 - Decode an image")
        print("3 - Show an image")
        print("0 - Quit")

        print("\nEnter a number: ", end="")

        option = input()
        # get user's choice

        # if encoding an image
        if option == "1":

            cover_img = add_image()
            # allow user to choose image

            # if image is large enough to store a message
            if cover_img.max_chars > 0:
                print("\nMaximum number of characters that can be hidden in this image: {}".format(cover_img.max_chars))
                # print maximum number of characters to user

                encode_msg = add_message()
                # allow user to enter a message

                # if message is not too long
                if encode_msg.length <= cover_img.max_chars:

                    key = get_key(cover_img, encode_msg, True)
                    # generate key

                    stego_img = lsb_encode(cover_img, encode_msg, key)
                    # encode new image

                    stego_img.save_image()
                    # save new image

                # if message is too long
                else:

                    print("Message too long for this image")
                    # print error message

            # if image is too small to store a message
            else:

                print("Image is too small for a message")
                # print error message

        # if decoding an image
        elif option == "2":

            stego_img = add_image()
            # allow user to choose image

            key = get_key(stego_img, 0, False)
            # get key from user

            decode_msg = lsb_decode(stego_img, key)
            # decode image

            # if message could not be successfully extracted
            if decode_msg.text == "":

                print("Message could not be extracted from image")
                # print error message

            else:

                print("\nExtracted message: {}".format(decode_msg.text))
                # print decoded message

        # if showing an image
        elif option == "3":

            img = add_image()
            # allow user to choose image

            img.display_image()
            # display image

        # if quitting
        elif option == "0":

            print("\nGoodbye!")
            # print goodbye message

        # if invalid option entered
        else:

            print("Invalid option - ", end="")
            # print error message


def start():
    '''starting function'''

    print("\nWelcome!")
    # print welcome message

    menu()
    # display menu


start()
# start
