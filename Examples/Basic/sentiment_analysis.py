# =====================
# ==method 1 (which is fail because python error)
# =====================

import re

from Data.Raw.emoji import (
    UNICODE_EMO,
)  # download emoji dataset from https://github.com/NeelShah18/emot/edit/master/emot/emo_unicode.py


def convert_emojis(text):
    for emot in UNICODE_EMO:
        text = re.sub(
            r"(" + emot + ")",
            "_".join(
                UNICODE_EMO[emot].replace(",", "").replace(":", "").split()
            ),
            text,
        )
    return text


text = "game is on 🔥"

convert_emojis(text)


# =====================
# ==method 2
# =====================

from emoji.unicode_codes import UNICODE_EMOJI

s = "\U0001f600"
print(UNICODE_EMOJI[s])
