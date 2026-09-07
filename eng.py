import random
from io import BytesIO
from gtts import gTTS
import streamlit as st
from supabase import create_client
from vocab_data import GLOBAL_VOCAB_DB

# 读取 Supabase 配置
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_ANON_KEY"]
supabase = create_client(url, key)

st.set_page_config(
    page_title="AI 英语进阶闯关", page_icon="🦉", layout="centered"
)

# 注入手机端极简样式（隐藏原生音频播放器，优化进度条颜色）
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        [data-testid="stAudio"] {
            display: none !important;
        }
        
        /* 多邻国风格进度条 */
        .stProgress > div > div > div > div {
            background-color: #58cc02;
        }
        
        .block-container {
            padding-top: 0.5rem;
            padding-bottom: 1rem;
            padding-left: 0.8rem;
            padding-right: 0.8rem;
            max-width: 500px;
        }

        .stButton > button {
            border-radius: 12px;
            font-weight: 600;
            padding: 0.5rem 0.8rem;
            font-size: 14px;
            box-shadow: 0 4px 0px rgba(0, 0, 0, 0.1); /* 多邻国按钮的厚重立体感 */
            transition: all 0.1s;
        }
        
        .stButton > button:active {
            box-shadow: 0 0px 0px rgba(0, 0, 0, 0.1);
            transform: translateY(4px);
        }
        
        .quiz-card {
            background-color: #ffffff;
            border: 2px solid #e5e5e5;
            padding: 20px 18px;
            border-radius: 18px;
            margin-bottom: 12px;
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# === 初始化 Session State ===
if "user" not in st.session_state:
    st.session_state.user = None

if not st.session_state.user and "uid" in st.query_params:
    saved_uid = st.query_params["uid"]
    class AutoLoginUser:
        def __init__(self, uid):
            self.id = uid
    st.session_state.user = AutoLoginUser(saved_uid)
    try:
        profile = supabase.table("user_profiles").select("*").eq("user_id", saved_uid).execute()
        if profile.data:
            st.session_state.level = profile.data[0].get("grade", 1)
    except Exception:
        pass

if "level" not in st.session_state:
    st.session_state.level = 1

if "queues" not in st.session_state:
    st.session_state.queues = {}
    for lvl in range(1, 21):
        q = list(GLOBAL_VOCAB_DB[lvl])
        random.shuffle(q)
        st.session_state.queues[lvl] = q

if "mastered" not in st.session_state:
    st.session_state.mastered = {lvl: [] for lvl in range(1, 21)}

if "page" not in st.session_state:
    st.session_state.page = "home"

# 多邻国红心生命值系统
if "hearts" not in st.session_state:
    st.session_state.hearts = 5


def get_audio_bytes(text):
    tts = gTTS(text=text, lang="en")
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()


def sync_progress_to_cloud(user_id, level, mastered_dict):
    try:
        supabase.table("user_profiles").upsert({
            "user_id": user_id,
            "grade": level,
            "mastered_words": str(len(mastered_dict.get(level, []))),
        }).execute()
    except Exception as e:
        print("同步云端失败:", e)


current_lvl = st.session_state.level
current_queue = st.session_state.queues[current_lvl]
mastered_list = st.session_state.mastered[current_lvl]
all_learned_pool = mastered_list + current_queue

# 未登录拦截
if not st.session_state.user:
    st.markdown(
        "<h3 style='text-align: center; color: #58cc02; margin-top:"
        " 10px;'>🦉 英语闯关打卡 App</h3>",
        unsafe_allow_html=True,
    )

    with st.container():
        email = st.text_input("邮箱地址", placeholder="请输入注册邮箱")
        password = st.text_input("密码", type="password", placeholder="请输入密码")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("登 录", use_container_width=True, type="primary"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state.user = res.user
                    st.query_params["uid"] = res.user.id
                    
                    profile = supabase.table("user_profiles").select("*").eq("user_id", res.user.id).execute()
                    if profile.data:
                        st.session_state.level = profile.data[0].get("grade", 1)
                    st.success("登录成功！")
                    st.rerun()
                except Exception as e:
                    st.error(f"登录失败: {e}")

        with col2:
            if st.button("注 册", use_container_width=True):
                try:
                    res = supabase.auth.sign_up({"email": email, "password": password})
                    st.success("注册成功！请直接登录。")
                except Exception as e:
                    st.error(f"注册失败: {e}")

# 已登录界面
else:
    # ---------------- HOME 主页 ----------------
    if st.session_state.page == "home":
        st.markdown(
            "<h3 style='text-align: center; color: #303133; margin-bottom: 5px;'>🦉 每日英语打卡</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<p style='text-align: center; color: #afafaf; font-size: 14px; margin-bottom: 15px;'>当前通关：<b>Level {current_lvl} / 20</b></p>",
            unsafe_allow_html=True,
        )

        # 首页展示多邻国风格进度条
        progress_pct = min(len(mastered_list) / 100.0, 1.0)
        st.progress(progress_pct)
        st.markdown(f"<p style='text-align: right; font-size: 12px; color: #58cc02; font-weight: bold;'>进度 {len(mastered_list)}/100 词</p>", unsafe_allow_html=True)

        st.write("")
        if st.button("🚀 继续学习新词汇", use_container_width=True, type="primary"):
            st.session_state.page = "study"
            st.rerun()

        st.write("")
        if st.button("🎯 进入红心生存小测", use_container_width=True):
            st.session_state.page = "quiz"
            st.rerun()

        st.write("")
        if st.button("🔁 查看已学单词重温", use_container_width=True):
            st.session_state.page = "review"
            st.rerun()

        st.markdown("---")
        if st.button("🚪 退出登录", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = "home"
            if "uid" in st.query_params:
                del st.query_params["uid"]
            st.rerun()

    # ---------------- 子页面 ----------------
    else:
        if st.button("⬅️ 返回主页", type="secondary"):
            st.session_state.page = "home"
            st.rerun()

        # ==========================================
        # 📚 核心背单词模式
        # ==========================================
        if st.session_state.page == "study":
            # 顶部进度条
            progress_pct = min(len(mastered_list) / 100.0, 1.0)
            st.progress(progress_pct)
            st.markdown(f"<p style='text-align: right; font-size: 12px; color: #58cc02; font-weight: bold;'>Level {current_lvl} 进度: {len(mastered_list)}/100</p>", unsafe_allow_html=True)

            if current_queue:
                current = current_queue[0]

                if st.button(f"🔊 点此朗读单词", use_container_width=True, type="primary"):
                    st.audio(get_audio_bytes(current["word"]), format="audio/mp3", autoplay=True)

                st.markdown(
                    f"""
                        <div class="quiz-card">
                            <div style="font-size: 38px; font-weight: bold; color: #303133; margin-bottom: 4px;">{current['word']}</div>
                            <div style="font-size: 15px; color: #afafaf; margin-bottom: 10px;">{current['phonetic']}</div>
                            <div style="font-size: 18px; font-weight: bold; color: #1cb0f6; margin-bottom: 12px;">{current['meaning']}</div>
                            <hr style="border: none; border-top: 2px solid #f2f2f2; margin: 15px 0;">
                            <div style="font-size: 14px; color: #4b4b4b; text-align: left; background-color: #f7f7f7; padding: 12px; border-radius: 12px;">
                                📖 <b>例句：</b>{current['example_en']}<br><br>
                                💡 <b>翻译：</b>{current['example_cn']}
                            </div>
                        </div>
                        """,
                    unsafe_allow_html=True,
                )

                if st.button("🔊 朗读整句例句", use_container_width=True):
                    st.audio(get_audio_bytes(current["example_en"]), format="audio/mp3", autoplay=True)

                # --- 操作按钮区域 ---
                st.write("")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("❌ 模糊 (重练)", use_container_width=True):
                        current_queue.append(current_queue.pop(0))
                        st.rerun()
                with col2:
                    if st.button("✔ 认识 (下一个)", use_container_width=True, type="primary"):
                        done_word = current_queue.pop(0)
                        if done_word not in mastered_list:
                            mastered_list.append(done_word)
                        sync_progress_to_cloud(st.session_state.user.id, st.session_state.level, st.session_state.mastered)
                        st.rerun()
                
                st.markdown("<hr style='margin: 15px 0; border: none; border-top: 2px dashed #f2f2f2;'>", unsafe_allow_html=True)
                
                if st.button("🗑️ 太简单，斩掉它！", use_container_width=True):
                    done_word = current_queue.pop(0)
                    if done_word not in mastered_list:
                        mastered_list.append(done_word)
                    sync_progress_to_cloud(st.session_state.user.id, st.session_state.level, st.session_state.mastered)
                    st.rerun()

            else:
                if current_lvl < 20:
                    st.balloons()
                    st.success(f"🎉 太棒了！Level {current_lvl} 完美通关！")
                    if st.button(f"🚀 冲刺进入 Level {current_lvl + 1}", use_container_width=True, type="primary"):
                        st.session_state.level += 1
                        sync_progress_to_cloud(st.session_state.user.id, st.session_state.level, st.session_state.mastered)
                        st.rerun()
                else:
                    st.success("🏆 恭喜你通关全部 20 个 Level！英语词汇终极大师！")
                    if st.button("🔄 重新开始挑战", use_container_width=True):
                        st.session_state.level = 1
                        st.rerun()

        # ==========================================
        # 🎯 红心生存测验模式 (Duolingo Style)
        # ==========================================
        elif st.session_state.page == "quiz":
            if not all_learned_pool:
                st.info("当前关卡还没有学过任何单词，快去学习吧！")
            else:
                # 顶部展示生命值红心
                st.markdown(f"<div style='text-align: right; font-size: 24px; margin-bottom: 10px;'>{'❤️'*st.session_state.hearts}{'🤍'*(5-st.session_state.hearts)}</div>", unsafe_allow_html=True)

                if st.session_state.hearts <= 0:
                    st.error("💔 你的红心耗尽了！测验被迫中断。")
                    if st.button("🔄 满血复活 (恢复 5 颗红心)", use_container_width=True, type="primary"):
                        st.session_state.hearts = 5
                        st.rerun()
                else:
                    if "quiz_current" not in st.session_state:
                        q_item = random.choice(all_learned_pool)
                        st.session_state.quiz_current = q_item
                        all_flat_words = [item for lvl_items in GLOBAL_VOCAB_DB.values() for item in lvl_items]
                        wrong_meanings = [v["meaning"] for v in all_flat_words if v["meaning"] != q_item["meaning"]]
                        distractors = random.sample(wrong_meanings, min(3, len(wrong_meanings)))
                        options = distractors + [q_item["meaning"]]
                        random.shuffle(options)
                        st.session_state.quiz_options = options
                        st.session_state.quiz_answered = False
                        st.session_state.selected_option = None

                    qc = st.session_state.quiz_current
                    opts = st.session_state.quiz_options

                    # 答题后展现结果
                    if st.session_state.get("quiz_answered", False):
                        selected = st.session_state.selected_option
                        st.audio(get_audio_bytes(qc["word"]), format="audio/mp3", autoplay=True)

                        if selected == qc["meaning"]:
                            status_msg = "✅ 完美！回答正确"
                            status_color = "#58cc02" # 多邻国绿
                        else:
                            status_msg = "❌ 哎呀，答错了"
                            status_color = "#ff4b4b" # 多邻国红

                        st.markdown(
                            f"""
                            <div class="quiz-card" style="border-color: {status_color};">
                                <div style="font-size: 36px; font-weight: bold; color: {status_color}; margin-bottom: 4px;">{qc['word']}</div>
                                <div style="font-size: 16px; font-weight: bold; color: {status_color}; margin-bottom: 10px;">{status_msg}</div>
                                <hr style="border: none; border-top: 2px dashed #f2f2f2; margin: 10px 0;">
                                <div style="font-size: 14px; color: #afafaf; margin-bottom: 10px;">{qc['phonetic']}</div>
                                <div style="font-size: 18px; font-weight: 600; color: #1cb0f6; margin-bottom: 12px;">{qc['meaning']}</div>
                                <div style="font-size: 13px; color: #4b4b4b; font-style: italic; text-align: left; background-color: #f7f7f7; padding: 12px; border-radius: 12px;">
                                    📖 <b>例句：</b>{qc['example_en']}<br><br>💡 <b>翻译：</b>{qc['example_cn']}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        if st.button("➡️ 继续下一题", use_container_width=True, type="primary"):
                            q_item = random.choice(all_learned_pool)
                            st.session_state.quiz_current = q_item
                            all_flat_words = [item for lvl_items in GLOBAL_VOCAB_DB.values() for item in lvl_items]
                            wrong_meanings = [v["meaning"] for v in all_flat_words if v["meaning"] != q_item["meaning"]]
                            distractors = random.sample(wrong_meanings, min(3, len(wrong_meanings)))
                            options = distractors + [q_item["meaning"]]
                            random.shuffle(options)
                            st.session_state.quiz_options = options
                            st.session_state.quiz_answered = False
                            st.session_state.selected_option = None
                            st.rerun()

                    # 未答题状态
                    else:
                        if st.button(f"🔊 点击听音", use_container_width=True):
                            st.audio(get_audio_bytes(qc["word"]), format="audio/mp3", autoplay=True)

                        st.markdown(
                            f"""
                            <div class="quiz-card">
                                <div style="font-size: 38px; font-weight: bold; color: #303133;">{qc['word']}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        col_a, col_b = st.columns(2)
                        labels = ["A", "B", "C", "D"]

                        for idx, opt in enumerate(opts):
                            current_col = col_a if idx % 2 == 0 else col_b
                            with current_col:
                                # 把词性括到最后面 (n.)
                                parts = opt.split(" ", 1)
                                if len(parts) == 2:
                                    btn_label = f"{labels[idx]}. {parts[1]} ({parts[0]})"
                                else:
                                    btn_label = f"{labels[idx]}. {opt}"
                                    
                                if st.button(btn_label, use_container_width=True, key=f"opt_{idx}"):
                                    st.session_state.quiz_answered = True
                                    st.session_state.selected_option = opt
                                    # 答错扣掉一颗红心
                                    if opt != qc["meaning"]:
                                        st.session_state.hearts -= 1
                                    st.rerun()

        # ==========================================
        # 🔁 单词重温模式
        # ==========================================
        elif st.session_state.page == "review":
            if not mastered_list:
                st.info("当前关卡还没有掌握任何单词哦！")
            else:
                if "review_current" not in st.session_state:
                    st.session_state.review_current = random.choice(mastered_list)

                rc = st.session_state.review_current
                
                if st.button(f"🔊 点此朗读单词", use_container_width=True, type="primary"):
                    st.audio(get_audio_bytes(rc["word"]), format="audio/mp3", autoplay=True)

                st.markdown(
                    f"""
                        <div class="quiz-card">
                            <div style="font-size: 38px; font-weight: bold; color: #303133; margin-bottom: 4px;">{rc['word']}</div>
                            <div style="font-size: 14px; color: #afafaf; margin-bottom: 10px;">{rc['phonetic']}</div>
                            <div style="font-size: 18px; font-weight: 600; color: #1cb0f6; margin-bottom: 12px;">{rc['meaning']}</div>
                            <hr style="border: none; border-top: 2px solid #f2f2f2; margin: 15px 0;">
                            <div style="font-size: 13px; color: #4b4b4b; text-align: left; background-color: #f7f7f7; padding: 12px; border-radius: 12px;">
                                📖 <b>例句：</b>{rc['example_en']}<br><br>💡 <b>翻译：</b>{rc['example_cn']}
                            </div>
                        </div>
                        """,
                    unsafe_allow_html=True,
                )

                if st.button("🔊 朗读整句例句", use_container_width=True):
                    st.audio(get_audio_bytes(rc["example_en"]), format="audio/mp3", autoplay=True)

                st.write("")
                if st.button("➡️ 换一个复习", use_container_width=True, type="primary"):
                    st.session_state.review_current = random.choice(mastered_list)
                    st.rerun()
