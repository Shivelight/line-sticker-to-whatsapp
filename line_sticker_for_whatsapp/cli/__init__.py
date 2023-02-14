# SPDX-FileCopyrightText: 2023-present Shivelight <shivelight@tuta.io>
#
# SPDX-License-Identifier: MIT
import click
import os

from ..__about__ import __version__
from .. import sticker


@click.command(
    help="Download and convert LINE sticker pack into WhatsApp compatible format."
)
@click.argument("pack_id", type=int)
@click.version_option(version=__version__, prog_name="LINE Sticker for WhatsApp")
def line_sticker_for_whatsapp(pack_id):
    click.echo(f"Downloading sticker pack metadata with ID {pack_id}")
    pack_meta = sticker.get_meta(pack_id)
    stk_type = pack_meta.get("stickerResourceType", "STATIC (assumed)")
    click.echo(f"Sticker pack name: {pack_meta['title']['en']}")
    click.echo(f"Sticker pack author: {pack_meta['author']['en']}")
    click.echo(f"Sticker pack type: {stk_type}")
    click.echo(f"Downloading and converting sticker pack with ID {pack_id}")
    click.echo(f"Saved to {os.getcwd()}/{sticker.download_pack(pack_meta)}")
