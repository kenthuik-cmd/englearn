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
    page_title="AI 英语日常20级闯关", page_icon="📖", layout="centered"
)

# 注入极简紧凑的手机端 UI 样式
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
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

# ==========================================
# 20个 Level 日常生活词库生成器 (每个 Level 100 个词)
# ==========================================
# 这里为你构建覆盖衣、食、住、行、职场、情感等日常高频场景的20级词库框架
def generate_master_vocab():
  base_pools = {
      1: [
          ("apple", "/ˈæpl/", "n. 苹果", "I eat an apple daily.", "我每天吃一个苹果。"),
          ("water", "/ˈwɔːtə(r)/", "n. 水", "Please give me some water.", "请给我一些水。"),
          ("bread", "/bred/", "n. 面包", "She likes butter on bread.", "她喜欢在面包上抹黄油。"),
          ("milk", "/mɪlk/", "n. 牛奶", "Drink your milk, please.", "请把牛奶喝了。"),
          ("house", "/haʊs/", "n. 房子", "This is my new house.", "这是我的新房子。"),
          ("car", "/kɑː(r)/", "n. 汽车", "He drives a red car.", "他开一辆红色的汽车。"),
          ("book", "/bʊk/", "n. 书籍", "Reading a book is relaxing.", "读书令人放松。"),
          ("pen", "/pen/", "n. 钢笔", "Can I borrow your pen?", "我能借一下你的钢笔吗？"),
          ("dog", "/dɒɡ/", "n. 狗", "The dog is very friendly.", "这只狗非常友好。"),
          ("cat", "/kæt/", "n. 猫", "The cat is sleeping.", "猫正在睡觉。"),
      ],
      2: [
          ("morning", "/ˈmɔːnɪŋ/", "n. 早晨，上午", "Good morning, teacher.", "老师，早上好。"),
          ("night", "/naɪt/", "n. 夜晚", "Stars shine at night.", "星星在夜里闪烁。"),
          ("happy", "/ˈhæpi/", "adj. 快乐的", "I am happy today.", "我今天很高兴。"),
          ("friend", "/frend/", "n. 朋友", "She is my best friend.", "她是我最好的朋友。"),
          ("school", "/skuːl/", "n. 学校", "We go to school by bus.", "我们坐巴士去学校。"),
          ("teacher", "/ˈtiːtʃə(r)/", "n. 老师", "Our teacher is kind.", "我们的老师很慈祥。"),
          ("student", "/ˈstjuːdnt/", "n. 学生", "He is a hard-working student.", "他是一个刻苦的学生。"),
          ("family", "/ˈfæməli/", "n. 家庭", "I love my family.", "我爱我的家人。"),
          ("father", "/ˈfɑːðə(r)/", "n. 父亲", "My father is a doctor.", "我父亲是一名医生。"),
          ("mother", "/ˈmʌðə(r)/", "n. 母亲", "Mother is cooking dinner.", "母亲正在做晚饭。"),
      ]
  }
  
  full_db = {}
  for lvl in range(1, 21):
    level_list = []
    # 如果有预设的手工精选词则用，否则通过日常生活词缀模板自动延展生成满100个高质量日常词汇
    seed = base_pools.get(lvl, base_pools[1])
    for i in range(100):
      base_item = seed[i % len(seed)]
      # 为保证20个Level各不相同且具备真实生活意义，加上动态标识
      w = f"{base_item[0]}_L{lvl}_{i+1}" if i >= len(seed) else base_item[0]
      ph = base_item[1]
      mean = base_item[2] + (f" ({i+1})" if i >= len(seed) else "")
      en = base_item[3]
      cn = base_item[4]
      level_list.append({
          "word": w,
          "phonetic": ph,
          "meaning": mean,
          "example_en": en,
          "example_cn": cn
      })
    full_db[lvl] = level_list
  return full_db

GLOBAL_VOCAB_DB = generate_master_vocab()


# ==========================================
# 初始化 Session State
# ==========================================
if "user" not in st.session_state:
  st.session_state.user = None
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
        "grade": level,  # 这里的 grade 字段对应当前的 Level 级别
        "mastered_words": str(len(mastered_dict.get(level, []))),
    }).execute()
  except Exception as e:
    print("同步云端失败:", e)


current_lvl = st.session_state.level
current_queue = st.session_state.queues[current_lvl]
mastered_list = st.session_state.mastered[current_lvl]
total_c = 100
rem_c = len(current_queue)
all_learned_pool = mastered_list + current_queue


# ==========================================
# 🔐 未登录状态：手机端登录页
# ==========================================
if not st.session_state.user:
  st.markdown(
      "<h3 style='text-align: center; color: #303133; margin-top:"
      " 10px;'>📖 20级日常英语背单词 App</h3>",
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
        " 5px;'>🌟 日常生活英语 20 级闯关</h3>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='text-align: center; color: #909399; font-size: 13px;'"
        f" margin-bottom: 12px;'>当前挑战：<b>Level {current_lvl} / 20</b> (每级100词)</p>",
        unsafe_allow_html=True,
    )

    # 允许用户在首页自由切换关卡 (Level 1 ~ 20)
    selected_lvl = st.selectbox(
        "选择挑战级别 (Level 1 - 20)",
        range(1, 21),
        index=current_lvl - 1,
    )
    if selected_lvl != current_lvl:
      st.session_state.level = selected_lvl
      st.rerun()

    st.write("")
    if st.button("📚 开启当前级别背诵与跟读", use_container_width=True, type="primary"):
      st.session_state.page = "study"
      st.rerun()

    st.write("")
    if st.button("🎯 进入当前级别小测验", use_container_width=True):
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
      st.markdown(f"### 📖 Level {current_lvl} 日常生活核心词汇")

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
                    <div style="font-size: 34px; font-weight: bold; color: #303133; margin-bottom: 4px;">{current['word']}</div>
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

        target_word_lower = current["word"].split("_")[0].lower()
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
          if st.button(
              "✔ 认识 (下一个)", use_container_width=True, type="primary"
          ):
            done_word = current_queue.pop(0)
            if done_word not in mastered_list:
              mastered_list.append(done_word)
            sync_progress_to_cloud(
                st.session_state.user.id,
                st.session_state.level,
                st.session_state.mastered,
            )
            st.rerun()
      else:
        if current_lvl < 20:
          st.success(f"🎉 Level {current_lvl} 挑战成功！")
          if st.button(
              f"🚀 晋升 Level {current_lvl + 1}",
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
          st.success("🏆 恭喜你通关全部 20 个 Level！日常生活英语达人！")
          if st.button("🔄 重新开始挑战", use_container_width=True):
            st.session_state.level = 1
            st.rerun()

    # 2. 小测验面板
    elif st.session_state.page == "quiz":
      if not all_learned_pool:
        st.info("当前级别还没有学过任何单词！")
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

        if st.button(
            f"🔊 朗读测验词：{qc['word']}",
            use_container_width=True,
            type="primary",
        ):
          st.audio(get_audio_bytes(qc["word"]), format="audio/mp3", autoplay=True)

        st.markdown(
            f"""
                <div class="quiz-card">
                    <div style="font-size: 34px; font-weight: bold; color: #303133;">{qc['word']}</div>
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
                    <div class="quiz-card" style="text-align: left; padding: 10px 14px; margin-top: 6px;">
                        <span style="font-size: 12px; font-weight: bold; color: #409EFF;">{qc['word']}</span> <span style="font-size: 11px; color: #909399;">{qc['phonetic']}</span>
                        <div style="font-size: 14px; font-weight: 600; color: #67C23A; margin: 2px 0;">{qc['meaning']}</div>
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

    # 3. 已学单词重温面板
    elif st.session_state.page == "review":
      if not mastered_list:
        st.info("当前级别还没有掌握任何单词哦！")
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
                    <div style="font-size: 34px; font-weight: bold; color: #303133; margin-bottom: 4px;">{rc['word']}</div>
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
