import streamlit as st
import json
import random
import openai  # GPT 模型可擴充

# 載入題庫
try:
    with open("story_data.json", "r", encoding="utf-8") as f:
        story_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    st.error(f"題庫載入失敗：{e}")
    story_data = []

# 關鍵字比對判斷
def ai_judge(user_input, story):
    keywords = story.get("keywords", [])
    for keyword in keywords:
        if keyword in user_input:
            return "✅ 是的，有關"
    return "❌ 沒有關係"

# 初始化 Session State
if "selected_story" not in st.session_state:
    st.session_state.selected_story = random.choice(story_data) if story_data else {"question": "無題目"}
    st.session_state.chat_history = []

# 顯示題目
st.title("🧠 海龜湯問答遊戲")
st.markdown("### 題目：")
st.markdown(st.session_state.selected_story.get("question", "題目載入失敗"))

# 玩家輸入
user_input = st.text_input("💬 請輸入你的推理問題：", "").strip()

# 處理玩家輸入
if user_input:
    st.session_state.chat_history.append({"role": "user", "text": user_input})

    ai_response = ai_judge(user_input, st.session_state.selected_story)
    st.session_state.chat_history.append({"role": "ai", "text": ai_response})

    # ✅ 如果答對，自動換下一題
    if "✅" in ai_response:
        st.success("你猜對了！進入下一題～")
        for key in ["selected_story", "chat_history"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

# 顯示對話紀錄
st.markdown("---")
st.markdown("### 🧾 問題紀錄：")
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.write(f"👤 玩家：{chat['text']}")
    else:
        st.write(f"🤖 AI：{chat['text']}")

# 換一題按鈕（手動）
if st.button("🔁 換一題"):
    for key in ["selected_story", "chat_history"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()
