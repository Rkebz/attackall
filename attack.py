import base64
import binascii
import urllib.parse
import os
import codecs

def detect_encoding(encoded_content):
    # Check for Base64
    try:
        base64.b64decode(encoded_content)
        return 'base64'
    except binascii.Error:
        pass

    # Check for Hex
    try:
        bytes.fromhex(encoded_content)
        return 'hex'
    except ValueError:
        pass

    # Check for URL encoding
    try:
        decoded_url = urllib.parse.unquote(encoded_content)
        if encoded_content != decoded_url:
            return 'url'
    except Exception:
        pass

    # Check for ROT13
    if all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" for c in encoded_content):
        return 'rot13'
    
    return None

def decode_content(encoded_content, encoding_type):
    if encoding_type == 'base64':
        decoded_bytes = base64.b64decode(encoded_content)
    elif encoding_type == 'hex':
        decoded_bytes = bytes.fromhex(encoded_content)
    elif encoding_type == 'url':
        decoded_bytes = urllib.parse.unquote(encoded_content).encode('utf-8')
    elif encoding_type == 'rot13':
        decoded_bytes = codecs.decode(encoded_content, 'rot_13').encode('utf-8')
    else:
        raise ValueError("Unsupported encoding type")
    
    return decoded_bytes.decode('utf-8')

def decode_file(input_file_path):
    with open(input_file_path, 'r') as input_file:
        encoded_content = input_file.read().strip()
    
    encoding_type = detect_encoding(encoded_content)
    
    if encoding_type is None:
        raise ValueError("Unable to detect encoding type")
    
    decoded_content = decode_content(encoded_content, encoding_type)
    
    output_file_path = os.path.splitext(input_file_path)[0] + '_decoded.txt'
    with open(output_file_path, 'w') as output_file:
        output_file.write(decoded_content)
    
    print(f"Detected encoding type: '{encoding_type}'")
    print(f"Decoded content written to file: {output_file_path}")

if __name__ == "__main__":
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()  # Hide the root window

    input_file_path = filedialog.askopenfilename(title="Select the encoded file")
    
    if input_file_path:
        try:
            decode_file(input_file_path)
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("No file selected")
