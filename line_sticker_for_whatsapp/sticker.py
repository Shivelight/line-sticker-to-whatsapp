from urllib.request import urlopen
import json
import tempfile
import zipfile
import os
import subprocess
from io import BytesIO

ENDPOINT_PRODUCT_META = "http://dl.stickershop.line.naver.jp/products/0/0/1/{pack_id}/android/productInfo.meta"
ENDPOINT_STICKERS = " http://dl.stickershop.line.naver.jp/products/0/0/1/{pack_id}/iphone/stickers@2x.zip"
ENDPOINT_STICKER_PACK = " http://dl.stickershop.line.naver.jp/products/0/0/1/{pack_id}/iphone/stickerpack@2x.zip "


def get_meta(pack_id):
    body = urlopen(ENDPOINT_PRODUCT_META.format(pack_id=pack_id))
    metadata = json.loads(body.read())
    return metadata


def download_pack(pack_meta):
    sticker_type = pack_meta.get("stickerResourceType", "STATIC")

    if sticker_type == "STATIC":
        download_url = ENDPOINT_STICKERS.format(pack_id=pack_meta["packageId"])
    elif sticker_type in ("ANIMATION"):
        download_url = ENDPOINT_STICKER_PACK.format(pack_id=pack_meta["packageId"])
    else:
        exit(0)

    with tempfile.TemporaryDirectory() as tmpd:
        body = urlopen(download_url)
        with zipfile.ZipFile(BytesIO(body.read())) as zf:
            zf.extractall(tmpd)

        if sticker_type == "STATIC":
            pack_dir = tmpd
        else:
            pack_dir = f"{tmpd}/animation@2x"

        return convert(pack_meta, pack_dir)


def convert(pack_meta, pack_dir):
    stk_name = pack_meta["title"]["en"]
    if not os.path.exists(stk_name):
        os.mkdir(stk_name)

    for sticker in pack_meta["stickers"]:
        stk_id = sticker["id"]
        subprocess.run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-i",
                f"{pack_dir}/{stk_id}@2x.png",
                "-vf",
                "scale=w=512:h=512:force_original_aspect_ratio=1,pad=512:512:(ow-iw)/2:(oh-ih)/2:color=black@0",
                f"{stk_name}/{stk_id}.webp",
            ]
        )

    return stk_name
