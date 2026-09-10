import random
import re
import time
from io import BytesIO
from datetime import date
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
    page_title="AI 英语进阶闯关", page_icon="🔥", layout="centered"
)

# 注入手机端极简样式
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        [data-testid="stAudio"] {
            display: none !important;
        }
        
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
        
        .status-bar {
            display: flex; 
            justify-content: space-between; 
            font-size: 16px; 
            font-weight: bold; 
            margin-bottom: 15px; 
            padding: 12px 18px; 
            background: #ffffff; 
            border-radius: 16px; 
            border: 2px solid #e5e5e5;
        }
        
        .section-title {
            font-size: 15px; 
            color: #afafaf; 
            font-weight: bold; 
            margin-top: 20px; 
            margin-bottom: 10px; 
            text-align: center;
        }

        @keyframes fireFlicker {
            0%, 100% { transform: scale(1) rotate(-3deg); }
            50% { transform: scale(1.15) rotate(3deg); }
        }
        .anim-fire {
            display: inline-block;
            animation: fireFlicker 1.2s infinite ease-in-out;
            transform-origin: bottom center;
        }

        @keyframes heartBeat {
            0% { transform: scale(1); }
            15% { transform: scale(1.25); }
            30% { transform: scale(1); }
            45% { transform: scale(1.25); }
            70%, 100% { transform: scale(1); }
        }
        .anim-heart {
            display: inline-block;
            animation: heartBeat 1.5s infinite;
            transform-origin: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

def get_audio_bytes(text):
    tts = gTTS(text=text, lang="en")
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()

# === 原生前端单词朗读按钮 ===
def render_word_audio_button(word, button_text="🔊 点此朗读单词", autoplay=False):
    escaped_word = word.replace("'", "\\'")
    autoplay_script = f"""
    <script>
        if ({'true' if autoplay else 'false'}) {{
            setTimeout(() => {{
                window.speechSynthesis.cancel(); 
                let u = new SpeechSynthesisUtterance('{escaped_word}'); 
                u.lang='en-US'; 
                window.speechSynthesis.speak(u);
            }}, 300);
        }}
    </script>
    """
    html_code = f"""
    <style>
        body {{ margin: 0; padding: 0; font-family: sans-serif; }}
        button {{
            width: 100%; background-color: #ff4b4b; color: white; border: none; padding: 12px; font-size: 15px; font-weight: bold; border-radius: 12px; cursor: pointer; box-shadow: 0 4px 0px rgba(255, 75, 75, 0.3); transition: transform 0.1s, box-shadow 0.1s;
        }}
        button:active {{ transform: translateY(4px); box-shadow: 0 0px 0px rgba(0,0,0,0.1); }}
    </style>
    <button onclick="window.speechSynthesis.cancel(); let u = new SpeechSynthesisUtterance('{escaped_word}'); u.lang='en-US'; window.speechSynthesis.speak(u);">
        {button_text}
    </button>
    {autoplay_script}
    """
    components.html(html_code, height=55)

# === AI 语音识别跟读组件 ===
def render_ai_speech_recognition(target_word):
    target_word_lower = target_word.lower().replace("'", "\\'")
    unique_id = int(time.time() * 1000)
    html_code = f"""
    <style>
        body {{ margin: 0; padding: 0; font-family: sans-serif; text-align: center; }}
        button {{
            width: 100%; background-color: #ff9600; color: white; border: none; padding: 12px; font-size: 15px; font-weight: bold; border-radius: 12px; cursor: pointer; box-shadow: 0 4px 0px rgba(255, 150, 0, 0.3); transition: transform 0.1s, box-shadow 0.1s, background-color 0.3s;
        }}
        button:active {{ transform: translateY(4px); box-shadow: 0 0px 0px rgba(0,0,0,0.1) !important; }}
    </style>
    <button id="recordBtn_{unique_id}">🎙️ AI 评测发音</button>
    <p id="statusText_{unique_id}" style="margin-top: 8px; color: #555; font-size: 13px; font-weight: bold;"></p>
    
    <script>
        const targetWord = '{target_word_lower}';
        const btn = document.getElementById('recordBtn_{unique_id}');
        const statusText = document.getElementById('statusText_{unique_id}');

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {{
            statusText.innerHTML = "❌ 当前浏览器不支持语音识别";
            btn.disabled = true;
            btn.style.backgroundColor = "#ccc";
            btn.style.boxShadow = "none";
        }} else {{
            const recognition = new SpeechRecognition();
            recognition.lang = 'en-US';
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;

            btn.onclick = function() {{
                statusText.innerHTML = "👂 正在听你发音...";
                btn.style.backgroundColor = "#ffc107";
                recognition.start();
            }};

            recognition.onresult = function(event) {{
                const speechResult = event.results[0][0].transcript.trim().toLowerCase();
                const cleanResult = speechResult.replace(/[.,\\/#!$%\\^&\\*;:{{}}=\\-_`~()]/g,"");
                
                if (cleanResult.includes(targetWord)) {{
                    statusText.innerHTML = "✅ 发音完美: " + speechResult + " 🎉";
                    btn.style.backgroundColor = "#58cc02";
                    btn.style.boxShadow = "0 4px 0px rgba(88, 204, 2, 0.3)";
                }} else {{
                    statusText.innerHTML = "❌ 识别为: " + speechResult + "，再试一次";
                    btn.style.backgroundColor = "#ff4b4b";
                    btn.style.boxShadow = "0 4px 0px rgba(255, 75, 75, 0.3)";
                }}
            }};

            recognition.onerror = function(event) {{
                statusText.innerHTML = "⚠️ 出错: " + event.error;
                btn.style.backgroundColor = "#ff9600";
            }};

            recognition.onspeechend = function() {{
                recognition.stop();
                setTimeout(() => {{ btn.innerHTML = "🎙️ 再次跟读"; }}, 1000);
            }};
        }}
    </script>
    """
    components.html(html_code, height=85)

# === 盲听双重发音按钮 ===
def render_blind_listen_button(word, button_text="🔊 播放神秘音频 (常速+慢速)", autoplay=False):
    escaped_word = word.replace("'", "\\'")
    autoplay_script = f"""
    <script>
        if ({'true' if autoplay else 'false'}) {{
            setTimeout(playTwice, 300);
        }}
    </script>
    """
    html_code = f"""
    <style>
        body {{ margin: 0; padding: 0; font-family: sans-serif; }}
        button {{
            width: 100%; background-color: #9c27b0; color: white; border: none; padding: 12px; font-size: 15px; font-weight: bold; border-radius: 12px; cursor: pointer; box-shadow: 0 4px 0px rgba(156, 39, 176, 0.3); transition: transform 0.1s, box-shadow 0.1s;
        }}
        button:active {{ transform: translateY(4px); box-shadow: 0 0px 0px rgba(0,0,0,0.1); }}
    </style>
    <script>
        function playTwice() {{
            window.speechSynthesis.cancel();
            let u1 = new SpeechSynthesisUtterance('{escaped_word}'); u1.lang = 'en-US'; u1.rate = 1.0;
            let u2 = new SpeechSynthesisUtterance('{escaped_word}'); u2.lang = 'en-US'; u2.rate = 0.6; 
            window.speechSynthesis.speak(u1); window.speechSynthesis.speak(u2);
        }}
    </script>
    <button onclick="playTwice()">{button_text}</button>
    {autoplay_script}
    """
    components.html(html_code, height=55)

# === 动态高亮例句组件 ===
def render_highlight_example(example_en, example_cn):
    escaped_en = example_en.replace("'", "\\'")
    unique_id = int(time.time() * 1000) + random.randint(0, 1000)
    html_code = f"""
    <style>
        body {{ margin: 0; padding: 0; font-family: sans-serif; }}
        .example-card {{
            background-color: #f7f7f7; padding: 18px; border-radius: 18px; box-sizing: border-box; width: 100%; border: 2px solid #e5e5e5; margin-bottom: 10px;
        }}
        .highlight {{
            color: #1cb0f6; font-weight: 900; font-size: 115%; background-color: rgba(28, 176, 246, 0.15); border-radius: 6px; padding: 0 4px; transition: all 0.1s;
        }}
        .word {{ display: inline-block; margin: 0 2px; transition: all 0.1s; color: #4b4b4b; }}
        button:active {{ transform: translateY(4px); box-shadow: 0 0px 0px rgba(0,0,0,0.1) !important; }}
    </style>
    <div class="example-card">
        <div style="font-size: 15px; margin-bottom: 12px; line-height: 1.6;">
            📖 <b>例句：</b><span id="sentence-box_{unique_id}"></span>
        </div>
        <div style="font-size: 14px; color: #777; margin-bottom: 16px; line-height: 1.5;">
            💡 <b>翻译：</b>{example_cn}
        </div>
        <button id="playBtn_{unique_id}" style="width: 100%; background-color: #1cb0f6; color: white; border: none; padding: 12px; font-size: 15px; font-weight: bold; border-radius: 12px; cursor: pointer; box-shadow: 0 4px 0px rgba(28, 176, 246, 0.3); transition: all 0.1s;">
            🔊 动态朗读例句
        </button>
    </div>
    <script>
        const sentenceStr = "{escaped_en}";
        const container = document.getElementById("sentence-box_{unique_id}");
        container.innerHTML = sentenceStr.replace(/([a-zA-Z0-9']+)/g, '<span class="word">$1</span>');
        
        const wordSpans = container.querySelectorAll('.word');
        const playBtn = document.getElementById("playBtn_{unique_id}");
        
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
            utterance.onend = () => {{ wordSpans.forEach(span => span.classList.remove('highlight')); }};
            window.speechSynthesis.speak(utterance);
        }};
    </script>
    """
    components.html(html_code, height=195)


# === 基础用户类：用于彻底替换系统账户 ===
class AutoLoginUser:
    def __init__(self, uid):
        self.id = uid

# === 从云端彻底恢复进度 ===
def restore_progress_from_db(profile_data):
    if profile_data:
        latest_profile = profile_data[-1]
        db_lvl = latest_profile.get("grade", 1)
        st.session_state.level = db_lvl
        
        saved_str = str(latest_profile.get("mastered_words", ""))
        if saved_str and not saved_str.isdigit():
            saved_words = saved_str.split(",")
            full_level_words = GLOBAL_VOCAB_DB.get(db_lvl, [])
            st.session_state.mastered[db_lvl] = [w for w in full_level_words if w["word"] in saved_words]
            remaining = [w for w in full_level_words if w["word"] not in saved_words]
            random.shuffle(remaining)
            st.session_state.queues[db_lvl] = remaining

# === 云端无缝保存逻辑 ===
def sync_progress_to_cloud(user_id, level, mastered_dict):
    try:
        mastered_words_list = [w['word'] for w in mastered_dict.get(level, [])]
        mastered_str = ",".join(mastered_words_list)
        
        res = supabase.table("user_profiles").select("id").eq("user_id", user_id).execute()
        if len(res.data) > 0:
            supabase.table("user_profiles").update({
                "grade": level,
                "mastered_words": mastered_str,
            }).eq("user_id", user_id).execute()
        else:
            supabase.table("user_profiles").insert({
                "user_id": user_id,
                "grade": level,
                "mastered_words": mastered_str,
            }).execute()
    except Exception as e:
        pass


# === 初始化 Session State ===
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

if "quiz_mode" not in st.session_state:
    st.session_state.quiz_mode = "normal"
if "quiz_type" not in st.session_state:
    st.session_state.quiz_type = "normal"
if "quiz_options" not in st.session_state:
    st.session_state.quiz_options = []
if "correct_ans" not in st.session_state:
    st.session_state.correct_ans = ""

if "hearts" not in st.session_state:
    st.session_state.hearts = int(st.query_params.get("hearts", 5))
if "streak" not in st.session_state:
    st.session_state.streak = int(st.query_params.get("streak", 1))

# === 免密自动登录触发机制 ===
if "user" not in st.session_state:
    st.session_state.user = None

if not st.session_state.user and "uid" in st.query_params:
    saved_uid = st.query_params["uid"]
    st.session_state.user = AutoLoginUser(saved_uid)
    try:
        profile = supabase.table("user_profiles").select("*").eq("user_id", saved_uid).execute()
        restore_progress_from_db(profile.data)
    except Exception:
        pass


current_lvl = st.session_state.level
current_queue = st.session_state.queues[current_lvl]
mastered_list = st.session_state.mastered[current_lvl]
all_learned_pool = mastered_list 

# ==========================================
# 🛑 未登录拦截 (修改为纯净无密代号模式)
# ==========================================
if not st.session_state.user:
    st.markdown(
        "<h3 style='text-align: center; color: #58cc02; margin-top: 10px;'>🦉 英语闯关打卡 App</h3>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; color: #909399; font-size: 14px;'>抛弃繁琐密码，输入代号一键读取存档！</p>",
        unsafe_allow_html=True,
    )
    
    with st.container():
        st.write("")
        username = st.text_input("🔑 你的专属存档代号 (如: Alex888)", placeholder="输入代号即可自动创建或读取进度")
        
        st.write("")
        if st.button("🚀 一键开启学习", use_container_width=True, type="primary"):
            user_id = username.strip()
            if user_id == "":
                st.warning("请先输入一个代号哦！")
            else:
                st.session_state.user = AutoLoginUser(user_id)
                st.query_params["uid"] = user_id
                
                try:
                    # 尝试从云端拉取这个代号的进度
                    profile = supabase.table("user_profiles").select("*").eq("user_id", user_id).execute()
                    if len(profile.data) > 0:
                        restore_progress_from_db(profile.data)
                        st.success(f"🎉 欢迎回来，{user_id}！已为你恢复学习进度。")
                    else:
                        # 没找到则自动创建新号
                        supabase.table("user_profiles").insert({
                            "user_id": user_id,
                            "grade": 1,
                            "mastered_words": ""
                        }).execute()
                        st.success(f"✨ 新专属存档 '{user_id}' 创建成功！")
                except Exception as e:
                    pass
                
                time.sleep(0.8)
                st.rerun()

# ==========================================
# 🟢 已登录界面
# ==========================================
else:
    if st.session_state.page != "home":
        st.markdown(f"""
        <div class='status-bar'>
            <span style='color: #ff9600;'><span class='anim-fire'>🔥</span> 连胜: {st.session_state.streak} 天</span>
            <span style='color: #ff4b4b; letter-spacing: 2px;'><span class='anim-heart'>{'❤️'*st.session_state.hearts}</span>{'🤍'*(5-st.session_state.hearts)}</span>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- HOME 主页 ----------------
    if st.session_state.page == "home":
        st.markdown("<h3 style='text-align: center; color: #303133; margin-bottom: 5px;'>🦉 每日英语打卡</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #afafaf; font-size: 14px; margin-bottom: 15px;'>当前通关：<b>Level {current_lvl} / 20</b></p>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style='display: flex; justify-content: center; gap: 20px; margin-bottom: 20px;'>
            <div style='text-align: center;'><div style='font-size: 32px;' class='anim-fire'>🔥</div><div style='font-weight: bold; color: #ff9600;'>{st.session_state.streak} 天连胜</div></div>
            <div style='text-align: center;'><div style='font-size: 32px;' class='anim-heart'>❤️</div><div style='font-weight: bold; color: #ff4b4b;'>{st.session_state.hearts} 颗红心</div></div>
        </div>
        """, unsafe_allow_html=True)

        progress_pct = min(len(mastered_list) / 100.0, 1.0)
        st.progress(progress_pct)
        st.markdown(f"<p style='text-align: right; font-size: 12px; color: #58cc02; font-weight: bold;'>进度 {len(mastered_list)}/100 词</p>", unsafe_allow_html=True)

        st.write("")
        if st.button("🚀 继续学习新词汇", use_container_width=True, type="primary"):
            st.session_state.page = "study"
            st.rerun()
            
        st.write("")
        if st.button("🔁 查看已学单词重温", use_container_width=True):
            st.session_state.page = "review"
            st.rerun()
            
        st.markdown("<div class='section-title'>— 🎯 专项测验 —</div>", unsafe_allow_html=True)
        
        def enter_quiz(mode):
            st.session_state.quiz_mode = mode
            st.session_state.page = "quiz"
            st.session_state.pop("quiz_current", None)
            st.session_state.pop("quiz_answered", None)
            st.rerun()

        col_q1, col_q2 = st.columns(2)
        with col_q1:
            if st.button("👁️ 经典选择", use_container_width=True):
                enter_quiz("normal")
            if st.button("🔤 语境填空", use_container_width=True):
                enter_quiz("fill_blank")
        with col_q2:
            if st.button("🎧 盲听辨认", use_container_width=True):
                enter_quiz("listen")
            if st.button("✍️ 串字挑战", use_container_width=True):
                enter_quiz("spell")

        st.markdown("---")
        if st.button("🚪 退出登录 (切换账号)", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = "home"
            st.query_params.clear() 
            st.rerun()

    # ---------------- 子页面 ----------------
    else:
        if st.button("⬅️ 返回主页", type="secondary"):
            st.session_state.page = "home"
            st.session_state.pop("quiz_current", None)
            st.session_state.pop("quiz_answered", None)
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
                
                st.audio(get_audio_bytes(current["word"]), format="audio/mp3", autoplay=True)
                render_word_audio_button(current["word"], "🔊 点此朗读单词", autoplay=False)

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
                render_ai_speech_recognition(current["word"])

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
        # 🎯 专项大测验
        # ==========================================
        elif st.session_state.page == "quiz":
            if not all_learned_pool:
                st.info("💡 当前关卡还没有掌握任何单词，请先去【继续学习新词汇】模块打牢基础！")
            else:
                if st.session_state.hearts <= 0:
                    st.error("💔 你的红心耗尽了！测验被迫中断。")
                    if st.button("🔄 满血复活 (恢复 5 颗红心)", use_container_width=True, type="primary"):
                        st.session_state.hearts = 5
                        st.query_params["hearts"] = 5  
                        st.rerun()
                else:
                    q_type = st.session_state.get("quiz_mode", "normal")
                    
                    if "quiz_current" not in st.session_state:
                        q_item = random.choice(all_learned_pool)
                        st.session_state.quiz_current = q_item
                        st.session_state.quiz_type = q_type
                        
                        all_flat_words = [item for lvl_items in GLOBAL_VOCAB_DB.values() for item in lvl_items]
                        
                        if q_type in ["normal", "listen"]:
                            st.session_state.correct_ans = q_item["meaning"]
                            wrong_pool = [v["meaning"] for v in all_flat_words if v["meaning"] != q_item["meaning"]]
                            distractors = random.sample(wrong_pool, min(3, len(wrong_pool)))
                            options = distractors + [q_item["meaning"]]
                            random.shuffle(options)
                            st.session_state.quiz_options = options
                        elif q_type == "fill_blank":
                            st.session_state.correct_ans = q_item["word"]
                            wrong_pool = [v["word"] for v in all_flat_words if v["word"] != q_item["word"]]
                            distractors = random.sample(wrong_pool, min(3, len(wrong_pool)))
                            options = distractors + [q_item["word"]]
                            random.shuffle(options)
                            st.session_state.quiz_options = options
                        else: 
                            st.session_state.correct_ans = q_item["word"].lower()
                            st.session_state.quiz_options = []
                            
                        st.session_state.quiz_answered = False
                        st.session_state.selected_option = None

                    qc = st.session_state.quiz_current
                    q_type = st.session_state.get("quiz_type", "normal")
                    opts = st.session_state.get("quiz_options", [])
                    correct_ans = st.session_state.get("correct_ans", "")

                    # --- 答题后展现结果 ---
                    if st.session_state.get("quiz_answered", False):
                        selected = st.session_state.selected_option
                        
                        st.audio(get_audio_bytes(qc["word"]), format="audio/mp3", autoplay=True)
                        render_word_audio_button(qc["word"], "🔊 再次朗读单词", autoplay=False)

                        is_correct = (selected == correct_ans)

                        if is_correct:
                            status_msg = "✅ 完美！回答正确"
                            status_color = "#58cc02" 
                        else:
                            if q_type == "spell":
                                status_msg = f"❌ 拼错了！正确拼写是: {qc['word']}"
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
                            del st.session_state["quiz_current"]
                            st.rerun()

                    # --- 未答题状态 ---
                    else:
                        if q_type == "normal":
                            st.audio(get_audio_bytes(qc["word"]), format="audio/mp3", autoplay=True)
                            render_word_audio_button(qc["word"], "🔊 点击听音", autoplay=False)
                            st.markdown(f"<div class='quiz-card' style='margin-top:10px;'><div style='font-size:38px; font-weight:bold; color:#303133;'>{qc['word']}</div></div>", unsafe_allow_html=True)
                            
                        elif q_type == "listen":
                            st.markdown("<h4 style='text-align:center; color:#9c27b0;'>🎧 盲听辨义</h4>", unsafe_allow_html=True)
                            st.audio(get_audio_bytes(qc["word"]), format="audio/mp3", autoplay=True)
                            render_blind_listen_button(qc["word"], "🔊 播放神秘音频 (常速+慢速)", autoplay=False)
                            st.markdown(f"<div class='quiz-card' style='margin-top:10px;'><div style='font-size:20px; font-weight:bold; color:#afafaf;'>❓❓❓</div></div>", unsafe_allow_html=True)

                        elif q_type == "fill_blank":
                            st.markdown("<h4 style='text-align:center; color:#1cb0f6;'>🔤 语境填空</h4>", unsafe_allow_html=True)
                            masked_en = re.sub(r'(?i)\b' + re.escape(qc['word']) + r'\b', '____', qc['example_en'])
                            st.markdown(f"<div class='quiz-card' style='margin-top:10px;'><div style='font-size:22px; font-weight:bold; color:#303133; line-height: 1.5;'>{masked_en}</div><div style='font-size:14px; color:#afafaf; margin-top:8px;'>{qc['example_cn']}</div></div>", unsafe_allow_html=True)

                        elif q_type == "spell":
                            st.markdown("<h4 style='text-align:center; color:#1cb0f6;'>✍️ 串字挑战</h4>", unsafe_allow_html=True)
                            st.audio(get_audio_bytes(qc["word"]), format="audio/mp3", autoplay=True)
                            render_word_audio_button(qc["word"], "🔊 听发音拼写", autoplay=False)
                            st.markdown(f"<div class='quiz-card' style='margin-top:10px;'><div style='font-size:24px; font-weight:bold; color:#ff9600;'>{qc['meaning']}</div></div>", unsafe_allow_html=True)

                        if q_type == "spell":
                            with st.form("spell_form"):
                                user_spell = st.text_input("请在下方串出你听到的英文单词：")
                                submitted = st.form_submit_button("✅ 提交答案", use_container_width=True)
                                if submitted:
                                    st.session_state.quiz_answered = True
                                    st.session_state.selected_option = user_spell.strip().lower()
                                    if st.session_state.selected_option != correct_ans:
                                        st.session_state.hearts -= 1
                                        st.query_params["hearts"] = st.session_state.hearts
                                    st.rerun()
                        else:
                            col_a, col_b = st.columns(2)
                            labels = ["A", "B", "C", "D"]
                            for idx, opt in enumerate(opts):
                                current_col = col_a if idx % 2 == 0 else col_b
                                with current_col:
                                    if q_type in ["normal", "listen"]:
                                        parts = opt.split(" ", 1)
                                        btn_label = f"{labels[idx]}. {parts[1]} ({parts[0]})" if len(parts) == 2 else f"{labels[idx]}. {opt}"
                                    else:
                                        btn_label = f"{labels[idx]}. {opt}" 
                                        
                                    if st.button(btn_label, use_container_width=True, key=f"opt_{idx}"):
                                        st.session_state.quiz_answered = True
                                        st.session_state.selected_option = opt
                                        if opt != correct_ans:
                                            st.session_state.hearts -= 1
                                            st.query_params["hearts"] = st.session_state.hearts
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
                
                st.audio(get_audio_bytes(rc["word"]), format="audio/mp3", autoplay=True)
                render_word_audio_button(rc["word"], "🔊 点此朗读单词", autoplay=False)

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
                render_ai_speech_recognition(rc["word"])

                st.write("")
                if st.button("➡️ 换一个复习", use_container_width=True, type="primary"):
                    st.session_state.review_current = random.choice(mastered_list)
                    st.rerun()
