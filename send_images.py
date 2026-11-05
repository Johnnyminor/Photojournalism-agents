"""Send billeder til en servet agent og følg samtalen i terminalen.

Brug (fra repo-roden, mens `agents serve` kører for agenten):

    uv run --env-file .env --project foto-culler python send_images.py foto-culler sti/til/batch/*.jpg -m "Vinkel: ..."

Billederne sendes som data-URI'er i samme session, så agenten husker
alt fra tidligere beskeder. Filnavnet uden endelse sendes som frame_id-reference.
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import mimetypes
from pathlib import Path

from mistralai import agents


def image_block(path: Path) -> agents.ImageContentBlock:
    data = base64.b64encode(path.read_bytes()).decode()
    media_type = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    return agents.ImageContentBlock(
        type="image",
        uri=f"data:{media_type};base64,{data}",
        media_type=media_type,
        alt_text=path.stem,
    )


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("agent_name", help="Navn på den servede agent, f.eks. foto-culler")
    parser.add_argument("images", nargs="+", type=Path, help="JPEG-filer der sendes i denne besked")
    parser.add_argument("-m", "--message", default="", help="Tekstbesked der sendes sammen med billederne")
    args = parser.parse_args()

    agent = agents.Agent.load_from(agent_name=args.agent_name)
    session = await agent.start_session()
    print(f"Session {session.id} på {args.agent_name}. Skriv /exit for at slutte.")

    blocks: list = [image_block(p) for p in args.images]
    if args.message:
        blocks.append(agents.TextContentBlock(type="text", text=args.message))

    while True:
        state = await session.run(blocks)
        if isinstance(state, agents.Busy):
            state = await state.turn.result()
        if isinstance(state, agents.Completed):
            print(state.text)
        else:
            print(f"[Tur sluttede: {state}]")

        line = input("\n> ")
        if line.strip() in {"/exit", "exit"}:
            break
        blocks = [agents.TextContentBlock(type="text", text=line)]

    await session.cancel()


if __name__ == "__main__":
    asyncio.run(main())
