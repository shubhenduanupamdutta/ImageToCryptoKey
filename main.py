"""This module created BitCoin keys based upon images provided."""

import secrets
import hashlib
import binascii
import datetime as dt
from time import sleep
import pandas as pd
import base58
import image_to_data as itd
import glob

HEX_CODES = list(range(16))
NUMBER_OF_KEYS = 2357
HEX_DIGIT = "0123456789ABCDEF"


def convert_to_list(image_df: pd.DataFrame) -> list:
    """converts dataframe (formed from and image excel to a list of data."""
    final_list = []
    for data_column in image_df.columns:
        tmp_list = image_df[data_column].tolist()
        final_list += tmp_list
    return final_list


def create_keys(data_as_list: list) -> list:
    """Creates a list of keys (of 64 char of hexadecimal digits) from a data list."""
    tmp_key_list = []
    while len(data_as_list) > 0:
        # print("Entered while loop")
        print("Data left: ", len(data_as_list))
        tmp_string = ""
        for _ in range(64):
            try:
                index = secrets.choice(range(len(data_as_list)))
                tmp_string += str(HEX_DIGIT[data_as_list[index] % 16])
                data_as_list.pop(index)
            except IndexError:
                tmp_string += HEX_DIGIT[(secrets.choice(HEX_CODES))]
        tmp_key_list.append(tmp_string)
    return tmp_key_list


# print(key_list)
#
# print(len(key_list))


def gen_WIF(key_string: str) -> list:
    """Generated WIF and WIF-compressed keys for bitcoin wallet from 64 char hexadecimal strings."""
    # print(key)
    # time.sleep(5)
    # extended_key = '80e25b59b3db026882fff960da5b6e67b62547b885d131e18e2f66b1fe4976305d01'

    extended_key = "80" + key_string
    extended_key_2 = extended_key + '01'

    key = [extended_key, extended_key_2]
    # print(extended_key)
    # print(extended_key_2)

    # print(key)

    first_sha256, second_sha256 = [], []
    for i, cur_key in enumerate(key):
        first_sha256.append(hashlib.sha256(binascii.unhexlify(cur_key)).hexdigest())
        second_sha256.append(hashlib.sha256(binascii.unhexlify(first_sha256[i])).hexdigest())

    # add checksum to end of extended key
    final_key = []
    for i, cur_key in enumerate(key):
        final_key.append(cur_key + second_sha256[i][:8])

    # Wallet Import Format = base 58 encoded final_key
    WIF = []
    for keys in final_key:
        WIF.append(base58.b58encode(binascii.unhexlify(keys)))

    return WIF


def convert_key_list_to_WIF(keys: list) -> list:
    """Converts hexadecimal string keys to WIF and WIF compressed keys"""
    all_keys = []
    for key in keys:
        wif_keys = []
        if len(key) == 64:
            wif_keys = gen_WIF(key)
        all_keys += wif_keys
    return all_keys


# WIF_KEYS = convert_key_list_to_WIF(key_list)
# print(WIF_KEYS)
# print("\n\n\n\n")
# print(len(WIF_KEYS))


def export_keys_to_txt_file(wif_keylist: list):
    """
    This function takes in a list of Private Keys and writes them in a text file.
    :param wif_keylist: Takes in a list of BitCoin Private Keys
    :return: None
    """
    str_key = ""
    for wif_key in wif_keylist:
        wif_str_key = str(wif_key)
        str_key += str(wif_str_key[2:-1])
        str_key += "\n"
    # print(str_key)

    now = dt.datetime.now()
    now_str = now.strftime("%Y%m%d_%H%M%S")
    file_name = f"image_keys_{now_str}.txt"
    with open(file_name, "w", encoding="UTF-8") as new_key_file:
        new_key_file.write(str_key)


# export_keys_to_txt_file(WIF_KEYS)

# collect all .jpg and .png files from ImageFile folder
image_files = glob.glob("ImageFiles/*.jpg") + glob.glob("ImageFiles/*.png")
# print(image_files)

for filename in image_files:
    # data_list = []
    print(filename)
    data_list = itd.convert_image_to_list(filename)
    print("Image Converted to List")
    # print(data_list)
    print(len(data_list))
    key_list = create_keys(data_list)
    print("Keys Created")
    WIF_KEYS = convert_key_list_to_WIF(key_list)
    print("WIF Keys Created")
    export_keys_to_txt_file(WIF_KEYS)
    print("Keys Exported")
    print("Sleeping for 7 seconds")
    sleep(7)



# key_list = create_keys(data_list)
# # print(key_list)
# #
# # print(len(key_list))
#
#
# def gen_WIF(key_string: str) -> list:
#     """Generated WIF and WIF-compressed keys for bitcoin wallet from 64 char hexadecimal strings."""
#     # print(key)
#     # time.sleep(5)
#     # extended_key = '80e25b59b3db026882fff960da5b6e67b62547b885d131e18e2f66b1fe4976305d01'
#
#     extended_key = "80" + key_string
#     extended_key_2 = extended_key + '01'
#
#     key = [extended_key, extended_key_2]
#     # print(extended_key)
#     # print(extended_key_2)
#
#     # print(key)
#
#     first_sha256 = []
#     second_sha256 = []
#     for i in range(len(key)):
#         first_sha256.append(hashlib.sha256(binascii.unhexlify(key[i])).hexdigest())
#         second_sha256.append(hashlib.sha256(binascii.unhexlify(first_sha256[i])).hexdigest())
#
#     # add checksum to end of extended key
#     final_key = []
#     for i in range(len(key)):
#         final_key.append(key[i] + second_sha256[i][:8])
#
#     # Wallet Import Format = base 58 encoded final_key
#     WIF = []
#     for keys in final_key:
#         WIF.append(base58.b58encode(binascii.unhexlify(keys)))
#
#     return WIF
#
#
# def convert_key_list_to_WIF(keys: list) -> list:
#     """Converts hexadecimal string keys to WIF and WIF compressed keys"""
#     all_keys = []
#     for key in keys:
#         wif_keys = []
#         if len(key) == 64:
#             wif_keys = gen_WIF(key)
#         all_keys += wif_keys
#     return all_keys
#
# WIF_KEYS = convert_key_list_to_WIF(key_list)
# # print(WIF_KEYS)
# # print("\n\n\n\n")
# # print(len(WIF_KEYS))
#
# def export_keys_to_txt_file(wif_keylist: list):
#     str_key = ""
#     for wif_key in wif_keylist:
#         wif_str_key = str(wif_key)
#         str_key += str(wif_str_key[2:-1])
#         str_key += "\n"
#     # print(str_key)
#
#     now = dt.datetime.now()
#     now_str = now.strftime("%Y%m%d_%H%M%S")
#     file_name = f"image_keys_{now_str}.txt"
#     with open(file_name, "w") as new_key_file:
#         new_key_file.write(str_key)
#
# export_keys_to_txt_file(WIF_KEYS)
