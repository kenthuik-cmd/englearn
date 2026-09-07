import random
from io import BytesIO
from gtts import gTTS
import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client
from vocab_data import GLOBAL_VOCAB_DB

# 读取 Supabase 配置
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_ANON_KEY"]
supabase = create_client(url, key)

st.set_page_config(
    page_title="AI 英语进阶闯关", page_icon="📖", layout="centered"
)

# 注入手机端极简样式（隐藏原生音频播放器）
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* 彻底隐藏所有的原生音频播放器 UI */
        [data-testid="stAudio"] {
            display: none !important;
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
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        
        .quiz-card {
            background-color: #ffffff;
            border: 1px solid #e4e7ed;
            padding: 20px 18px;
            border-radius: 18px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.08);
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

# ====== 新增核心：原生免刷新掉线机制 (URL 记住设备) ======
# 当检测到内存被刷新清空，但网址栏带有 uid 凭证时，自动静默登录
if not st.session_state.user and "uid" in st.query_params:
    saved_uid = st.query_params["uid"]
    
    # 构建一个符合逻辑的模拟用户对象
    class AutoLoginUser:
        def __init__(self, uid):
            self.id = uid
            
    st.session_state.user = AutoLoginUser(saved_uid)
    
    # 顺便从云端同步该用户的关卡等级
    try:
        profile = supabase.table("user_profiles").select("*").eq("user_id", saved_uid).execute()
        if profile.data:
            st.session_state.level = profile.data[0].get("grade", 1)
    except Exception:
        pass
# ==========================================================

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
        "<h3 style='text-align: center; color: #303133; margin-top:"
        " 10px;'>📖 英语逐级背单词 App</h3>",
        unsafe_allow_html=True,
    )

    with st.container():
        email = st.text_input("邮箱地址", placeholder="请输入注册邮箱")
        password = st.text_input(
            "密码", type="password", placeholder="请输入密码"
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("登 录", use_container_width=True, type="primary"):
                try:
                    res = supabase.auth.sign_in_with_password(
                        {"email": email, "password": password}
                    )
                    st.session_state.user = res.user
                    
                    # --- 新增：登录成功后，把凭证写入 URL 网址，这样刷新就不会掉线了 ---
                    st.query_params["uid"] = res.user.id
                    
                    profile = (
                        supabase.table("user_profiles")
                        .select("*")
                        .eq("user_id", res.user.id)
                        .execute()
                    )
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
    # HOME 主页
    if st.session_state.page == "home":
        st.markdown(
            "<h3 style='text-align: center; color: #303133; margin-bottom:"
            " 5px;'>🌟 英语难度闯关</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<p style='text-align: center; color: #409EFF; font-size: 14px;'"
            f" margin-bottom: 15px;'>当前正在挑战：<b>Level {current_lvl} / 20</b></p>",
            unsafe_allow_html=True,
        )

        if st.button("📚 开启当前关卡背诵与跟读", use_container_width=True, type="primary"):
            st.session_state.page = "study"
            st.rerun()

        st.write("")
        if st.button("🎯 进入当前关卡小测验", use_container_width=True):
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
            # --- 新增：退出登录时，从 URL 擦除凭证印记 ---
            if "uid" in st.query_params:
                del st.query_params["uid"]
            st.rerun()

    # 子页面
    else:
        if st.button("⬅️ 返回主页", type="secondary"):
            st.session_state.page = "home"
            st.rerun()

        # 背单词模式
        if st.session_state.page == "study":
            st.markdown(f"### 📖 Level {current_lvl} 核心词汇闯关")

            if current_queue:
                current = current_queue[0]

                if st.button(
                    f"🔊 点此朗读：{current['word']}",
                    use_container_width=True,
                    type="primary",
                ):
                    st.audio(
                        get_audio_bytes(current["word"]), format="audio/mp3", autoplay=True
                    )

                st.markdown(
                    f"""
                        <div class="quiz-card">
                            <div style="font-size: 36px; font-weight: bold; color: #303133; margin-bottom: 4px;">{current['word']}</div>
                            <div style="font-size: 14px; color: #909399; margin-bottom: 10px;">{current['phonetic']}</div>
                            <div style="font-size: 18px; font-weight: 600; color: #409EFF; margin-bottom: 12px;">{current['meaning']}</div>
                            <hr style="border: none; border-top: 1px solid #ebeef5; margin: 10px 0;">
                            <div style="font-size: 13px; color: #606266; font-style: italic; text-align: left;">
                                📝 <b>例句：</b>{current['example_en']}<br>🏷️ <b>翻译：</b>{current['example_cn']}
                            </div>
                        </div>
                        """,
                    unsafe_allow_html=True,
                )

                if st.button("🔊 朗读例句", use_container_width=True):
                    st.audio(
                        get_audio_bytes(current["example_en"]),
                        format="audio/mp3",
                        autoplay=True,
                    )

                target_word_lower = current["word"].lower()
                speech_component_html = (
                    """
                        <div style="font-family: sans-serif; text-align: center; margin-top: 2px;">
                            <button id="recordBtn" style="background-color: #ff4b4b; color: white; border: none; padding: 10px 16px; font-size: 14px; border-radius: 12px; cursor: pointer; width: 100%;">🎙️ 点击进行 AI 语音跟读</button>
                            <p id="statusText" style="margin-top: 4px; color: #555; font-size: 12px;"></p>
                        </div>
                        <script>
                            const targetWord = '"""
                    + target_word_lower
                    + """';
                            const btn = document.getElementById('recordBtn');
                            const statusText = document.getElementById('statusText');

                            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                            if (!SpeechRecognition) {
                                statusText.innerHTML = "❌ 浏览器不支持语音识别";
                                btn.disabled = true;
                            } else {
                                const recognition = new SpeechRecognition();
                                recognition.lang = 'en-US';
                                recognition.interimResults = false;
                                recognition.maxAlternatives = 1;

                                btn.onclick = function() {
                                    statusText.innerHTML = "👂 正在听你发音...";
                                    btn.style.backgroundColor = "#ffa500";
                                    recognition.start();
                                };

                                recognition.onresult = function(event) {
                                    const speechResult = event.results[0][0].transcript.trim().toLowerCase();
                                    const cleanResult = speechResult.replace(/[.,\/#!$%%^&*;:{}=\\-_`~()]/g,"");
                                    
                                    if (cleanResult.includes(targetWord)) {
                                        statusText.innerHTML = "✅ 识别成功: " + speechResult + " 🎉";
                                        btn.style.backgroundColor = "#67C23A";
                                    } else {
                                        statusText.innerHTML = "❌ 识别为: " + speechResult + "，再试一次";
                                        btn.style.backgroundColor = "#F56C6C";
                                    }
                                };

                                recognition.onerror = function(event) {
                                    statusText.innerHTML = "⚠️ 出错: " + event.error;
                                    btn.style.backgroundColor = "#ff4b4b";
                                };

                                recognition.onspeechend = function() {
                                    recognition.stop();
                                    btn.innerHTML = "🎙️ 再次跟读";
                                };
                            }
                        </script>
                        """
                )
                components.html(speech_component_html, height=75)

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
                
                st.markdown(
                    "<hr style='margin: 15px 0 10px 0; border: none; border-top: 1px dashed #dcdfe6;'>", 
                    unsafe_allow_html=True
                )
                
                if st.button("🗑️ 太简单，不再出现", use_container_width=True):
                    done_word = current_queue.pop(0)
                    if done_word not in mastered_list:
                        mastered_list.append(done_word)
                    sync_progress_to_cloud(st.session_state.user.id, st.session_state.level, st.session_state.mastered)
                    st.rerun()

            else:
                if current_lvl < 20:
                    st.success(f"🎉 Level {current_lvl} 完美通关！")
                    if st.button(
                        f"🚀 自动解锁并进入 Level {current_lvl + 1}",
                        use_container_width=True,
                        type="primary",
                    ):
                        st.session_state.level += 1
                        sync_progress_to_cloud(
                            st.session_state.user.id,
                            st.session_state.level,
                            st.session_state.mastered,
                        )
                        st.rerun()
                else:
                    st.success("🏆 恭喜你通关全部 20 个 Level！")
                    if st.button("🔄 重新开始挑战", use_container_width=True):
                        st.session_state.level = 1
                        st.rerun()

        # 小测验面板
        elif st.session_state.page == "quiz":
            if not all_learned_pool:
                st.info("当前关卡还没有学过任何单词！")
            else:
                if "quiz_current" not in st.session_state:
                    q_item = random.choice(all_learned_pool)
                    st.session_state.quiz_current = q_item
                    all_flat_words = [
                        item
                        for lvl_items in GLOBAL_VOCAB_DB.values()
                        for item in lvl_items
                    ]
                    wrong_meanings = [
                        v["meaning"]
                        for v in all_flat_words
                        if v["meaning"] != q_item["meaning"]
                    ]
                    distractors = random.sample(
                        wrong_meanings, min(3, len(wrong_meanings))
                    )
                    options = distractors + [q_item["meaning"]]
                    random.shuffle(options)
                    st.session_state.quiz_options = options
                    st.session_state.quiz_answered = False
                    st.session_state.selected_option = None

                qc = st.session_state.quiz_current
                opts = st.session_state.quiz_options

                # 已经答题的状态
                if st.session_state.get("quiz_answered", False):
                    selected = st.session_state.selected_option
                    audio_bytes = get_audio_bytes(qc["word"])
                    st.audio(audio_bytes, format="audio/mp3", autoplay=True)

                    if selected == qc["meaning"]:
                        status_msg = "✅ 回答正确！"
                        status_color = "#67C23A"
                    else:
                        status_msg = "❌ 抱歉，答错了"
                        status_color = "#F56C6C"

                    st.markdown(
                        f"""
                        <div class="quiz-card">
                            <div style="font-size: 36px; font-weight: bold; color: {status_color}; margin-bottom: 4px;">{qc['word']}</div>
                            <div style="font-size: 16px; font-weight: bold; color: {status_color}; margin-bottom: 10px;">{status_msg}</div>
                            <hr style="border: none; border-top: 1px dashed #ebeef5; margin: 10px 0;">
                            <div style="font-size: 14px; color: #909399; margin-bottom: 10px;">{qc['phonetic']}</div>
                            <div style="font-size: 18px; font-weight: 600; color: #409EFF; margin-bottom: 12px;">{qc['meaning']}</div>
                            <div style="font-size: 13px; color: #606266; font-style: italic; text-align: left; background-color: #f8f9fa; padding: 10px; border-radius: 8px;">
                                📝 <b>例句：</b>{qc['example_en']}<br><br>🏷️ <b>翻译：</b>{qc['example_cn']}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    if st.button("➡️ 下一题", use_container_width=True, type="primary"):
                        q_item = random.choice(all_learned_pool)
                        st.session_state.quiz_current = q_item
                        all_flat_words = [
                            item
                            for lvl_items in GLOBAL_VOCAB_DB.values()
                            for item in lvl_items
                        ]
                        wrong_meanings = [
                            v["meaning"]
                            for v in all_flat_words
                            if v["meaning"] != q_item["meaning"]
                        ]
                        distractors = random.sample(
                            wrong_meanings, min(3, len(wrong_meanings))
                        )
                        options = distractors + [q_item["meaning"]]
                        random.shuffle(options)
                        st.session_state.quiz_options = options
                        st.session_state.quiz_answered = False
                        st.session_state.selected_option = None
                        st.rerun()

                # 未答题状态
                else:
                    if st.button(f"🔊 朗读测验词", use_container_width=True, type="primary"):
                        st.audio(get_audio_bytes(qc["word"]), format="audio/mp3", autoplay=True)

                    st.markdown(
                        f"""
                        <div class="quiz-card">
                            <div style="font-size: 36px; font-weight: bold; color: #303133;">{qc['word']}</div>
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
                                st.rerun()

        # 重温模式
        elif st.session_state.page == "review":
            if not mastered_list:
                st.info("当前关卡还没有掌握任何单词哦！")
            else:
                if "review_current" not in st.session_state:
                    st.session_state.review_current = random.choice(mastered_list)

                rc = st.session_state.review_current
                with st.container():
                    if st.button(
                        f"🔊 点此朗读：{rc['word']}", use_container_width=True, type="primary"
                    ):
                        st.audio(get_audio_bytes(rc["word"]), format="audio/mp3", autoplay=True)

                    st.markdown(
                        f"""
                            <div class="quiz-card">
                                <div style="font-size: 36px; font-weight: bold; color: #303133; margin-bottom: 4px;">{rc['word']}</div>
                                <div style="font-size: 14px; color: #909399; margin-bottom: 10px;">{rc['phonetic']}</div>
                                <div style="font-size: 18px; font-weight: 600; color: #67C23A; margin-bottom: 12px;">{rc['meaning']}</div>
                                <hr style="border: none; border-top: 1px solid #ebeef5; margin: 10px 0;">
                                <div style="font-size: 13px; color: #606266; font-style: italic; text-align: left;">
                                    📝 <b>例句：</b>{rc['example_en']}<br>🏷️ <b>翻译：</b>{rc['example_cn']}
                                </div>
                            </div>
                            """,
                        unsafe_allow_html=True,
                    )

                if st.button("➡️ 换一个复习", use_container_width=True, type="primary"):
                    st.session_state.review_current = random.choice(mastered_list)
                    st.rerun()
