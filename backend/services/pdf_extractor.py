import asyncio

async def extract_text_from_pdf(file_bytes: bytes) -> str:
    await asyncio.sleep(0.1)
    return "Texte extrait du CV..."