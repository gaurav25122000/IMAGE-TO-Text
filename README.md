# IMAGE-TO-Text
The code uses various libraries of python to interact with the csv/Image file provided.
Firstly the image if coloured is converted to grayscale. Then using pytesseract the image is converted to a string. 
then the string is converted into a list using split function splitting at every new line.
Using regex(REGULAR EXPRESSION) the text neended is searched in the list.
Then accoridng to the text that is to be found, the list is further splitted and the output is stored in another list.
Finally all of the found lists are appended in a file.


This is the main working of the code.
REGEX is used for searching and pytesseract to convert it into string.
Some resizing is also done based upon the allowed sizes for the functions.
