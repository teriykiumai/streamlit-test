import numpy as np

# 音楽理論の参考サイト https://watanabejunya.com/
class Keys:
    def __init__(self):
        self.select = ["C", "C#/D♭", "D", "D#/E♭", "E", "F", "F#/G♭", "G", "G#/A♭", "A", "A#/B♭", "B"]
        self.flat = ["C", "D♭", "D", "E♭", "E", "F", "G♭", "G", "A♭", "A", "B♭", "B"]
        self.sharp = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        self.all = [self.flat, self.sharp]


class ScalesCommon:
    """
    スケールの基底クラス
    """
    def __init__(self):
        self.__scale_filter = None
        self.__tonic = None
        self.__dominant = None
        self.__sub_dominant = None
        self.__triad = None
        self.__tetrad = None
        
    @property
    def scale_filter(self):
        # 構成音として使うものを 1, そうでないものを 0 としたリストを格納する。 len=7/12音
        return self.__scale_filter
    @property
    def tonic(self):
        # index番号を格納する
        return self.__tonic
    @property
    def dominant(self):
        # index番号を格納する
        return self.__dominant
    @property
    def sub_dominant(self):
        # index番号を格納する
        return self.__sub_dominant
    @property
    def triad(self):
        # 三和音の場合の付属文字列
        return self.__triad
    @property
    def tetrad(self):
        # 四和音の場合の付属文字列
        return self.__tetrad
    
    def set_parameter(self):
        """
        propertyの値を各クラスの値で更新する
        """
        self.scale_filter()
        self.scale_filter = np.array(self.scale_filter, dtype=bool)
        self.tonic()
        self.dominant()
        self.sub_dominant()
        self.triad()
        self.tetrad()
    
    
class MajorScale(ScalesCommon):
    def __init__(self):
        super().__init__()
        self.set_parameter()

    def scale_filter(self):
        self.scale_filter = [1, 0, 1, 0 , 1, 1, 0, 1, 0, 1, 0, 1]
    def tonic(self):
        # I, Ⅱ, Ⅵ　
        self.tonic = [0, 2, 5]
    def dominant(self):
        self.dominant = [4, 6]
    def sub_dominant(self):
        self.sub_dominant = [3, 1]
    def triad(self):
        self.triad = ["", "m", "m", "", "", "m", "m(♭5)"]
    def tetrad(self):
        self.tetrad = ["M7", "m7", "m7", "M7", "7", "m7", "m7(♭5)"]
         
    def relative_shift(self):
        # 平行調の取得の際にリストをシフトさせるための数 [C] - [Am]
        return 11
     
    
class NaturalMinorScale(ScalesCommon):
    def __init__(self):
        super().__init__()
        self.set_parameter()

    def scale_filter(self):
        self.scale_filter = [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0]
    def tonic(self):
        self.tonic = [0, 2]
    def dominant(self):
        self.dominant = [4, 6]
    def sub_dominant(self):
        self.sub_dominant = [1, 3, 5]
    def triad(self):
        self.triad = ["m", "m(♭5)", "", "m", "m", "", ""]
    def tetrad(self):
        self.tetrad = ["m7", "m7(♭5)", "M7", "m7", "m7", "M7", "7"]
        
    def relative_shift(self):
        # 平行調の取得の際にリストをシフトさせるための数 [C] - [E♭]
        return 5
        
        
class HarmonicMinorScale(ScalesCommon):
    """
    ナチュラルマイナーから七度が半音上がる
    """
    def __init__(self):
        super().__init__()
        self.set_parameter()
        
    def scale_filter(self):
        self.scale_filter = [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1]
    def tonic(self):
        self.tonic = [0, 2]
    def dominant(self):
        self.dominant = [4, 6]
    def sub_dominant(self):
        self.sub_dominant = [1, 3, 5]
    def triad(self):
        self.triad = ["m", "m(♭5)", "aug", "m", "", "", "dim"]
    def tetrad(self):
        self.tetrad = ["mM7", "m7(♭5)", "augM7", "m7", "7", "M7", "dim7"]
        
        
class MelodicMinorScale(ScalesCommon):
    """
    メージャースケールと比較して三度が半音下がる
    """
    def __init__(self):
        super().__init__()
        self.set_parameter()
        
    def scale_filter(self):
        self.scale_filter = [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    def tonic(self):
        self.tonic = [0, 2, 5]
    def dominant(self):
        self.dominant = [3, 4, 6]
    def sub_dominant(self):
        self.sub_dominant = [1]
    def triad(self):
        self.triad = ["m", "m", "aug", "", "", "m(♭5)", "m(♭5)"]
    def tetrad(self):
        self.tetrad = ["mM7", "m7", "augM7", "7", "7", "m7(♭5)", "m7(♭5)"]
        
        
class Scales:
    def __init__(self):
        self.all = {
            "Major": MajorScale(),
            "Minor": NaturalMinorScale(),
            "HarmonicMinor": HarmonicMinorScale(),
            "MelodicMinor": MelodicMinorScale(),
        }
        
        self.select = {
            "Major": MajorScale(),
            "Minor": NaturalMinorScale(),
        }
        
        self.major = {
            "Major": MajorScale()
        }
        
        self.minor = {
            "Minor": NaturalMinorScale(),
            "HarmonicMinor": HarmonicMinorScale(),
            "MelodicMinor": MelodicMinorScale(),
        }


class DiatonicKeys:
    """
    指定したキーのダイアトニック構成音と対応した平行調のダイアトニック構成音を作る
    """
    def __init__(self, target_key="C", scale_type="Major"):
        self.keys = Keys()
        self.scales = Scales()
        
        self.update_keys(target_key="C", scale_type="Major")
        

    def _rotate_keys(self):
        target_index = self.keys.select.index(self.target_key)
        self.rotated_keys = [self._circulate_keys(keys, target_index) for keys in self.keys.all]
    
    def _circulate_keys(self, keys, target_key_index):
        """
        ターゲットKeyを先頭にしてリスト循環させる
        """
        return np.roll(keys, len(keys)-target_key_index)
    
    def _jadge_unique_key(self, pickup_keys):
        """
        白鍵キーが7つ存在している方を返す。なければ先頭要素のリストを返す
        """
        for keys in pickup_keys:
            if len({_[0] for _ in keys}) == 7:
                return keys
        else:
            return pickup_keys[0] 
    
    def _get_scale_keys(self):
        """
        指定したスケールのダイアトニック構成音を抜き出す
        """
        self.diatonic_keys = {}
        if self.scale_type == "Major":
            scales = self.scales.major.items()
        elif self.scale_type == "Minor":
            scales = self.scales.minor.items()
            
        for k, scale in scales:
            scale_filtered_keys = [keys[scale.scale_filter] for keys in self.rotated_keys]
            scale_keys = self._jadge_unique_key(scale_filtered_keys)
            self.diatonic_keys[k] = scale_keys
        
    def _get_relative_keys(self):
        """
        取得したキーとスケールの平行調のダイアトニック構成音を取り出す [C] ⇔ [Am]
        """
        select_scale = self.scales.select[self.scale_type]
        shift = select_scale.relative_shift()
        # 平行調の12音階を取得
        relative_keys = self._circulate_keys(self.rotated_keys, shift)
        
        # 平行調なので選択したスケールとは反対のスケール群を用いる
        if self.scale_type == "Major":
            scales = self.scales.minor.items()
        elif self.scale_type == "Minor":
            scales = self.scales.major.items()
        
        # 平行調のダイアトニックを追加する
        for k, scale in scales:
            relative_filtered_keys = [keys[scale.scale_filter] for keys in relative_keys]
            relative_diatonic = self._jadge_unique_key(relative_filtered_keys)
            self.diatonic_keys[k] = relative_diatonic
            
    def get_diatonic_keys(self):
        return self.diatonic_keys
    
    def update_keys(self, target_key, scale_type):
        # 共通で使うプロパティ
        self.target_key = target_key
        self.scale_type = scale_type
        
        # 実行するメソッド群
        self._rotate_keys()
        self._get_scale_keys()
        self._get_relative_keys()


class DiatonicChords(DiatonicKeys):
    def __init__(self, target_key="C", scale_type="Major", chord_type="fifth"):
        super().__init__(target_key, scale_type)
        # 有効とするリスト群
        self.select_chord_type = ["fifth", "seventh"]
        self.update_chords(target_key, scale_type, chord_type)
        
        
    def _update_chord_type(self):
        """
        和音構成音別に仕分けするために使うパラメータ情報の更新
        """
        if not self.chord_type in self.select_chord_type:
            print("指定できない和音構成です")
            return 
            
        if self.chord_type == "fifth":
            self._add_triad()
            self._clip = -1
        elif self.chord_type == "seventh":
            self._add_tetrad()
            self._clip = None
        
    def _add_triad(self):
        """
        三和音構成の際のコードネームを返す
        """
        for k, scale in self.scales.all.items():
            self._diatonic_chords[k] = [f"{diatonic_key}{add_chara}" for diatonic_key, add_chara in zip(self.diatonic_keys[k], scale.triad)]
        
    def _add_tetrad(self):
        """
        四和音(7thコード)の際のコードネームを返す
        """
        for k, scale in self.scales.all.items():
            self._diatonic_chords[k] = [f"{diatonic_key}{add_chara}" for diatonic_key, add_chara in zip(self.diatonic_keys[k], scale.tetrad)]
   
    def _extract_roles(self):
        """
        スケール毎にトニックなどの役割を果たす属性をグループ分けして返す
        """
        for k, scale in self.scales.all.items():
            roles = {
                "tonic": [self._diatonic_chords[k][idx] for idx in scale.tonic],
                "dominant": [self._diatonic_chords[k][idx] for idx in scale.dominant],
                "sub_dominant":[self._diatonic_chords[k][idx] for idx in scale.sub_dominant]
            }
            self._diatonic_roles[k] = roles
    
    def _extract_composite_chords(self):
        """
        ディグリーネームキーそれぞれの和音構成音を返す
        """
        scales = list(self._diatonic_chords.keys())
        for scale in scales:
            composite = {}
            chords = self._diatonic_chords[scale]
            keys = self.diatonic_keys[scale]
            for chord, key in zip(chords, keys):
                target_idx = list(keys).index(key)
                # ルートから一つ飛ばしで和音を構成する
                composite[chord] = list(self._circulate_keys(keys, target_idx))[0:self._clip:2]
            self._composite_chords[scale] = composite


    def _classification(self):
        """
        主調と平行調を分けて格納する
        """
        if self.scale_type == "Major":
            scale_chords = list(self.scales.major.keys())
            relative_chords = list(self.scales.minor.keys())
        elif self.scale_type == "Minor":
            scale_chords = list(self.scales.minor.keys())
            relative_chords = list(self.scales.major.keys())
            
        self.scale_chords =  {scale: self._diatonic_chords[scale] for scale in scale_chords}
        self.scale_composites = {scale: self._composite_chords[scale] for scale in scale_chords}
        self.scale_roles =  {scale: self._diatonic_roles[scale] for scale in scale_chords}
        
        self.relative_chords =  {scale: self._diatonic_chords[scale] for scale in relative_chords}
        self.relative_composites = {scale: self._composite_chords[scale] for scale in relative_chords}
        self.relative_roles =  {scale: self._diatonic_roles[scale] for scale in relative_chords}
        
    def update_chords(self, target_key, scale_type, chord_type):
        self.update_keys(target_key, scale_type)
        self.chord_type = chord_type

        # 共通で使用するプロパティ
        self._diatonic_chords = {}
        self._diatonic_roles = {}
        self._composite_chords = {}
        
        # 実行するメソッド群
        self._update_chord_type()  
        self._extract_roles()
        self._extract_composite_chords()
        self._classification()

if __name__ == "__main__":
    c_sharp = DiatonicChords("C#/D♭", "Minor", "fifth")
    print(c_sharp._composite_chords)
    
    c_M = DiatonicChords("C", "Major", "fifth")
    print(c_M.relative_chords)
    