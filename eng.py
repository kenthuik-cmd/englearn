from io import BytesIO
import random
from gtts import gTTS
import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client

# 从 Streamlit 的 secrets 配置中读取你的 Supabase 链接和密匙
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_ANON_KEY"]
supabase = create_client(url, key)

# 页面设置
st.set_page_config(
    page_title="AI 英语背单词", page_icon="📖", layout="centered"
)

# 注入 CSS 样式：放大单词卡片，同时保持整体手机端单屏可容纳
st.markdown(
    """
    <style>
        /* 隐藏 Streamlit 默认的顶部导航和底部标识 */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* 页面整体内边距 */
        .block-container {
            padding-top: 0.5rem;
            padding-bottom: 1rem;
            padding-left: 0.8rem;
            padding-right: 0.8rem;
            max-width: 500px;
        }

        /* 手机端按钮美化 */
        .stButton > button {
            border-radius: 12px;
            font-weight: 600;
            padding: 0.5rem 0.8rem;
            font-size: 14px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        
        /* 放大后的单词背诵卡片样式 */
        .quiz-card {
            background-color: #ffffff;
            border: 1px solid #e4e7ed;
            padding: 24px 20px;
            border-radius: 18px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.08);
            margin-bottom: 15px;
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# 初始化 Session State
# ==========================================
if "user" not in st.session_state:
  st.session_state.user = None
if "grade" not in st.session_state:
  st.session_state.grade = 5
if "queue_g5" not in st.session_state:
  st.session_state.queue_g5 = list(
      [
          {
              "word": "active",
              "phonetic": "/ˈæktɪv/",
              "meaning": "adj. 积极的，活跃的",
              "example_en": "Be active in class.",
              "example_cn": "在课堂上要积极。",
          },
          {
              "word": "activity",
              "phonetic": "/ækˈtɪvəti/",
              "meaning": "n. 活动",
              "example_en": "We have many school activities.",
              "example_cn": "我们有很多学校活动。",
          },
          {
              "word": "afraid",
              "phonetic": "/əˈfreɪd/",
              "meaning": "adj. 害怕的，担心的",
              "example_en": "Don't be afraid of dogs.",
              "example_cn": "不要害怕狗。",
          },
          {
              "word": "animal",
              "phonetic": "/ˈænɪml/",
              "meaning": "n. 动物",
              "example_en": "The panda is a cute animal.",
              "example_cn": "大熊猫是一只可爱的动物。",
          },
          {
              "word": "answer",
              "phonetic": "/ˈɑːnsə(r)/",
              "meaning": "v./n. 回答，答案",
              "example_en": "Please answer my question.",
              "example_cn": "请回答我的问题。",
          },
          {
              "word": "autumn",
              "phonetic": "/ˈɔːtəm/",
              "meaning": "n. 秋天",
              "example_en": "Autumn is a harvest season.",
              "example_cn": "秋天是收获的季节。",
          },
          {
              "word": "become",
              "phonetic": "/bɪˈkʌm/",
              "meaning": "v. 变成，成为",
              "example_en": "I want to become a teacher.",
              "example_cn": "我想成为一名老师。",
          },
          {
              "word": "begin",
              "phonetic": "/bɪˈɡɪn/",
              "meaning": "v. 开始",
              "example_en": "Class begins at 8:00.",
              "example_cn": "8点钟开始上课。",
          },
          {
              "word": "behind",
              "phonetic": "/bɪˈhaɪnd/",
              "meaning": "prep. 在……后面",
              "example_en": "The cat is behind the door.",
              "example_cn": "猫在门后面。",
          },
          {
              "word": "better",
              "phonetic": "/ˈbetə(r)/",
              "meaning": "adj./adv. 更好的（地）",
              "example_en": "Practice makes better.",
              "example_cn": "熟能生巧。",
          },
      ]
  )
  random.shuffle(st.session_state.queue_g5)

if "mastered_g5" not in st.session_state:
  st.session_state.mastered_g5 = []
if "queue_g6" not in st.session_state:
  st.session_state.queue_g6 = list(
      [
          {
              "word": "achieve",
              "phonetic": "/əˈtʃiːv/",
              "meaning": "v. 实现，取得",
              "example_en": "You can achieve your goal.",
              "example_cn": "你能实现你的目标。",
          },
          {
              "word": "balance",
              "phonetic": "/ˈbæləns/",
              "meaning": "n./v. 平衡，均衡",
              "example_en": "Keep a balance between study and play.",
              "example_cn": "保持学习和玩耍的平衡。",
          },
          {
              "word": "communication",
              "phonetic": "/kəˌmjuːnɪˈkeɪʃn/",
              "meaning": "n. 交流，沟通",
              "example_en": "Good communication is important.",
              "example_cn": "良好的沟通很重要。",
          },
          {
              "word": "confident",
              "phonetic": "/ˈkɒnfɪdənt/",
              "meaning": "adj. 自信的",
              "example_en": "Be confident in yourself.",
              "example_cn": "对你自己要有信心。",
          },
          {
              "word": "curious",
              "phonetic": "/ˈkjʊəriəs/",
              "meaning": "adj. 好奇的",
              "example_en": "Children are curious about the world.",
              "example_cn": "孩子们对世界充满好奇。",
          },
      ]
  )
  random.shuffle(st.session_state.queue_g6)

if "mastered_g6" not in st.session_state:
  st.session_state.mastered_g6 = []
if "page" not in st.session_state:
  st.session_state.page = "home"


# 词库完整定义
VOCAB_GRADE_5 = [
    {
        "word": "active",
        "phonetic": "/ˈæktɪv/",
        "meaning": "adj. 积极的，活跃的",
        "example_en": "Be active in class.",
        "example_cn": "在课堂上要积极。",
    },
    {
        "word": "activity",
        "phonetic": "/ækˈtɪvəti/",
        "meaning": "n. 活动",
        "example_en": "We have many school activities.",
        "example_cn": "我们有很多学校活动。",
    },
    {
        "word": "afraid",
        "phonetic": "/əˈfreɪd/",
        "meaning": "adj. 害怕的，担心的",
        "example_en": "Don't be afraid of dogs.",
        "example_cn": "不要害怕狗。",
    },
    {
        "word": "animal",
        "phonetic": "/ˈænɪml/",
        "meaning": "n. 动物",
        "example_en": "The panda is a cute animal.",
        "example_cn": "大熊猫是一只可爱的动物。",
    },
    {
        "word": "answer",
        "phonetic": "/ˈɑːnsə(r)/",
        "meaning": "v./n. 回答，答案",
        "example_en": "Please answer my question.",
        "example_cn": "请回答我的问题。",
    },
    {
        "word": "autumn",
        "phonetic": "/ˈɔːtəm/",
        "meaning": "n. 秋天",
        "example_en": "Autumn is a harvest season.",
        "example_cn": "秋天是收获的季节。",
    },
    {
        "word": "become",
        "phonetic": "/bɪˈkʌm/",
        "meaning": "v. 变成，成为",
        "example_en": "I want to become a teacher.",
        "example_cn": "我想成为一名老师。",
    },
    {
        "word": "begin",
        "phonetic": "/bɪˈɡɪn/",
        "meaning": "v. 开始",
        "example_en": "Class begins at 8:00.",
        "example_cn": "8点钟开始上课。",
    },
    {
        "word": "behind",
        "phonetic": "/bɪˈhaɪnd/",
        "meaning": "prep. 在……后面",
        "example_en": "The cat is behind the door.",
        "example_cn": "猫在门后面。",
    },
    {
        "word": "better",
        "phonetic": "/ˈbetə(r)/",
        "meaning": "adj./adv. 更好的（地）",
        "example_en": "Practice makes better.",
        "example_cn": "熟能生巧。",
    },
]

VOCAB_GRADE_6 = [
    {
        "word": "achieve",
        "phonetic": "/əˈtʃiːv/",
        "meaning": "v. 实现，取得",
        "example_en": "You can achieve your goal.",
        "example_cn": "你能实现你的目标。",
    },
    {
        "word": "balance",
        "phonetic": "/ˈbæləns/",
        "meaning": "n./v. 平衡，均衡",
        "example_en": "Keep a balance between study and play.",
        "example_cn": "保持学习和玩耍的平衡。",
    },
    {
        "word": "communication",
        "phonetic": "/kəˌmjuːnɪˈkeɪʃn/",
        "meaning": "n. 交流，沟通",
        "example_en": "Good communication is important.",
        "example_cn": "良好的沟通很重要。",
    },
    {
        "word": "confident",
        "phonetic": "/ˈkɒnfɪdənt/",
        "meaning": "adj. 自信的",
        "example_en": "Be confident in yourself.",
        "example_cn": "对你自己要有信心。",
    },
    {
        "word": "curious",
        "phonetic": "/ˈkjʊəriəs/",
        "meaning": "adj. 好奇的",
        "example_en": "Children are curious about the world.",
        "example_cn": "孩子们对世界充满好奇。",
    },
]


def get_audio_bytes(text):
  tts = gTTS(text=text, lang="en")
  fp = BytesIO()
  tts.write_to_fp(fp)
  fp.seek(0)
  return fp.read()


def sync_progress_to_cloud(user_id, grade, mastered_list):
  try:
    supabase.table("user_profiles").upsert({
        "user_id": user_id,
        "grade": grade,
        "mastered_words": mastered_list,
    }).execute()
  except Exception as e:
    print("同步云端失败:", e)


# 确定当前年级对应的词库
if st.session_state.grade == 5:
  total_c = len(VOCAB_GRADE_5)
  rem_c = len(st.session_state.queue_g5)
  current_queue = st.session_state.queue_g5
  mastered_list = st.session_state.mastered_g5
  all_learned_pool = mastered_list + current_queue
else:
  total_c = len(VOCAB_GRADE_6)
  rem_c = len(st.session_state.queue_g6)
  current_queue = st.session_state.queue_g6
  mastered_list = st.session_state.mastered_g6
  all_learned_pool = mastered_list + current_queue


# ==========================================
# 🔐 未登录状态：手机端登录页
# ==========================================
if not st.session_state.user:
  st.markdown(
      "<h3 style='text-align: center; color: #303133; margin-top:"
      " 10px;'>📖 智能背单词 App</h3>",
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
          profile = (
              supabase.table("user_profiles")
              .select("*")
              .eq("user_id", res.user.id)
              .execute()
          )
          if profile.data:
            st.session_state.grade = profile.data[0].get("grade", 5)
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

# ==========================================
# 👤 已登录状态：手机端主页与功能页
# ==========================================
else:
  # ------------------------------------------
  # 🏠 HOME 主页
  # ------------------------------------------
  if st.session_state.page == "home":
    st.markdown(
        "<h3 style='text-align: center; color: #303133; margin-bottom:"
        " 5px;'>🌟 学习中心</h3>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='text-align: center; color: #909399; font-size: 12px;'"
        f" margin-bottom: 15px;>当前年级：小学 {st.session_state.grade} 年级</p>",
        unsafe_allow_html=True,
    )

    if st.button("📚 开启单词背诵与 AI 跟读", use_container_width=True):
      st.session_state.page = "study"
      st.rerun()

    st.write("")
    if st.button("🎯 进入已学单词小测验", use_container_width=True):
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
      st.rerun()

  # ------------------------------------------
  # ⬅️ 手机端子页面
  # ------------------------------------------
  else:
    if st.button("⬅️ 返回主页", type="secondary"):
      st.session_state.page = "home"
      st.rerun()

    # 1. 单词背诵与 AI 跟读模式
    if st.session_state.page == "study":
      if current_queue:
        current = current_queue[0]

        # 放大、高质感的单词卡片
        st.markdown(
            f"""
                <div class="quiz-card">
                    <div style="font-size: 36px; font-weight: bold; color: #303133; margin-bottom: 4px;">{current['word']}</div>
                    <div style="font-size: 14px; color: #909399; margin-bottom: 10px;">{current['phonetic']}</div>
                    <div style="font-size: 19px; font-weight: 600; color: #409EFF; margin-bottom: 12px;">{current['meaning']}</div>
                    <hr style="border: none; border-top: 1px solid #ebeef5; margin: 10px 0;">
                    <div style="font-size: 13px; color: #606266; font-style: italic; text-align: left;">
                        📝 <b>例句：</b>{current['example_en']}<br>🏷️ <b>翻译：</b>{current['example_cn']}
                    </div>
                </div>
                """,
            unsafe_allow_html=True,
        )

        # 紧凑的音频朗读与跟读组件
        c_audio, c_speak = st.columns(2)
        with c_audio:
          if st.button("🔊 朗读单词", use_container_width=True):
            st.audio(
                get_audio_bytes(current["word"]), format="audio/mp3", autoplay=True
            )
        with c_speak:
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

        # 底部操作按钮
        col1, col2 = st.columns(2)
        with col1:
          if st.button("❌ 模糊 (重练)", use_container_width=True):
            current_queue.append(current_queue.pop(0))
            st.rerun()
        with col2:
          if st.button(
              "✔ 认识 (下一个)", use_container_width=True, type="primary"
          ):
            done_word = current_queue.pop(0)
            if done_word not in mastered_list:
              mastered_list.append(done_word)
            sync_progress_to_cloud(
                st.session_state.user.id,
                st.session_state.grade,
                mastered_list,
            )
            st.rerun()
      else:
        if st.session_state.grade == 5:
          st.success("🎉 五年级单词已全通关！")
          if st.button(
              "🚀 进入六年级词汇", use_container_width=True, type="primary"
          ):
            st.session_state.grade = 6
            sync_progress_to_cloud(
                st.session_state.user.id,
                st.session_state.grade,
                mastered_list,
            )
            st.rerun()
        else:
          st.success("🏆 全通关大吉！")
          if st.button("🔄 重新复习全部课程", use_container_width=True):
            st.session_state.queue_g5 = list(VOCAB_GRADE_5)
            random.shuffle(st.session_state.queue_g5)
            st.session_state.queue_g6 = list(VOCAB_GRADE_6)
            random.shuffle(st.session_state.queue_g6)
            st.session_state.grade = 5
            sync_progress_to_cloud(
                st.session_state.user.id,
                st.session_state.grade,
                mastered_list,
            )
            st.rerun()

    # 2. 小测验面板
    elif st.session_state.page == "quiz":
      if not all_learned_pool:
        st.info("当前还没有学过任何单词！")
      else:
        if "quiz_current" not in st.session_state:
          q_item = random.choice(all_learned_pool)
          st.session_state.quiz_current = q_item
          wrong_meanings = [
              v["meaning"]
              for v in VOCAB_GRADE_5 + VOCAB_GRADE_6
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

        # 放大后的测验单词卡片
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
            btn_label = f"{labels[idx]}. {opt}"
            if st.button(btn_label, use_container_width=True, key=f"opt_{idx}"):
              st.session_state.quiz_answered = True
              st.session_state.selected_option = opt

        if st.session_state.get("quiz_answered", False):
          selected = st.session_state.selected_option
          audio_bytes = get_audio_bytes(qc["word"])
          st.audio(audio_bytes, format="audio/mp3", autoplay=True)

          if selected == qc["meaning"]:
            st.success("✅ 回答正确！")
          else:
            st.error(f"❌ 正确答案是：{qc['meaning']}")

          st.markdown(
              f"""
                    <div class="quiz-card" style="text-align: left; padding: 12px 16px; margin-top: 8px;">
                        <span style="font-size: 13px; font-weight: bold; color: #409EFF;">{qc['word']}</span> <span style="font-size: 11px; color: #909399;">{qc['phonetic']}</span>
                        <div style="font-size: 15px; font-weight: 600; color: #67C23A; margin: 2px 0;">{qc['meaning']}</div>
                    </div>
                    """,
              unsafe_allow_html=True,
          )

          if st.button("➡️ 下一题", use_container_width=True, type="primary"):
            q_item = random.choice(all_learned_pool)
            st.session_state.quiz_current = q_item
            wrong_meanings = [
                v["meaning"]
                for v in VOCAB_GRADE_5 + VOCAB_GRADE_6
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

    # 3. 已学单词重温面板
    elif st.session_state.page == "review":
      if not mastered_list:
        st.info("还没有掌握任何单词哦！")
      else:
        if "review_current" not in st.session_state:
          st.session_state.review_current = random.choice(mastered_list)

        rc = st.session_state.review_current
        with st.container():
          st.markdown(
              f"""
                <div class="quiz-card">
                    <div style="font-size: 36px; font-weight: bold; color: #303133; margin-bottom: 4px;">{rc['word']}</div>
                    <div style="font-size: 14px; color: #909399; margin-bottom: 10px;">{rc['phonetic']}</div>
                    <div style="font-size: 19px; font-weight: 600; color: #67C23A; margin-bottom: 12px;">{rc['meaning']}</div>
                    <hr style="border: none; border-top: 1px solid #ebeef5; margin: 10px 0;">
                    <div style="font-size: 13px; color: #606266; font-style: italic; text-align: left;">
                        📝 <b>例句：</b>{rc['example_en']}<br>🏷️ <b>翻译：</b>{rc['example_cn']}
                    </div>
                </div>
                """,
              unsafe_allow_html=True,
          )

          if st.button("🔊 朗读", use_container_width=True):
            st.audio(get_audio_bytes(rc["word"]), format="audio/mp3", autoplay=True)

        if st.button("➡️ 换一个复习", use_container_width=True, type="primary"):
          st.session_state.review_current = random.choice(mastered_list)
          st.rerun()
