import re
import unicodedata
from pathlib import Path
import soundfile as sf

from .hifigan.mel2wave import mel2wave
from .nat.config import FLAGS
from .nat.text2mel import text2mel

import os

current_directory = os.path.dirname(__file__)


# def synthesize_text(text, output_path, sample_rate=16000, silence_duration=0.2, lexicon_file="D:/PBL6/Test/vietTTS/assets/infore/lexicon.txt"):
def synthesize_text(
    text,
    output_path,
    sample_rate=16000,
    silence_duration=0.2,
    lexicon_file=current_directory + "/assets/infore/lexicon.txt",
):
    def nat_normalize_text(text):
        text = unicodedata.normalize("NFKC", text)
        text = text.lower().strip()
        sil = FLAGS.special_phonemes[FLAGS.sil_index]
        text = re.sub(r"[\n.,:]+", f" {sil} ", text)
        text = text.replace('"', " ")
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[.,:;?!]+", f" {sil} ", text)
        text = re.sub("[ ]+", " ", text)
        text = re.sub(f"( {sil}+)+ ", f" {sil} ", text)
        return text.strip()

    normalized_text = nat_normalize_text(text)
    print("Normalized text input:", normalized_text)
    mel = text2mel(normalized_text, lexicon_file, silence_duration)
    wave = mel2wave(mel)
    print("Writing output to file", output_path)
    sf.write(output_path, wave, samplerate=sample_rate)


# Sử dụng hàm synthesize_text với các tham số cụ thể
# Ví dụ:
# synthesize_text("tôi muốn tổng hợp giọng nói từ văn bản này", output_path="output.wav", sample_rate=22050, silence_duration=0.2, lexicon_file="lexicon.txt")
