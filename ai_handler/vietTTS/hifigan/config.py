from pathlib import Path
from typing import NamedTuple


class FLAGS:
    import os

    current_directory = os.path.dirname(__file__)
    ckpt_dir = Path(current_directory + "/../assets/infore/hifigan")
    # ckpt_dir = Path("D:/PBL6/Test/vietTTS/assets/infore/hifigan")
