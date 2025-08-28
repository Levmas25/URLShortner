import string


BASE62_ALPHABET = string.digits + string.ascii_letters
DIGIT_TO_LETTER_BASE62_DICTIONARY = { num: letter for num, letter in enumerate(BASE62_ALPHABET) }
OFFSET = 10**7


def convert_to_base62(num: int) -> str:
    """
        Converts integer number to base62 
    """
    offset_num = num + OFFSET
    
    if offset_num == 0:
        return '0'

    converted_num = ''
    while offset_num:
        converted_num += DIGIT_TO_LETTER_BASE62_DICTIONARY[offset_num % 62]
        offset_num //= 62
    return converted_num[::-1]