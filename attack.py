import base64
import binascii
import argparse
import urllib.parse

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
        decoded_bytes = encoded_content.encode('rot_13')
    else:
        raise ValueError("Unsupported encoding type")
    
    return decoded_bytes.decode('utf-8')

def decode_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file:
        encoded_content = input_file.read().strip()
    
    encoding_type = detect_encoding(encoded_content)
    
    if encoding_type is None:
        raise ValueError("Unable to detect encoding type")
    
    decoded_content = decode_content(encoded_content, encoding_type)
    
    with open(output_file_path, 'w') as output_file:
        output_file.write(decoded_content)
    
    print(f"Detected encoding type: '{encoding_type}'")
    print(f"Decoded content written to file: {output_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decode an encoded file")
    parser.add_argument("input_file", help="Path to the input encoded file")
    parser.add_argument("output_file", help="Path to the output decoded file")
    args = parser.parse_args()

    decode_file(args.input_file, args.output_file)
