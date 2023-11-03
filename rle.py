"""rle.py
Iterative run length string encoding/decoding algorithm used in Sokoban Wizard
Note that input strings cannot contain numerals, which are reserved for the encoding multiplier"""

def rle_encode(string: str) -> str:
    """Returns an run-length encoded version of a given string"""
    encoded_string = ""
    current_char = ""
    multiplier = 0
    for next_char in string:
        if current_char == next_char:
            multiplier += 1
        else:
            if multiplier > 1:
                encoded_string += f"{multiplier}"
            encoded_string += next_char
            current_char = next_char
            multiplier = 1
    if multiplier > 0:
        encoded_string += f"{multiplier}"
    return encoded_string

## BUG What if the multiplier is double-digit or greater?
def rle_decode(string: str) -> str:
    """Returns a run-length decoded string from a given encoding"""
    decoded_string = ""
    for next_char in string:
        try:
            multiplier = int(next_char)
            decoded_elem = decoded_string[-1] * (multiplier - 1)
            decoded_string += decoded_elem
        except ValueError:
            decoded_string += next_char
    return decoded_string
