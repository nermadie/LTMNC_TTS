from vietTTS.synthesizer import synthesize_text

import time

text = "Anh cho em xin một vé đi tuổi thơ."


synthesize_text(text=text, output_path="output.wav")
