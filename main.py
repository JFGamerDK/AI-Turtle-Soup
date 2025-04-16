import streamlit as st
import json
import random
import openai  # 預留 GPT 模型使用

# 嘗試載入題庫
try:
    with open("story_data.json", "r", encoding="utf-8") as f:
        story_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    st.error(f"題庫載入失敗：{e}")
    story_data = []

# 簡單關鍵字判斷
def ai_judge(user_input, story):
    keywords = story.get("keywords", [])
    for keyword in keywords:
        if keyword in user_input:
            return "✅ 是的，有關"
    return "❌ 沒有關係"

# 初始化狀態
if "selected_story" not in st.session_state:
    st.session_state.selected_story = random.choice(story_data) if story_data else {"question": "無題目"}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# 🔁 換一題按鈕邏輯
def restart_game():
    for key in ["selected_story", "chat_history", "user_input"]:
        st.session_state.pop(key, None)
    st.rerun()

# 處理使用者輸入（透過 on_change 觸發）
def handle_input():
    user_input = st.session_state.user_input.strip()
    if user_input:
        st.session_state.chat_history.append({"role": "user", "text": user_input})
        ai_response = ai_judge(user_input, st.session_state.selected_story)
        st.session_state.chat_history.append({"role": "ai", "text": ai_response})
    st.session_state.user_input = ""  # 清空輸入框內容

# UI 標題與題目顯示
st.title("🧠 海龜湯問答遊戲")
st.markdown("### 題目：")
st.markdown(st.session_state.selected_story.get("question", "題目載入失敗"))

# 玩家輸入區（用 on_change 控制觸發）
st.text_input("💬 請輸入你的推理問題：", key="user_input", on_change=handle_input)

# 顯示問答紀錄
st.markdown("---")
st.markdown("### 🧾 問題紀錄：")
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.write(f"👤 玩家：{chat['text']}")
    else:
        st.write(f"🤖 AI：{chat['text']}")

# 換一題按鈕
if st.button("🔁 換一題"):
    restart_game()
