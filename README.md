# 5062CEM_CW1

## Introduction

Welcome to the repository for my coursework 1 for the module 5062CEM Programming and Algorithms 2

## What It Does

This is an image steganography program designed to be run on a linux system. Image steganography is the process of hiding data within an image file. The point is to conceal the existence of the data from anyone who looks at the image.

[More information about image steganography](https://www.geeksforgeeks.org/image-steganography-in-cryptography/)

With this program, users are able to encode an image with a piece of text, decode a piece of text that has been hidden in an image, or view an image.

This program specifically uses the least significant bit method to encode the text within an image. To do this, it changes the last bit of every byte that makes up the image to a bit representing the data being concealed. Since the most significant bits are unaffected, there is no visible change to the image.

[More information about the least significant bit method (with example)](https://www.tutorialspoint.com/what-is-least-significant-bit-algorithm-in-information-security)

## How To Use

To run this program, first the following files need to be downloaded:
- main.py
- image_def.py
- message_def.py
- test.py
- image.png
- image_copy.jpg

### Module Requirements

The following modules will need to be installed for all parts of the program to run correctly:
 
#### Modules imported in main.py:
- [OpenCV](https://docs.opencv.org/3.4/index.html)
- [OS](https://docs.python.org/3/library/os.html)

#### Modules imported in image_def.py:
- [OpenCV](https://docs.opencv.org/3.4/index.html)
- [OS](https://docs.python.org/3/library/os.html)
- [Math](https://docs.python.org/3/library/math.html)

#### Modules imported in test.py
- [Unitttest](https://docs.python.org/3/library/unittest.html)
- [OpenCV](https://docs.opencv.org/3.4/index.html)
- [OS](https://docs.python.org/3/library/os.html)

### Testing

The file test.py contains tests for the functions used in main.py, image_def.py and message_def.py.

It can be run from the CLI by navigating to the project directory where test.py is located and running the command:

`python3 test.py`

### Running the program

The program can be run from the CLI by navigating to the project directory where main.py is located and running the command:

`python3 main.py`
