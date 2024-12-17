import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog, Text, Scrollbar
from PIL import Image


# CONSTANTS
ASCII_CHARS = "@%#*+=-:. "


# FUNCTIONS
def ResizeImage(image, newWidth=100, maxHeight=50):
    # RATIO_SIZE adjusts for character dimensions in ASCII art
    RATIO_SIZE = 1.7
    # get the original dimensions of the image
    width, height = image.size
    # calculate the aspect ratio of the image
    # RATIO_SIZE is used to adjust the aspect ratio for character dimensions in ASCII art
    ratio = height / width / RATIO_SIZE
    # calculate the new height based on the new width and the aspect ratio
    newHeight = min(int(newWidth * ratio), maxHeight)  # constrain to maxHeight
    # Resize to the new dimensions (newWidth, newHeight) and return image
    return image.resize((newWidth, newHeight))

def Grayify(image):
    # converts the image to grayscale
    return image.convert("L")

def PixelsToAscii(image):
    # get pixel data from image
    pixels = image.getdata()
    # initialize an empty string for ASCII representation
    asciiStr = ""

    for pixel in pixels:
        # map the pixel value (0-255) to an index in ASCII_CHARS
        # len(ASCII_CHARS) gives the number of characters in the ASCII_CHARS string (10 in this case)    
        # scale the pixel value to the range of ASCII_CHARS indices
        # the formula pixel * len(ASCII_CHARS) // 256 does the following:
        # 1. pixel * len(ASCII_CHARS): scales the pixel value (0-255) to a range of 0-2550
        # 2. // 256: reduces the scaled value to an index in the range of 0-9 (the valid indices for ASCII_CHARS)
        # example:
        # if pixel is 0, then 0 * 10 // 256 = 0 (maps to '@')
        # if pixel is 255, then 255 * 10 // 256 = 9 (maps to ' ')
        asciiStr += ASCII_CHARS[pixel * len(ASCII_CHARS) // 256]
    return asciiStr

def ImageToAscii(imagePath, newWidth=100, maxHeight=50):
    try:
        # open the image
        image = Image.open(imagePath)
    except Exception as e:
        print(e)
        return ""

    # process the image (resize and grayscale)
    image = ResizeImage(image, newWidth, maxHeight)
    image = Grayify(image)
    # convert pixels to ASCII characters
    asciiStr = PixelsToAscii(image)
    # Format the ASCII string into lines based on image width
    asciiStrLen = len(asciiStr)
    asciiImg = "\n".join(asciiStr[i:i + newWidth] for i in range(0, asciiStrLen, newWidth))
    # return the ASCII text
    return asciiImg    

def SelectImage():
    # open a file dialog to select an image file
    imagePath = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("JPEG files", "*.jpg *.jpeg"), 
                   ("PNG files", "*.png"), 
                   ("BMP files", "*.bmp"), 
                   ("GIF files", "*.gif"), 
                   ("All Files", "*.*")]
    )

    if imagePath:
        # get the width of the text area in characters
        textWidth = textArea.winfo_width() // tkFont.Font(font=textArea.cget("font")).measure("M")  # Estimate how many characters fit in the width
        # convert the selected image to ASCII art
        asciiArt = ImageToAscii(imagePath, newWidth=textWidth, maxHeight=50)
        # clear the text area and insert the new ASCII art
        textArea.delete(1.0, tk.END)
        textArea.insert(tk.END, asciiArt)


# MAIN APP
if __name__ == "__main__":
    # create a main window
    root = tk.Tk()
    root.geometry("1000x700") # set initial window size (width x height)
    root.minsize(600, 400)    # set minimum window size
    root.title("Image to ASCII")
    # create a button to select an image
    selectButton = tk.Button(root, text="Select Image", command=SelectImage, font=("Helvetica", 12))
    selectButton.pack(pady=10)
    # create a scrollable text area to display the ASCII art
    textArea = Text(root, wrap=tk.NONE, height=40, width=80, font=tkFont.Font(family="Courier", size=8))
    textArea.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
    # add a scrollbar to the text area
    scrollbar = Scrollbar(root, command=textArea.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    textArea.config(yscrollcommand=scrollbar.set)
    # start the GUI event loop
    root.mainloop()