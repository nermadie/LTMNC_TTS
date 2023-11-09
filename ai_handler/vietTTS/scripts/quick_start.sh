text=`cat assets/transcript.txt`
python -m vietTTS.synthesizer --text "$text" --output assets/infore/clip.wav --lexicon-file assets/infore/lexicon.txt --silence-duration 0.2
