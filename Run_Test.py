#!/usr/bin/env python3

import sys


def test_mifarekeys() -> bool:
    from mifarekeys import gen_MifarePWD

    key_A = bytearray.fromhex('A0A1A2A3A4A5')
    key_B = bytearray.fromhex('B0B1B2B3B4B5')

    expected_result = ['8C7F46D76CE01266', '40424446484A7E00', '007E60626466686A']

    results = gen_MifarePWD(key_A, key_B)

    if expected_result == results:
        print("mifarekeys: Test Pass")
        return True

    print("mifarekeys: Test Fail")
    print(f"\tExpected {expected_result}")
    print(f"\tReceived {results}")
    return False


def test_rfidiot_lib() -> bool:

    test_get_error_str()

    test_conversion_functions()

def test_conversion_functions() -> bool:

    return_val = True

    in_val = ["DE", "AD", "BE", "EF"]
    out = [222, 173, 190, 239]
    dat = rfi.HexArrayToList(in_val)
    if dat != out:
        print("HexArrayToList: Test Fail")
        print(f"\t{dat} != {out}")
        return_val = False

    in_val = "DEADBEEF"
    out = [222, 173, 190, 239]
    dat = rfi.HexToList(in_val)
    if dat != out:
        print("HexToList: Test Fail")
        print(f"\t{dat} != {out}")
        return_val = False

    in_val = "DEADBEEF"
    out = ['DE', 'AD', 'BE', 'EF']
    dat = rfi.HexArraysToArray(in_val)
    if dat != out:
        print("HexArraysToArray: Test Fail")
        print(f"\t{dat} != {out}")
        return_val = False

    in_val = "10101010"
    out = "1001100110011001"
    dat = rfi.BinaryToManchester(in_val)
    if dat != out:
        print("BinaryToManchester: Test Fail")
        print(f"\t{dat} != {out}")
        return_val = False
    
    if return_val:
        print("Conversion Functions: Test Pass")

    return return_val

def ToHex(data):
    "convert binary data to hex printable"
    if isinstance(data, (bytes, bytearray)):
        return data.hex()
    string= ''
    for x in range(len(data)):
        string += '%02x' % ord(data[x])
    return string

def test_crypto_functions() -> bool:

    return_val = True

    in_val = b'\xde\xad\xbe\xef'
    out = "dfadbfef"
    dat = rfi.DESParity(in_val).hex()
    if dat != out:
        print("DESParity: Test Fail")
        print(f"\t{dat} != {out}")
        return_val = False
    else:
        print("DESParity: Test Pass")
    
    in_val = b'\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef'
    out = 'ef3489f7b9e6525d5776dafb32ad2c62'
    dat = rfi.DESKey(in_val, rfi.KMAC, 16).hex()
    if dat != out:
        print("DESKey: Test Fail")
        print(f"\t{dat} != {out}")
        return_val = False
    else:
        print("DESKey: Test Pass")
    
    out = b'\x80\x00\x00\x00\x00\x00\x00\x00'
    dat = rfi.PADBlock('')
    if dat != out:
        print("PADBlock: Test Fail")
        print(f"\t{dat} != {out}")
        return_val = False
    
    message = b"The quick brown fox jumps over the lazy dog"
    key = b'\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef'
    ssc = ''
    out = '9be9c94b596eff37'
    dat = rfi.DESMAC(message, key, ssc).hex()
    if dat != out:
        print("DESMAC: Test Fail")
        print(f"\t{dat} != {out}")
        return_val = False
    else:
        print("DESMAC: Test Pass")
    
    message = b"The quick brown fox jumps over the lazy dog"
    #key = b'\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef'
    # key = b'\xde\xad\xbe\xef' *6
    key = b'\xa1\x10n\x08L=uv&vR\x85\xec\xcbp)\xe6Tu\xd0y\xb3*\x07'
    ssc = ''
    out = rfi.DES3MAC(message, key, ssc)
    print("DES3MAC", ToHex(out))

    if return_val:
        print("Crypto Functions: Test Pass")

def test_get_error_str() -> bool:
    # sys.argv.append('-n')
    # import rfidiot
    # $ from rfidiot.RFIDIOt import rfidiot as rid
    # import rfidiot as ri
    # import rfidiot.rfidiot 

    # rid = rfidiot.RFIDIOt.rfidiot()
    # print(dir(rfidiot))
    # print(dir(rfidiot.card))
    # rfi = rfidiot.card
    # print(dir(rid))

    # print("3")
    # rfi = rfidiot()

    test_cases = {
        "6200": "No information given",
        'xxxxxxx': "gemeral error",
        "6700": "Wrong length",
        "6800": "No information given",
        "PC00": "No TAG present!",
        0: "NFC_SUCCESS, Success (no error)",
        -1: "NFC_EIO, Input / output error",
        -80: "NFC_ESOFT Software error",
    }

    for k, v in test_cases.items():
        x = rfi.get_error_str(k)
        if x != v:
            print("get_error_str: Test Fail")
            print(f"\tExpected {v}")
            print(f"\tReceived {x}")
            break
    else:
        print("get_error_str: Test Pass")
        return True

    return False


if __name__ == '__main__':

    print("\n---Script Tests---")
    assert test_mifarekeys()

    print("\n---Module Library Tests---")
    sys.argv.append('-n')
    import rfidiot
    rfi = rfidiot.card
    test_rfidiot_lib()

    test_crypto_functions()



