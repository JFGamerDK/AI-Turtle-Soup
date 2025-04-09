import streamlit as st
import json
import random

# 載入題庫
with open("story_data.json", "r", encoding="utf-8") as f:
    story_data = json.load(f)

# 初始化 Session State
if "selected_story" not in st.session_state:
    st.session_state.selected_story = random.choice(story_data)
    st.session_state.chat_history = []

# 顯示題目
st.title("🧠 海龜湯問答遊戲")
st.markdown("### 題目：")
st.markdown(st.session_state.selected_story["question"])

# 玩家輸入提問
user_input = st.text_input("💬 請輸入你的推理問題：", "")

# 當玩家按下 Enter 時
if user_input:
    st.session_state.chat_history.append({"role": "user", "text": user_input})

# 顯示對話紀錄（目前只顯示提問）
st.markdown("---")
st.markdown("### 🧾 問題紀錄：")
for chat in st.session_state.chat_history:
    st.write(f"👤 玩家：{chat['text']}")

# 重新開始按鈕
if st.button("🔁 換一題"):
    st.session_state.selected_story = random.choice(story_data)
    st.session_state.chat_history = st.session_state.chat_history = []
    st.experimental_rerun()
