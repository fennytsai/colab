import google.generativeai as genai
from google.colab import userdata


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
