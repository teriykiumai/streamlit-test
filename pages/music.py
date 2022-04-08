import random
import numpy as np
import string

flat_keys = ["C", "D♭", "D", "E♭", "E", "F", "G♭", "G", "A♭", "A", "B♭", "B"]
sharp_keys =["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
# italy_keys = ["ド", "レ♭", "レ", "ミ♭", "ミ", "ファ", "ソ♭", "ソ", "ラ♭", "ラ", "シ♭", "シ"]

def diatonic_coords(keys, target_key="C"):
    l = len(keys)
    key = keys.index(target_key)

    # 第二引数の数で shiht する
    ch_keys = np.roll(keys, l-key)

    def major_coord():
        diatonic = [1, 0, 1, 0 , 1, 1, 0, 1, 0, 1, 0, 1]
        return np.array([True if k==1 else None for k in diatonic], dtype=bool)

    def minor_coord():
        diatonic = [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0]
        return np.array([True if k==1 else None for k in diatonic], dtype=bool)

    def harmonic_minor():
        diatonic = [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1]
        return np.array([True if k==1 else None for k in diatonic], dtype=bool)

    def melodic_minor():
        diatonic = [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1]
        return np.array([True if k==1 else None for k in diatonic], dtype=bool)

    sl = major_coord()
    return ch_keys[major_coord()]
    # return ch_keys[minor_coord()]
    # return ch_keys[harmonic_minor()]
    # return ch_keys[melodic_minor()]

t = "B"
sharp_key = t
flat_key = t
if len(t) != 1:
    if t[-1] == "#":
        idx = sharp_keys.index(t)
        flat_key = flat_keys[idx]
    elif t[-1] == "♭":
        idx = flat_keys.index(t)
        sharp_key = sharp_keys[idx]
        
s_diatonic = diatonic_coords(sharp_keys, sharp_key)
f_diatonic = diatonic_coords(flat_keys, flat_key)

print(s_diatonic)
print(f_diatonic)
print("-"*50)

def reform(flat, sharp, mark="#"):
    unique_flat = {k[0] for k in flat}
    unique_sharp = {k[0] for k in sharp}
    if len(unique_flat) == 7:
        print("No Chage")
        return flat
    if len(unique_sharp) == 7:
        print("No Chage")
        return sharp
    
    
    # [A-G] のアルファベット   
    alpha = list(string.ascii_uppercase)[:7]  
    only_key = [_[0] for _ in flat]
    print(f"yu{only_key}")
    
    # 集合のXORをとる
    unique = list(set(alpha) - set(only_key))
    print(f"途中{unique}")
    
    unique = [u_key+mark for u_key in unique]
    print(f"途中{unique}")
    
    keys_change = [sharp.tolist().index(uk) for uk in unique]
    for k in keys_change:
        flat[k] = sharp[k]
    return flat

# reform(f_diatonic, s_diatonic)
reform(s_diatonic, f_diatonic, "♭")
