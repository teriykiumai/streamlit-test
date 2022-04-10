import numpy as np
import string

# 音楽理論の参考サイト https://watanabejunya.com/
class Diatonic:
    def __init__(self, target_key="C", scale_type="major"):
        self._flat_keys = ["C", "D♭", "D", "E♭", "E", "F", "G♭", "G", "A♭", "A", "B♭", "B"]
        self._sharp_keys = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        self._keys = [self._flat_keys, self._sharp_keys]
        # self.italy_keys = ["ド", "レ♭", "レ", "ミ♭", "ミ", "ファ", "ソ♭", "ソ", "ラ♭", "ラ", "シ♭", "シ"]
    
    def _change_pattern(self, keys):
        target_index = keys.index(self.target_key)
        # 主Keyを先頭にしてリスト循環させる
        return np.roll(keys, len(keys)-target_index)

    def _select_scale(self):
        """
        numpy filtaに使うbool配列を返す
        """
        if self.scale_type == "major":
            # [全、全、半、全、全、全、半]
            interval = [1, 0, 1, 0 , 1, 1, 0, 1, 0, 1, 0, 1]
        elif self.scale_type == "minor":
            # [全、半、全、全、半、全、全]
            interval = [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0]
        elif self.scale_type == "harmonic_minor":
            interval = [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1]
        elif self.scale_type == "melodic_minor":
            interval = [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1]
        else:
            print("存在しないスケールが指定されています")
            return 
            
        return np.array([True if i==1 else False for i in interval], dtype=bool)
    
    def daitonic(self, target_key="C", scale_type="major"):
        """
        ダイアトニック構成音のリストを返す
            args:
                [0]=key: str
                [1]=scale_type: str
            return: -> list
                [0]=flat_keys [♭]
                [1]=sharp_keys [#]
        """
        self.target_key = target_key
        self.scale_type = scale_type
        
        changed_keys = [self._change_pattern(k) for k in self._keys]
        fillter_scale = self._select_scale()
        self.diatonic_keys = [k[fillter_scale] for k in changed_keys]
        return self.diatonic_keys
    
d = Diatonic()
f_diatonic, s_diatonic = d.daitonic("E", "harmonic_minor")
print(f_diatonic)
print(s_diatonic)

def reform(flat, sharp, mark="#"):
    unique_flat = {k[0] for k in flat}
    unique_sharp = {k[0] for k in sharp}
    if len(unique_flat) == 7:
        print("flat")
        return flat
    if len(unique_sharp) == 7:
        print("sharp")
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
