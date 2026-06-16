import os
import asyncio
from fastapi import FastAPI
import uvicorn

from google import genai  # ✅ 新版 SDK

# =========================
# FastAPI
# =========================
app = FastAPI()

@app.get("/")
async def home_get():
    return {"status": "🤖 誰是臥底機器人 24 暢通運作中！"}

@app.head("/")
async def home_head():
    return None


# =========================
# Gemini setup（新版）
# =========================
api_key = os.getenv("GEMINI_KEY")

if not api_key:
    print("❌ 沒有 GEMINI_KEY")

client = genai.Client(api_key=api_key)


def test_gemini():
    try:
        res = client.models.generate_content(
            model="gemini-1.5-flash",
            contents="hi"
        )
        print("✅ Gemini OK:", res.text)
    except Exception as e:
        print("❌ Gemini error:", e)


# ⚠️ 不要在 import 時跑重測（Render 會不穩）
# test_gemini()


# =========================
# Discord bot（你原本沒貼 bot，我先安全處理）
# =========================
bot = None  # ⚠️ 避免 NameError（你要自己補 discord.Bot / commands.Bot）


# =========================
# main entry
# =========================
async def main():
    TOKEN = os.getenv("DISCORD_TOKEN")

    if not TOKEN:
        print("❌ 錯誤：找不到 DISCORD_TOKEN")
        return

    config = uvicorn.Config(app, host="0.0.0.0", port=10000, log_level="info")
    server = uvicorn.Server(config)

    await server.serve()  # ⚠️ 先只跑 API，避免 bot crash


if __name__ == "__main__":
    asyncio.run(main())
