import random
import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client
from vocab_data import GLOBAL_VOCAB_DB

# 读取 Supabase 配置
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_ANON_KEY"]
supabase = create_client(url, key)

st.set_page_config(
    page_title="AI 英语进阶闯关", page_icon="🦉", layout="centered"
)

# 注入手机端极简样式
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
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
            box-shadow: 0 4px 0px rgba(0, 0, 0, 0.1); 
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

# === 核心武器 1：原生前端单词朗读按钮 (完美突破手机静音限制) ===
def render_word_audio_button(word, button_text="🔊 点此朗读单词"):
    html_code = f"""
    <style>
        body {{ margin: 0; padding: 0; font-family: sans-serif; }}
        button {{
            width: 100%; 
            background-color: #ff4b4b; 
            color: white; 
            border: none; 
            padding: 12px; 
            font-size: 15px; 
            font-weight: bold; 
            border-radius: 12px; 
            cursor: pointer; 
            box-shadow: 0 4px 0px rgba(255, 75, 75, 0.3); 
            transition: transform 0.1s, box-shadow 0.1s;
        }}
        button:active {{
            transform: translateY(4px);
            box-shadow: 0 0px 0px rgba(0,0,0,0.1);
        }}
    </style>
    <button onclick="window.speechSynthesis.cancel(); let u = new SpeechSynthesisUtterance('{word}'); u.lang='en-US'; window.speechSynthesis.speak(u);">
        {button_text}
    </button>
    """
    components.html(html_code, height=55)

# === 核心武器 2：动态高亮例句组件 ===
def render_highlight_example(example_en, example_cn):
    escaped_en = example_en.replace("'", "\\'")
    html_code = f"""
    <style>
        body {{ margin: 0; padding: 0; font-family: sans-serif; }}
        .example-card {{
            background-color: #f7f7f7; 
            padding: 18px; 
            border-radius: 18px; 
            box-sizing: border-box; 
            width: 100%;
            border: 2px solid #e5e5e5;
        }}
        .highlight {{
            color: #1cb0f6;
            font-weight: 900;
            font-size: 115%;
            background-color: rgba(28, 176, 246, 0.15);
            border-radius: 6px;
            padding: 0 4px;
            transition: all 0.1s;
        }}
        .word {{ display: inline-block; margin: 0 2px; transition: all 0.1s; color: #4b4b4b; }}
        button:active {{ transform: translateY(4px); box-shadow: 0 0px 0px rgba(0,0,0,0.1) !important; }}
    </style>
    <div class="example-card">
        <div style="font-size: 15px; margin-bottom: 12px; line-height: 1.6;">
            📖 <b>例句：</b><span id="sentence-box"></span>
        </div>
        <div style="font-size: 14px; color: #777; margin-bottom: 16px; line-height: 1.5;">
            💡 <b>翻译：</b>{example_cn}
        </div>
        <button id="playBtn" style="width: 100%; background-color: #1cb0f6; color: white; border: none; padding: 12px; font-size: 15px; font-weight: bold; border-radius: 12px; cursor: pointer; box-shadow: 0 4px 0px rgba(28, 176, 246, 0.3); transition: all 0.1s;">
            🔊 动态朗读例句
        </button>
    </div>
    <script>
        const sentenceStr = "{escaped_en}";
        const container = document.getElementById("sentence-box");
        container.innerHTML = sentenceStr.replace(/([a-zA-Z0-9']+)/g, '<span class="word">$1</span>');
        
        const wordSpans = container.querySelectorAll('.word');
        const playBtn = document.getElementById("playBtn");
        
        playBtn.onclick = () => {{
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(sentenceStr);
            utterance.lang = 'en-US';
            utterance.rate = 0.85;
            
            let currentWordIndex = 0;
            utterance.onboundary = (event) => {{
                if (event.name === 'word') {{
                    wordSpans.forEach(span => span.classList.remove('highlight'));
                    if (currentWordIndex < wordSpans.length) {{
                        wordSpans[currentWordIndex].classList.add('highlight');
                        currentWordIndex++;
                    }}
                }}
            }};
            utterance.onend = () => {{
                wordSpans.forEach(span => span.classList.remove('highlight'));
            }};
            window.speechSynthesis.speak(utterance);
        }};
    </script>
    """
    components.html(html_code, height=205)

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

if "hearts" not in st.session_state:
    st.session_state.hearts = 5


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
            progress_pct = min(len(mastered_list) / 100.0, 1.0)
            st.progress(progress_pct)
            st.markdown(f"<p style='text-align: right; font-size: 12px; color: #58cc02; font-weight: bold;'>Level {current_lvl} 进度: {len(mastered_list)}/100</p>", unsafe_allow_html=True)

            if current_queue:
                current = current_queue[0]

                # 替换为全新的手机端无敌发音按钮
                render_word_audio_button(current["word"], "🔊 点此朗读单词")

                st.markdown(
                    f"""
                        <div class="quiz-card" style="margin-bottom: 12px;">
                            <div style="font-size: 38px; font-weight: bold; color: #303133; margin-bottom: 4px;">{current['word']}</div>
                            <div style="font-size: 15px; color: #afafaf; margin-bottom: 10px;">{current['phonetic']}</div>
                            <div style="font-size: 18px; font-weight: bold; color: #1cb0f6;">{current['meaning']}</div>
                        </div>
                        """,
                    unsafe_allow_html=True,
                )
                
                render_highlight_example(current["example_en"], current["example_cn"])

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
                
                st.markdown("<hr style='margin: 15px 0 10px 0; border: none; border-top: 2px dashed #f2f2f2;'>", unsafe_allow_html=True)
                
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
        # 🎯 红心生存测验模式
        # ==========================================
        elif st.session_state.page == "quiz":
            if not all_learned_pool:
                st.info("当前关卡还没有学过任何单词，快去学习吧！")
            else:
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
                        
                        # 在结果面板顶部放置发音按钮
                        render_word_audio_button(qc["word"], "🔊 再次朗读单词")

                        if selected == qc["meaning"]:
                            status_msg = "✅ 完美！回答正确"
                            status_color = "#58cc02" 
                        else:
                            status_msg = "❌ 哎呀，答错了"
                            status_color = "#ff4b4b" 

                        st.markdown(
                            f"""
                            <div class="quiz-card" style="border-color: {status_color}; margin-bottom: 12px; margin-top: 10px;">
                                <div style="font-size: 36px; font-weight: bold; color: {status_color}; margin-bottom: 4px;">{qc['word']}</div>
                                <div style="font-size: 16px; font-weight: bold; color: {status_color}; margin-bottom: 10px;">{status_msg}</div>
                                <hr style="border: none; border-top: 2px dashed #f2f2f2; margin: 10px 0;">
                                <div style="font-size: 14px; color: #afafaf; margin-bottom: 10px;">{qc['phonetic']}</div>
                                <div style="font-size: 18px; font-weight: 600; color: #1cb0f6;">{qc['meaning']}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        
                        render_highlight_example(qc["example_en"], qc["example_cn"])

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
                        render_word_audio_button(qc["word"], "🔊 点击听音")

                        st.markdown(
                            f"""
                            <div class="quiz-card" style="margin-top: 10px;">
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
                                parts = opt.split(" ", 1)
                                if len(parts) == 2:
                                    btn_label = f"{labels[idx]}. {parts[1]} ({parts[0]})"
                                else:
                                    btn_label = f"{labels[idx]}. {opt}"
                                    
                                if st.button(btn_label, use_container_width=True, key=f"opt_{idx}"):
                                    st.session_state.quiz_answered = True
                                    st.session_state.selected_option = opt
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
                
                render_word_audio_button(rc["word"], "🔊 点此朗读单词")

                st.markdown(
                    f"""
                        <div class="quiz-card" style="margin-bottom: 12px; margin-top: 10px;">
                            <div style="font-size: 38px; font-weight: bold; color: #303133; margin-bottom: 4px;">{rc['word']}</div>
                            <div style="font-size: 14px; color: #afafaf; margin-bottom: 10px;">{rc['phonetic']}</div>
                            <div style="font-size: 18px; font-weight: 600; color: #1cb0f6;">{rc['meaning']}</div>
                        </div>
                        """,
                    unsafe_allow_html=True,
                )
                
                render_highlight_example(rc["example_en"], rc["example_cn"])

                st.write("")
                if st.button("➡️ 换一个复习", use_container_width=True, type="primary"):
                    st.session_state.review_current = random.choice(mastered_list)
                    st.rerun()
