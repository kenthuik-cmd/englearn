import random
import streamlit as st

VOCAB_LIST = [
    {"word": "achieve", "phonetic": "/əˈtʃiːv/", "meaning": "v. 实现，达成", "example": "You can achieve your goals with hard work."},
    {"word": "benefit", "phonetic": "/ˈbenɪfɪt/", "meaning": "n. 利益，好处", "example": "Regular exercise is of great benefit to health."},
    {"word": "challenge", "phonetic": "/ˈtʃælɪndʒ/", "meaning": "n./v. 挑战", "example": "We are ready to face any challenge."},
]

st.title("📖 常用英语单词训练")

if "queue" not in st.session_state:
    st.session_state.queue = list(VOCAB_LIST)
    random.shuffle(st.session_state.queue)

if st.session_state.queue:
    current = st.session_state.queue[0]
    st.subheader(current["word"])
    st.write(f"**音标**: {current['phonetic']}")
    st.write(f"**释义**: {current['meaning']}")
    st.write(f"*例句*: {current['example']}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("❌ 模糊 (重练)"):
            st.session_state.queue.append(st.session_state.queue.pop(0))
            st.rerun()
    with col2:
        if st.button("✔ 认识 (下一个)"):
            st.session_state.queue.pop(0)
            st.rerun()
else:
    st.success("太棒了！当前单词已全部学完！")
    if st.button("重新开始"):
        st.session_state.queue = list(VOCAB_LIST)
        random.shuffle(st.session_state.queue)
        st.rerun()
