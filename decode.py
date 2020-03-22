#!/usr/bin/env python3
import codecs
import binascii
import socket

scale = 16
#entry = '0xC6 0x57 0x54 0x95 0x5E 0x9E 0x6B 0xC6 0x57 0x54 0x95 0x5E 0x9E 0x6B 0xC6 0x55 0x17 0x55 0x52 0x9E 0x21 '
#Hexa values of start, end and transmission packets
start_packet = '0xC6'
end_packet = '0x6B'
end_transmission = '0x21'
markers = [start_packet, end_packet, end_transmission]
space = '0x20'

#Bin values of start, end and transmission packets
bin_start_packet = '11000110'
bin_end_packet = '01101011'
bin_end_transmission = '00100001'

#Lists ans dictionaries
arr_packet = list()
list_four = list()
list_five = list()
list_eight = list()
hexa = list()
decoded_msg = list()
noSpace = str
input_encode = str

table_1 = {'0000':'11110', '0001':'01001', '0010':'10100', '0011':'10101',
            '0100':'01010', '0101':'01011', '0110':'01110', '0111':'01111',
            '1000':'10010', '1001':'10011', '1010':'10110', '1011':'10111', 
            '1100': '11010', '1101':'11011', '1110':'11100', '1111': '11101' }

def bin_to_hex(s):
    return hex(int(s, 2))

def build_table_inv():
    inv = dict()
    for key, value in table_1.items():
        inv[value] = key
    return inv

table_inv = build_table_inv()

#decode code

#find a key by value
def get_key(val): 
    return table_inv[val]

#find a value by key
def get_value(key):
    for k, value in table_1.items():
        if k == key:
            return value

def get_groups(message):
    split_start = message.strip().split(start_packet)[1:]
    first = split_start[0][1:-5].strip().split()
    second = split_start[1][:-5].strip().split()
    return first, second

def get_groups_no_markers(message):
    sp = message.split()
    groups = []
    LEN = 4
    for i in range(0, len(sp), LEN):
        groups.append(sp[i:i + LEN])
    return groups

def hex_to_bin(h):
    b = int(h[2:], 16)
    b = bin(b)[2:]
    b = '0' * (8 - len(b)) + b
    return b

def byte_to_hex(line):
    return line.hex()

def hex_to_hex(line):
    h = []
    for i in range(0, len(line), 2):
        h.append('0x' + line[i:i + 2].upper())
    return ' '.join(h)

def hex_group_to_bin_group(group):
    return [hex_to_bin(h) for h in group]

def group_to_five_group(group):
    line = ''.join(group)
    five = []
    for i in range(0, len(line), 5):
        five.append(line[i:i + 5])
    return five

def four_group_to_five_group(four):
    return [table_1[f] for f in four]

def five_group_to_four_group(five):
    return [table_inv[f] for f in five]

def eigth_to_four_group(eight):
    line = ''.join(eight)
    four = []
    for i in range(0, len(line), 4):
       four.append(line[i:i + 4])
    return four

def four_to_eight_group(four):
    line = ''.join(four)
    eight = []
    for i in range(0, len(line), 8):
       eight.append(line[i:i + 8])
    return eight

def five_to_eight_group(five):
    line = ''.join(five)
    eight = []
    for i in range(0, len(line), 8):
       eight.append(line[i:i + 8])
    return eight

def bin_group_to_hex_group(group):
    return [bin_to_hex(b) for b in group]

#def hex_message_to_bin_message(hex_message):
#    tokens = hex_message.split()
#    for token in tokens:
#

#Decode the inittial message and return a inverted message input of encoded

def hex_to_ascii(s):
    return bytes.fromhex(s[2 : ]).decode('utf-8')

def hex_group_to_ascii(group):
    return [hex_to_ascii(h) for h in group]

def hex_list_to_str(lis):
    return ''.join(lis).strip()

def low_upper(str):
    return "".join(s.upper() if i%2 == 0 else s.lower() for i,s in enumerate(str))

def white_to_under(s):
    return s.replace(" ", "_")

def invert_message(s):
    return s[::-1]

def letter_to_hex(s):
    return s.encode("utf-8").hex()

def letter_to_bin(s):
    binMessage = bin(int(s, scale)).zfill(8)
    return binMessage

def size_div_4(str):
    size = len(str)
    l = str.split()
    while size % 4 != 0:    
        size = size + 1
        l.append('_')
    s = ''.join(l)
    return s

def encode_msg_to_hex(s):
    return ['0x' + letter_to_hex(h) for h in s]

def hex_str_to_int(s):
    hex_str = s 
    hex_int = int(hex_str, 16)
    return hex_int

def hex_group_to_int_group(s):
    return [hex_str_to_int(h) for h in s]

def xor(s):
    return [h^11 for h in s]

def int_to_hex(s):
    return [hex(h) for h in s]

def decode_message(message):
    # step 1
    group1_hex, group2_hex = get_groups(message)
    print(f'group1_hex = {group1_hex}')
    print(f'group2_hex = {group2_hex}')

    # step 2
    group1_bin = hex_group_to_bin_group(group1_hex)
    group2_bin = hex_group_to_bin_group(group2_hex)
    print(f'group1_bin = {group1_bin}')
    print(f'group2_bin = {group2_bin}')

    group1_five = group_to_five_group(group1_bin)
    group2_five = group_to_five_group(group2_bin)
    print(f'group1_five = {group1_five}')
    print(f'group2_five = {group2_five}')

    group1_four = five_group_to_four_group(group1_five)
    group2_four = five_group_to_four_group(group2_five)
    print(f'group1_four = {group1_four}')
    print(f'group2_four = {group2_four}')

    group1_eight = four_to_eight_group(group1_four)
    group2_eight = four_to_eight_group(group2_four)
    print(f'group1_eight = {group1_eight}')
    print(f'group2_eight = {group2_eight}')

    group1_eight_hex = bin_group_to_hex_group(group1_eight)
    group2_eight_hex = bin_group_to_hex_group(group2_eight)
    print(f'group1_eight_hex = {group1_eight_hex}')
    print(f'group2_eight_hex = {group2_eight_hex}')

    # Step 3
    group12 = group1_eight_hex + group2_eight_hex 
    print(f'group12 = {group12}')

    # Step 4
    hex_ascii = []
    hex_ascii = hex_group_to_ascii(group12)
    print(f'hex_ascii = {hex_ascii}')
    
    #step 5
    str_ascii = hex_list_to_str(hex_ascii)
    print(len(str_ascii))
    print(f'str = {str_ascii}')

    #step 6
    lowUp = low_upper(str_ascii)
    print(f'lowUp = {lowUp}')

    #step 7
    fill_wiht_under = white_to_under(lowUp)
    print(f'fill wiht under = {fill_wiht_under}')

    #invert message
    inverte = invert_message(fill_wiht_under)
    print(f'inverte = {inverte}')
    
    return inverte

def encode_message(str):
    #step 1
    pad_message = size_div_4(str)
    print(f'pad message = {pad_message}')

    #step 2
    encode_to_hex = encode_msg_to_hex(pad_message)
    print(f'encode to hex = {encode_to_hex}')

    #step 3
    groups = ' '.join(encode_to_hex)
    print(groups)

    group1_hex , group2_hex = get_groups_no_markers(groups)
    print(f'group1 = {group1_hex}')
    print(f'group2 = {group2_hex}')
    
    group1_bin = hex_group_to_bin_group(group1_hex)
    group2_bin = hex_group_to_bin_group(group2_hex)
    print(f'group1_bin = {group1_bin}')
    print(f'group2_bin = {group2_bin}')
    
    group1_four = eigth_to_four_group(group1_bin)
    group2_four = eigth_to_four_group(group2_bin)
    print(f'group1_four = {group1_four}')
    print(f'group2_four = {group2_four}')

    group1_five = four_group_to_five_group(group1_four)
    group2_five = four_group_to_five_group(group2_four)
    print(f'group1_five = {group1_five}')
    print(f'group2_five = {group2_five}')

    group1_eight = five_to_eight_group(group1_five)
    group2_eight = five_to_eight_group(group2_five)
    print(f'group1_four = {group1_eight}')
    print(f'group2_four = {group2_eight}')

    group1_eight_hex = bin_group_to_hex_group(group1_eight)
    group2_eight_hex = bin_group_to_hex_group(group2_eight)
    print(f'group1_eight_hex = {group1_eight_hex}')
    print(f'group2_eight_hex = {group2_eight_hex}')

    #step 4
    hex1_to_int = hex_group_to_int_group(group1_eight_hex)
    hex2_to_int = hex_group_to_int_group(group2_eight_hex)
    print(f'hex1_to_int = {hex1_to_int}')
    print(f'hex2_to_int = {hex2_to_int}')

    #step 5
    xor1 = xor(hex1_to_int)
    xor2 = xor(hex2_to_int)
    print(f'xor1 = {xor1}')
    print(f'xor2 = {xor2}')

    int1_to_hex = int_to_hex(xor1)
    int2_to_hex = int_to_hex(xor2)
    
    print(f'xor1 = {int1_to_hex}')
    print(f'xor2 = {int2_to_hex}')

    #Steps 6/7: Adding Start and End Packets
    int1_to_hex.insert(0, start_packet)
    int1_to_hex.append(end_packet)
    int2_to_hex.insert(0, start_packet)
    int2_to_hex.append(end_transmission)
    print(f'xor1 = {int1_to_hex}')
    print(f'xor2 = {int2_to_hex}')

    final_str = int1_to_hex + int2_to_hex
    final_str = ' '.join(final_str)
    return final_str
    print(final_str) 

TCP_IP = '189.6.76.118'
TCP_PORT = 50017
BUFFER_SIZE = 1024
#MESSAGE = b'0xC6 0x5e 0x14 0x5e 0x5a 0x76 0x6B 0xC6 0x5e 0xd7 0x9e 0x7e 0x76 0x21'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
data = s.recv(BUFFER_SIZE)

receive = byte_to_hex(data)
receive = hex_to_hex(receive)
print(f'Input of decode: {receive}')

entrada = decode_message(receive)
entrada = hex_to_hex(entrada)
print(f'Input of send = {encode_message(entrada)}')

my_str = entrada
my_str_as_bytes = str.encode(my_str)
s.send(my_str_as_bytes)
print(my_str_as_bytes)

#my_decoded_str = my_str_as_bytes.decode()
#print(type(my_decoded_str))

s.close()
print("received data:", data)


