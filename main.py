import google.generativeai as genai
# from google.colab import userdata


import asyncio
from fastapi import FastAPI
import uvicorn

# ─── 1. 建立 FastAPI 網頁伺服器 ───
app = FastAPI()

# 瀏覽器用的 GET 請求
@app.get("/")
async def home_get():
    return {"status": "🤖 誰是臥底機器人 24 暢通運作中！"}

# 專門給 UptimeRobot 用的 HEAD 請求（完全不帶 request 參數，避免底層解析出錯）
@app.head("/")
async def home_head():
    return None  # HEAD 請求依照 HTTP 規範本來就不需要回傳內容，給個空值即可




# 讀取金鑰: api_keys 是一個變數,不要加引號
# api_keys = userdata.get('GEMINI_KEY')
api_keys = os.getenv('GEMINI_KEY')
genai.configure(api_key=api_keys)




def diagnose_quota():
    print("=== 權限診斷開始 ===")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f" 檢查模型: {m.name}")
                try:
                    test_model = genai.GenerativeModel(m.name)
                    test_model.generate_content(
                        "hi",
                        generation_config={"max_output_tokens": 1}
                    )
                    print(f" 狀態: 正常可用")
                except Exception:
                    print(f" 狀態: 被封鎖 (可能是 Limit 0)")
    except Exception as e:
        print(f" 發生嚴重錯誤: {e}")




diagnose_quota()


'''
基本必備
'''
async def main():
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        print("❌ 錯誤：找不到環境變數 DISCORD_TOKEN")
        return

    config = uvicorn.Config(app, host="0.0.0.0", port=10000, log_level="info")
    server = uvicorn.Server(config)

    await asyncio.gather(
        server.serve(),
        bot.start(TOKEN)
    )

if __name__ == "__main__":
    asyncio.run(main()) 


