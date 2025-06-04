
# define Message class
class Message:

    def __init__(self, text):
        '''initialise new Message object'''

        self.text = text
        # .text holds the message entered by the user

        self.length = len(self.text)
        # .length holds the length of the message

    def create_bin_arr(self):
        '''converts user's message into binary ascii values and stores bits in an array'''

        self.bin_arr = []
        # initialise array

        # for each character in the message + end of message string
        for x in (self.text + "xxx"):

            bin_val = bin(ord(x))[2:]
            # convert ascii value of character to binary

            # ensure each character is represented by a whole byte
            while len(bin_val) < 8:
                bin_val = "0" + bin_val

            # individually add each bit into array
            for y in bin_val:
                self.bin_arr.append(int(y))

