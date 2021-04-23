import string
import struct
from decimal import Decimal 
from alarm_code import ALARM_CODE
ITEM = "item"
LENGTH = "length"
GET_MESSAGE = "get_message"
INVALID = "Invalid"

TRUE_STATES = ['1', 'on', 'true']
FALSE_STATES = ['0', 'off', 'false']
BINARY_STATES = TRUE_STATES + FALSE_STATES

MSG_MUST_BE_HEX_DIGITS = "Only hex digits allowed"
MSG_MUST_BE_STR = "Only string input allowed"
MSG_MUST_BE_BINARY = f"Must be from {BINARY_STATES}"
MSG_LENGTH_X = lambda x: f"Must be length {x}"

def hex_to_dec(s, subtract='0'):
    assert type(s) == str, MSG_MUST_BE_STR
    assert all([c in string.hexdigits for c in s]), MSG_MUST_BE_HEX_DIGITS
    return str(int(s, 16) - int(subtract, 16))

def bin_to_dec(s):
    assert (type(s) == str), MSG_MUST_BE_STR
    assert (all([c in BINARY_STATES for c in s])), MSG_MUST_BE_HEX_DIGITS
    return str(int(s, 2))

def get_bool(s):
    assert type(s) == str, MSG_MUST_BE_STR
    assert s in BINARY_STATES, MSG_MUST_BE_BINARY
    
    if (s in FALSE_STATES):
        return 'false'
    return 'true'

def hex_to_binary_int_string(s, n=None):
    assert type(s) == str, MSG_MUST_BE_STR
    if (n == None):
        n = 4*len(s)
    s = hex_to_dec(s)
    
    data_status_binary = format(int(s), f"0{n}b")
    
    return data_status_binary

def hex_to_binary_string_list(s, number_of_bits, selected_bits=None):
    data_status_binary = hex_to_binary_int_string(s, number_of_bits)
    if (selected_bits == None):
        selected_bits = number_of_bits
    data_status = [get_bool(data_status_binary[i]) for i in range(selected_bits)]
    
    return data_status
    

def invert_string(s):
    assert s in {"true", "false"}, "Only True or False input allowed"
    if (s == "true"):
        return "false"
    return "true"

def get_data_status(s):
    data_status = hex_to_binary_string_list(s, 4, 3)
    
    data_status[2] = invert_string(data_status[2])
    return data_status

def binary_to_on_off(s):
    assert s in BINARY_STATES, MSG_MUST_BE_BINARY
    
    if (s in FALSE_STATES):
        return 'off'
    return 'on'

def get_digital_io_status(s):
    digital_io_status = hex_to_binary_string_list(s, 16)
    
    return [
        invert_string(digital_io_status[0]),
        digital_io_status[1],
        digital_io_status[2],
        digital_io_status[9],
        digital_io_status[10],
        digital_io_status[15],
        digital_io_status[5],
    ]
    
def get_alarm(s):
    assert all([c in string.hexdigits for c in s]), MSG_MUST_BE_HEX_DIGITS
    assert (len(s) == 2), MSG_LENGTH_X(2)
    
    if (s[0] in string.digits):
        if (s[1] in string.digits):
            if (int(s) > 37):
                return [s, '']
            elif(int(s) <= 9):
                return ['0', '']
            else:
                return [s, ALARM_CODE[s]]
        else:
            if(int(s[0]) == 0):
                return ['0', '']
            return [s[0], ALARM_CODE[s[0]]]
    
    return ["NaN", '']
def get_reverse(s):
    assert all([c in string.hexdigits for c in s]), MSG_MUST_BE_HEX_DIGITS
    assert len(s) == 2, MSG_LENGTH_X(2)
    
    satelite = "GPS+Beidou satellite system"
    if (s[0] in {'0', '1', '2', '3'}):
        satelite = "GPS+Glonass satellite system"
    elif (s[0] in {'4', '5', '6', '7', 'c', 'd', 'e', 'f'}):
        satelite = "GPS+Galileo satellite system"
        
    return [satelite, 'false', 'false']

def get_battery(s):
    assert all([c in string.hexdigits for c in s]), MSG_MUST_BE_HEX_DIGITS
    assert len(s) == 2, MSG_LENGTH_X(2)
    if (s[0] in string.digits and s[1] in string.digits):
        if (s == '00'):
            return '100'
        else:
            return str(int(s))
    return "NaN"

def hex_to_float(s):
    assert all([c in string.hexdigits for c in s]), MSG_MUST_BE_HEX_DIGITS
    assert len(s) == 8, MSG_LENGTH_X(8)
    s = s[6:] + s[4:6] + s[2:4] + s[:2]
    
    return str(Decimal(str(struct.unpack('!f', bytes.fromhex(s))[0])).normalize())

def make_decimal(s, n):
    # if (s == '0000'):
    #     return '0'
    s = ''.join(c for c in s if c.isdigit())
    if (len(s) == 0):
        return "NaN"
    s = s.zfill(4)
    assert n <= len(s), "n must be less than length of decimal"
        
    s = s[:n] + '.' + s[n:]
    return str(Decimal(s).normalize())

    
decode_items = {
        1 : { 
                ITEM : "Message" ,
                LENGTH : 6,
                GET_MESSAGE :  (lambda x: "Alarm message")
            }, 
        2 : { 
                ITEM : "Message Length" ,
                LENGTH : 4,
                GET_MESSAGE :  (lambda x: hex_to_dec(x))
            }, 
        3 : { 
                ITEM : "Serial no" ,
                LENGTH : 4,
                GET_MESSAGE :  (lambda x: hex_to_dec(x))
            }, 
        4 : { 
                ITEM : "IMEI" ,
                LENGTH : 16,
                GET_MESSAGE :  (lambda x: hex_to_dec(x))
            },
        5 : { 
                ITEM : "Acc on interval" ,
                LENGTH : 4,
                GET_MESSAGE :  (lambda x: hex_to_dec(x))
            },
        6 : { 
                ITEM : "Acc off interval" ,
                LENGTH : 4,
                GET_MESSAGE :  (lambda x: hex_to_dec(x))
            }, 
        7 : { 
                ITEM : "Angle compensation" ,
                LENGTH : 2,
                GET_MESSAGE :  (lambda x: hex_to_dec(x))
            },
        8 : { 
                ITEM : "Distance compensation" ,
                LENGTH : 4,
                GET_MESSAGE :  (lambda x: hex_to_dec(x))
            },
        9 : { 
                ITEM : "Speed Alarm" ,
                LENGTH : 4,
                GET_MESSAGE :  (lambda x: f"Over speed setting:{hex_to_dec(x[0:2])}km/h;Network signal:{hex_to_dec(x[2:4])}")
            },
        10 : { 
                ITEM : "data status" ,
                LENGTH : 2,
                GET_MESSAGE :  (lambda x: f"""History data:{get_data_status(x[0])[0]} ;GNSS data:{get_data_status(x[0])[1]} ;
                                GNSS working:{get_data_status(x[0])[2]} ;satellite number:{hex_to_dec(x[1])}""")
            },
        11 : {
                ITEM : "Gsensor manager status",
                LENGTH : 2,
                GET_MESSAGE : (lambda x: f"""Gsensor:{hex_to_dec(x[0])} Admin manager 1 open:{hex_to_binary_string_list(x[1], 4)[3]} ;
                               Admin manager 2 open:{hex_to_binary_string_list(x[1], 4)[2]} ;Admin manager 3 open:{hex_to_binary_string_list(x[1], 4)[1]} ;
                               Admin manager 4 open:{hex_to_binary_string_list(x[1], 4)[0]}""")
            },
        12 : {
                ITEM : "Other",
                LENGTH : 2,
                GET_MESSAGE : (lambda x: f"""Lock sim:{hex_to_binary_string_list(x[1], 4)[3]} ;
                               Lock tracker:{hex_to_binary_string_list(x[1], 4)[2]} 
                               Antitheft:off({hex_to_binary_string_list(x[1], 4)[0]}) ;
                               Vibration level:{hex_to_dec(x[1])}""")
            },
        13 : {
                ITEM : "Heartbeat(minute)",
                LENGTH : 2,
                GET_MESSAGE : (lambda x: hex_to_dec(x))
            },
        14 : {
                ITEM : "Relay status(KM/H)",
                LENGTH : 2,
                GET_MESSAGE : (lambda x: f"""Relay status:{hex_to_binary_string_list(x[0], 4)[1]} ;
                               Relay mode:{bin_to_dec(hex_to_binary_int_string(x[0], 4)[2:])} ;
                               SMS language:1""")
            },
        15 : {
                ITEM : "Drag alarm setting",
                LENGTH : 4,
                GET_MESSAGE : (lambda x: hex_to_dec(x))
            },
        16 : {
                ITEM : "Digital I/O status",
                LENGTH : 4,
                GET_MESSAGE : (lambda x: f"""External power connect:{get_digital_io_status(x)[0]} ;
                               ACC on:{get_digital_io_status(x)[1]} ;
                               AC on:{get_digital_io_status(x)[2]} ;
                               Speaker status:{get_digital_io_status(x)[3]} ;
                               RS232 power on:{get_digital_io_status(x)[4]} ;
                               ACCDET:{get_digital_io_status(x)[5]} ;
                               relay enable:{get_digital_io_status(x)[6]}
                               """)
            },
        17 : {
                ITEM : "Alarm",
                LENGTH : 2,
                GET_MESSAGE : (lambda x: f"""Alarm code:{get_alarm(x)[0]} ;
                               Alarm is:{get_alarm(x)[1]}
                               """)
            },
        18 : {
                ITEM : "Reverse",
                LENGTH : 2,
                GET_MESSAGE : (lambda x: 
                    f"""GPS state:{get_reverse(x)[0]} 
                    SMS alarm open:{get_reverse(x)[1]}:
                    Digtal 2 alarm open:{get_reverse(x)[2]}
                               """)
            },
        19 : {
                ITEM : "Mileage(Meter)",
                LENGTH : 8,
                GET_MESSAGE : (lambda x: hex_to_dec(x))
            },
        20 : {
                ITEM : "Inner battery voltage(V)",
                LENGTH : 2,
                GET_MESSAGE : get_battery
            },
        21 : {
                ITEM : "Mileage(Meter)",
                LENGTH : 12,
                GET_MESSAGE : (lambda x: f"20{x}")
            },
        # 22  Height  [00 00 e8 41]  :   29
        22 : {
                ITEM : "Height",
                LENGTH : 8,
                GET_MESSAGE : hex_to_float
            },
        23 : {
                ITEM : "Longitude",
                LENGTH : 8,
                GET_MESSAGE : hex_to_float
            },
        24 : {
                ITEM : "Latitude",
                LENGTH : 8,
                GET_MESSAGE : hex_to_float
            },
        25 : {
                ITEM : "Reverse",
                LENGTH : 4,
                GET_MESSAGE : (lambda x: "")
            },
        26 : {
                ITEM : "Direction(Degree)",
                LENGTH : 4,
                GET_MESSAGE : hex_to_dec
            },
        27 : {
                ITEM : "External Power Supply Voltage(V)",
                LENGTH : 4,
                GET_MESSAGE : (lambda s: make_decimal(s, 2))
            },
        28 : {
                ITEM : "Speed(km/h)",
                LENGTH : 4,
                GET_MESSAGE : (lambda s: make_decimal(s, 3))
            },
        
         29 : {
                ITEM : "Accumulating fuel consumption(ml)",
                LENGTH : 8,
                GET_MESSAGE : hex_to_dec
            },
         
        30 : {
                ITEM : "Instant fuel consumption(ml)",
                LENGTH : 8,
                GET_MESSAGE : hex_to_dec
            },
        31 : {
                ITEM : "RPM(round per minute)",
                LENGTH : 4,
                GET_MESSAGE : hex_to_dec
            },
        32 : {
                ITEM : "Air input(g/s)",
                LENGTH : 2,
                GET_MESSAGE : (lambda x: INVALID if x == 'ff' else hex_to_dec(x))
            },
        
        33 : {
                ITEM : "Air Press(kpa)",
                LENGTH : 2,
                GET_MESSAGE : (lambda x: INVALID if x == 'ff' else hex_to_dec(x))
            },
        
        34 : {
                ITEM : "Cooling fluid temperature(C)",
                LENGTH : 2,
                GET_MESSAGE : (lambda x: INVALID if x == 'ff' else hex_to_dec(x, '28'))
            },
        35 : {
                ITEM : "Air inflow temperature(C))",
                LENGTH : 2,
                GET_MESSAGE : (lambda x: INVALID if x == 'ff' else hex_to_dec(x, '28'))
            },
        
        
        36 : {
                ITEM : "Engine load(%)",
                LENGTH : 2,
                GET_MESSAGE : (lambda x: INVALID if x == 'ff' else hex_to_dec(x))
            },
        37 : {
                ITEM : "Throttle position(%)",
                LENGTH : 2,
                GET_MESSAGE : (lambda x: INVALID if x == 'ff' else hex_to_dec(x))
            },
        38 : {
                ITEM : "Remain fuel rate(%)",
                LENGTH : 2,
                GET_MESSAGE : (lambda x: INVALID if x == 'ff' else hex_to_dec(x))
            },
}

def format_hex(s):
    new_string = ''
    for i, c in enumerate(s):
        new_string += c
        if (i%2 != 0):
            new_string += ' '
            
    return f'[{new_string[:-1]}]'

def format_output(index, value, s):
    print(index, value[ITEM], format_hex(s), ':', value[GET_MESSAGE](s))

def decode(s, decode_items):
    position = 0
    for index in decode_items:
        value = decode_items[index]
        sub_string = s[position: position + value[LENGTH]]
        position += value[LENGTH]
        format_output(index, value, sub_string)

if __name__ == '__main__':
    s = "2626040053079b08652840427206680014a8c000000000024ac004050100640020160000823a8d002101280053060000e841976fbfc2c650ee410000014b12380000000ce2bb000000000000ff002828000054"
    decode(s, decode_items)