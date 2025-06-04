import unittest
from unittest import mock
import cv2
import os
from main import lsb_encode, lsb_decode, get_key, add_image
from image_def import Image
from message_def import Message


class MyTestCase(unittest.TestCase):

    # test that message encoded in an image can be successfully extracted from that image
    def test_encode_decode(self):

        # create image and message objects
        image = Image(cv2.imread("image.png", cv2.IMREAD_COLOR), "image.png")
        message = Message("Hello World!")

        # test without key
        encoded_image = lsb_encode(image, message, 0)
        self.assertEqual(lsb_decode(encoded_image, 0).text, "Hello World!")

        # create new message
        message = Message("Test with good key")

        # test with key
        encoded_image = lsb_encode(image, message, 1234)
        self.assertEqual(lsb_decode(encoded_image, 1234).text, "Test with good key")

        # create new message
        message = Message("Test with bad key")

        # test that message cannot be decoded with incorrect key
        encoded_image = lsb_encode(image, message, 1234)
        self.assertNotEqual(lsb_decode(encoded_image, 4321).text, "Test with bad key")

    # test that message is being correctly converted to array of ascii bits
    def test_create_bin_arr(self):

        # test message with lowercase
        message = Message("test")
        message.create_bin_arr()
        self.assertEqual(message.bin_arr, [0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1,
                                           1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0,
                                           0, 0, 0, 1, 1, 1, 1, 0, 0, 0])

        # test message with uppercase and numbers
        message = Message("TEST 2")
        message.create_bin_arr()
        self.assertEqual(message.bin_arr, [0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0,
                                           1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0,
                                           0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0,
                                           0, 0, 0, 1, 1, 1, 1, 0, 0, 0])

        # test message with symbols
        message = Message(":)")
        message.create_bin_arr()
        self.assertEqual(message.bin_arr, [0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
                                           1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0])

    # test that key is correctly generated from user input
    @mock.patch('main.input', create=True)
    def test_get_key(self, mocked_input):

        # create image and message objects
        test_image = Image([[[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]],
                            [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]],
                            [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]],
                            [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]], "file.png")
        message = Message(":)")

        # test with encode=True and input smaller than highest allowed key value
        mocked_input.side_effect = ['Y', '5']
        self.assertEqual(get_key(test_image, message, True), 1)

        # create new message
        message = Message("Test")

        # test with encode=True and input larger than highest allowed key value
        mocked_input.side_effect = ['Y', '123']
        self.assertEqual(get_key(test_image, message, True), 1)

        # test with encode=False and valid key value
        mocked_input.side_effect = ['Y', '1']
        self.assertEqual(get_key(test_image, message, False), 1)

        # test with encode=True and invalid key values
        mocked_input.side_effect = ['Y', '123', '-1', '1']
        self.assertEqual(get_key(test_image, message, False), 1)

        # create image and message objects
        test_image = Image([], "file.png")
        message = Message("")

        # test with no key value input
        mocked_input.side_effect = ['N']
        self.assertEqual(get_key(test_image, message, False), 0)

        # test with invalid inputs
        mocked_input.side_effect = ['X', 'X', 'n']
        self.assertEqual(get_key(test_image, message, False), 0)

    # test that maximum message length for an image is calculated correctly
    def test_max_lsb_length(self):

        # test with image large enough for message
        test_image = Image([[[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]],
                            [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]],
                            [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]], "file.png")
        test_image.max_lsb_length()
        self.assertEqual(test_image.max_chars, 3)

        # test with image too small for message
        test_image = Image([[[0, 1], [2, 3], [4, 5], [6, 7]]], "file.png")
        test_image.max_lsb_length()
        self.assertEqual(test_image.max_chars, -2)

    # test that image can be successfully read in
    @mock.patch('main.input', create=True)
    def test_add_image(self, mocked_input):

        # test with valid only input
        mocked_input.side_effect = ['image.png']

        image = add_image()
        self.assertEqual(image.img.tolist(), cv2.imread("image.png", cv2.IMREAD_COLOR).tolist())
        self.assertEqual(image.filepath, 'image.png')

        # test with invalid inputs
        mocked_input.side_effect = ['fake.png', 'image_copy.jpg', 'image.png']

        image = add_image()
        self.assertEqual(image.img.tolist(), cv2.imread("image.png", cv2.IMREAD_COLOR).tolist())
        self.assertEqual(image.filepath, 'image.png')

    # test that image can be saved correctly
    def test_save_image(self):

        # create image object
        image = Image(cv2.imread("image.png", cv2.IMREAD_COLOR), "save_test_image.png")

        # test without existing file
        image.save_image()
        self.assertTrue(os.path.isfile("save_test_image_encoded.png"))

        # test with existing file
        image.save_image()
        self.assertTrue(os.path.isfile("save_test_image_encoded(1).png"))

        # delete created files
        os.remove("save_test_image_encoded.png")
        os.remove("save_test_image_encoded(1).png")


if __name__ == '__main__':
    unittest.main()

