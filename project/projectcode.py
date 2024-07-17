import cv2
import numpy as np
from PIL import Image
from tkinter import simpledialog
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

#it convert data in binary formate

def data2binary(data):
    if type(data) == str:
        p = ''.join([format(ord(i), '08b')for i in data])
    elif type(data) == bytes or type(data) == np.ndarray:
        p = [format(i, '08b')for i in data]
    return p
# hide data in given img
def hidedata(img, data):
    data += "$$"                                   #'$$'--> secrete key
    d_index = 0
    b_data = data2binary(data)
    len_data = len(b_data)

 #iterate pixels from image and update pixel values

    for value in img:
        for pix in value:
            r, g, b = data2binary(pix)
            if d_index < len_data:
                pix[0] = int(r[:-1] + b_data[d_index])
                d_index += 1
            if d_index < len_data:
                pix[1] = int(g[:-1] + b_data[d_index])
                d_index += 1
            if d_index < len_data:
                pix[2] = int(b[:-1] + b_data[d_index])
                d_index += 1
            if d_index >= len_data:
                break
    return img
def supply():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    user_input = simpledialog.askstring("Input", "Enter data:")

    root.destroy()  # Close the hidden window

    data = user_input
    return data
def encode():
    # Get the image name from the user.
    img_name = filedialog.askopenfilename(title="Select an image", filetypes=[("All Files", "*.*")])
    
    
    # Read the image using OpenCV.
    image = cv2.imread(img_name)
    # Get the image size.
    w, h = Image.open(img_name).size
    # Get the message from the user.
    # Print the text to the console. 
    x = supply()
    data = x
    # Check if the message is empty.
    if len(data) == 0:
        raise ValueError("Empty data")

    # Get the encoded image name from the user.
    enc_img = filedialog.asksaveasfilename(title="Save encoded image", filetypes=[("All Files", "*.*")])

    # Encode the data in the image.
    enc_data = hidedata(image, data)

    # Save the encoded image.
    cv2.imwrite(enc_img, enc_data)

    # Resize the encoded image to the original size.
    img1 = Image.open(enc_img, 'r')
    img1 = img1.resize((w, h), Image.ANTIALIAS)
    # Optimize the encoded image with 65% quality.
    if w != h:
        img1.save(enc_img, optimize=True, quality=100)
    else:
        img1.save(enc_img)

# decoding

def find_data(img):
    bin_data = ""
    for value in img:
        for pix in value:
            r, g, b = data2binary(pix)
            bin_data += r[-1]
            bin_data += g[-1]
            bin_data += b[-1]

    all_bytes = [bin_data[i: i + 8] for i in range(0, len(bin_data), 8)]

    readable_data = ""
    for x in all_bytes:
        readable_data += chr(int(x, 2))
        if readable_data[-2:] == "$$":
            break
    return readable_data[:-2]


def decode():
   

    # Create a Tkinter window
 root = tk.Tk()

    
 img_name = filedialog.askopenfilename(title="Select an image", filetypes=[("All files", "*.*")])

 root.destroy()

    # Decode the image
 image = cv2.imread(img_name)
 img=Image.open(img_name,'r')
 msg = find_data(image)

 print(msg)
 def display_message(message):
    message_window = tk.Toplevel(root)
    message_window.title("Decrypted Data")
    
    # Center the message window on the screen
    window_width = 400
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    message_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Create a label with custom colors for text and background
    label = tk.Label(message_window, text=message, font=("Arial", 14), bg="white", fg="black")

    label.pack(pady=20, padx=20)

 root = tk.Tk()
 root.title("decrypted data")
 window_width = 400
 window_height = 400
 screen_width = root.winfo_screenwidth()
 screen_height = root.winfo_screenheight()
 x = (screen_width // 2) - (window_width // 2)
 y = (screen_height // 2) - (window_height // 2)
 root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create a button to display the decrypted data
 button = tk.Button(root, text='Display Decrypted Data', font=("Arial", 12), command=lambda: display_message(msg))
 button.pack(pady=20)
 
 


def main():
    root = tk.Tk()
    root.title("Image Steganography")
    root.geometry("500x300")
    
    # Create a frame for the background
    background_frame = ttk.Frame(root, style="TFrameStyle.TFrame")
    background_frame.pack(fill="both", expand=True)
    label = ttk.Label(background_frame, text="Submitted by CH Raja Vignesh,22EEB0A33")
    label.pack(side="bottom",pady=20,padx=5)
    # Create a label for the title within the background frame
    title_label = ttk.Label(background_frame, text="Image Steganography", style="TLabelTitle.TLabel")
    title_label.pack(pady=20)

    # Create a frame for instructions within the background frame
    instructions_frame = ttk.Frame(background_frame, style="TFrameStyle.TFrame")
    instructions_frame.pack(pady=10, padx=20, fill="both")

    # Create a label for instructions within the instructions frame
    instructions_label = ttk.Label(instructions_frame, text="Choose the task to be performed:", style="TLabelStyle.TLabel")
    instructions_label.pack()

    # Create a frame for buttons within the background frame
    buttons_frame = ttk.Frame(background_frame, style="TFrameStyle.TFrame")
    buttons_frame.pack(pady=20)

    # Create a button to encode an image within the buttons frame
    encode_button = ttk.Button(buttons_frame, text="Encode", command=encode, style="TButtonEncode.TButton")
    encode_button.pack(side="left", padx=10)

    # Create a button to decode an image within the buttons frame
    decode_button = ttk.Button(buttons_frame, text="Decode", command=decode, style="TButtonDecode.TButton")
    decode_button.pack(side="right", padx=10)

    # Styling
    style = ttk.Style()
    style.configure("TFrameStyle.TFrame", background="#34495e")  # Background color
    style.configure("TLabelTitle.TLabel", font=("Helvetica", 18), foreground="white", background="#34495e")  # Large title label
    style.configure("TLabelStyle.TLabel", font=("Helvetica", 12), foreground="black", background="#ecf0f1")  # Normal labels
    style.configure("TButton.TButton", font=("Helvetica", 12))  # Normal buttons
    style.configure("TButtonEncode.TButton", foreground="black", background="#2ecc71")  # Encode button style
    style.configure("TButtonDecode.TButton", foreground="black", background="#e74c3c")  # Decode button style

    root.mainloop()

if __name__ == "__main__":
    main()