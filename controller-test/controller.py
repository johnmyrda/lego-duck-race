import hid

keymap = {
    # Bitmask : Keyname
    0b00000001 : 'k1',
    0b00000010 : 'k2',
    0b00000100 : 'k3',
    0b00001000 : 'k4',
    0b00010000 : 'k5',
    0b00100000 : 'k6',     
    0b01000000 : 'k7',      
    0b10000000 : 'k8',
    # K9-13 are in the second bitfield      
    # 0b00000001 : 'k9',
    # 0b00000010 : 'k10',
    # 0b00000100 : 'k11',
    # 0b00001000 : 'k12',
    # 0b00010000 : 'k13' 
}

# Enumerate devices to get ids
for device in hid.enumerate():
    print(f"0x{device['vendor_id']:04x}:0x{device['product_id']:04x} {device['product_string']}")


# Initialize Gamepad
gamepad = hid.device()
gamepad.open(0x32be, 0x2000)
gamepad.set_nonblocking(True)

while True:
    report = gamepad.read(64)
    if report:
        key1 = report[0] # K1-8
        key2 = report[1] # K9-13
        print(report)
        if(key1 in keymap.keys()):
            print(keymap[key1])

# TODO: Write joypad class
# TODO: Implement command pattern
