import streamlit as st
import json
import random
import openai  # OpenAI 的 GPT 模型

# 載入題庫，加入錯誤處理
try:
    with open("story_data.json", "r", encoding="utf-8") as f:
        story_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    st.error(f"題庫載入失敗：{e}")
    story_data = []

# 一個範例判斷邏輯（也可以直接用你預設的關鍵字匹配）
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

# 玩家輸入提問
user_input = st.text_input("💬 請輸入你的推理問題：", "").strip()

# 玩家輸入後按 Enter
if user_input:
    st.session_state.chat_history.append({"role": "user", "text": user_input})

    # ✅ AI 來判斷這句話是不是有關鍵字（也可以改成 GPT 模型）
    ai_response = ai_judge(user_input, st.session_state.selected_story)
    st.session_state.chat_history.append({"role": "ai", "text": ai_response})

# 顯示對話紀錄（目前只顯示提問）
st.markdown("---")
st.markdown("### 🧾 問題紀錄：")
for chat in st.session_state.chat_history:
    st.write(f"👤 玩家：{chat['text']}")

# 重新開始按鈕
if st.button("🔁 換一題"):
    st.session_state.selected_story = random.choice(story_data) if story_data else {"question": "無題目"}
    st.session_state.chat_history = []
    st.experimental_rerun()
