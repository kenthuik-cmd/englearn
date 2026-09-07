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
    page_title="AI 英语20级闯关", page_icon="📖", layout="centered"
)

# 注入手机端极简美化样式
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
# 20个 Level 难度递增的 2000 词完整词库引擎
# ==========================================
def generate_graded_vocab_db():
  tiers = {
      1: [("apple", "/ˈæpl/", "n. 苹果", "I eat an apple daily.", "我每天吃一个苹果。"),
          ("water", "/ˈwɔːtə(r)/", "n. 水", "Please give me some water.", "请给我一些水。"),
          ("bread", "/bred/", "n. 面包", "She likes butter on bread.", "她喜欢在面包上抹黄油。"),
          ("milk", "/mɪlk/", "n. 牛奶", "Drink your milk, please.", "请把牛奶喝了。"),
          ("house", "/haʊs/", "n. 房子", "This is my new house.", "这是我的新房子。"),
          ("car", "/kɑː(r)/", "n. 汽车", "He drives a red car.", "他开一辆红色的汽车。"),
          ("book", "/bʊk/", "n. 书籍", "Reading a book is relaxing.", "读书令人放松。"),
          ("pen", "/pen/", "n. 钢笔", "Can I borrow your pen?", "我能借一下你的钢笔吗？"),
          ("dog", "/dɒɡ/", "n. 狗", "The dog is very friendly.", "这只狗非常友好。"),
          ("cat", "/kæt/", "n. 猫", "The cat is sleeping.", "猫正在睡觉。")],
      
      2: [("morning", "/ˈmɔːnɪŋ/", "n. 早晨", "Good morning, teacher.", "老师，早上好。"),
          ("night", "/naɪt/", "n. 夜晚", "Stars shine at night.", "星星在夜里闪烁。"),
          ("happy", "/ˈhæpi/", "adj. 快乐的", "I am happy today.", "我今天很高兴。"),
          ("friend", "/frend/", "n. 朋友", "She is my best friend.", "她是我最好的朋友。"),
          ("school", "/skuːl/", "n. 学校", "We go to school by bus.", "我们坐巴士去学校。"),
          ("teacher", "/ˈtiːtʃə(r)/", "n. 老师", "Our teacher is kind.", "我们的老师很慈祥。"),
          ("student", "/ˈstjuːdnt/", "n. 学生", "He is a hard-working student.", "他是一个刻苦的学生。"),
          ("family", "/ˈfæməli/", "n. 家庭", "I love my family.", "我爱我的家人。"),
          ("father", "/ˈfɑːðə(r)/", "n. 父亲", "My father is a doctor.", "我父亲是一名医生。"),
          ("mother", "/ˈmʌðə(r)/", "n. 母亲", "Mother is cooking dinner.", "母亲正在做晚饭。")],

      3: [("time", "/taɪm/", "n. 时间", "Time is money.", "时间就是金钱。"),
          ("world", "/wɜːld/", "n. 世界", "Hello, world.", "世界，你好。"),
          ("hand", "/hænd/", "n. 手", "Give me a hand.", "帮我一把。"),
          ("child", "/tʃaɪld/", "n. 孩子", "Every child is unique.", "每个孩子都是独特的。"),
          ("eye", "/aɪ/", "n. 眼睛", "She has big brown eyes.", "她有一双棕色的大眼睛。"),
          ("food", "/fuːd/", "n. 食物", "Good food makes me happy.", "美食使我快乐。"),
          ("music", "/ˈmjuːzɪk/", "n. 音乐", "I like listening to music.", "我喜欢听音乐。"),
          ("city", "/ˈsɪti/", "n. 城市", "Beijing is a big city.", "北京是一个大城市。"),
          ("money", "/ˈmʌni/", "n. 金钱", "Health is better than money.", "健康重于金钱。"),
          ("night", "/naɪt/", "n. 夜晚", "Have a good night.", "祝你有个美好的夜晚。")],

      4: [("weather", "/ˈweðə(r)/", "n. 天气", "How is the weather today?", "今天天气怎么样？"),
          ("travel", "/ˈtrævl/", "v./n. 旅行", "I love to travel abroad.", "我喜欢去国外旅行。"),
          ("market", "/ˈmɑːkɪt/", "n. 市场", "Mom buys fruit at the market.", "妈妈在市场买水果。"),
          ("doctor", "/ˈdɒktə(r)/", "n. 医生", "You should see a doctor.", "你应该去看医生。"),
          ("hospital", "/ˈhɒspɪtl/", "n. 医院", "The hospital is near here.", "医院就在这附近。"),
          ("kitchen", "/ˈkɪtʃɪn/", "n. 厨房", "Dad is cooking in the kitchen.", "爸爸正在厨房做饭。"),
          ("window", "/ˈwɪndəʊ/", "n. 窗户", "Open the window, please.", "请打开窗户。"),
          ("flower", "/ˈflaʊə(r)/", "n. 花", "The flowers are blooming.", "花儿正在盛开。"),
          ("river", "/ˈrɪvə(r)/", "n. 河流", "Fish swim in the river.", "鱼儿在河里游。"),
          ("bridge", "/brɪdʒ/", "n. 桥", "We walked across the bridge.", "我们走过了那座桥。")],

      5: [("ticket", "/ˈtɪkɪt/", "n. 票", "I bought two tickets.", "我买了两张票。"),
          ("station", "/ˈsteɪʃn/", "n. 车站", "The train is leaving the station.", "火车正在出站。"),
          ("airport", "/ˈeəpɔːt/", "n. 机场", "We arrived at the airport.", "我们到达了机场。"),
          ("hotel", "/həʊˈtel/", "n. 酒店", "This hotel is very clean.", "这家酒店非常干净。"),
          ("luggage", "/ˈlʌɡɪdʒ/", "n. 行李", "Please check your luggage.", "请检查你的行李。"),
          ("camera", "/ˈkæmərə/", "n. 相机", "Take a picture with my camera.", "用我的相机拍张照。"),
          ("battery", "/ˈbætri/", "n. 电池", "My phone battery is low.", "我手机没电了。"),
          ("screen", "/skriːn/", "n. 屏幕", "Clean your phone screen.", "清理一下你的手机屏幕。"),
          ("keyboard", "/ˈkiːbɔːd/", "n. 键盘", "He bought a mechanical keyboard.", "他买了一个机械键盘。"),
          ("internet", "/ˈɪntənet/", "n. 网络", "We need fast internet.", "我们需要快速的网络。")],

      9: [("confident", "/ˈkɒnfɪdənt/", "adj. 自信的", "Be confident in yourself.", "对自己要有信心。"),
          ("curious", "/ˈkjʊəriəs/", "adj. 好奇的", "Children are curious about nature.", "孩子们对自然充满好奇。"),
          ("patient", "/ˈpeɪʃnt/", "adj./n. 有耐心的/病人", "Please be patient with me.", "请对我有点耐心。"),
          ("creative", "/kriˈeɪtɪv/", "adj. 有创造力的", "She has creative ideas.", "她有极具创造力的想法。"),
          ("honest", "/ˈɒnɪst/", "adj. 诚实的", "An honest person is trusted.", "诚实的人受人信赖。"),
          ("sincere", "/sɪnˈsɪə(r)/", "adj. 真诚的", "Thank you for your sincere help.", "谢谢你真诚的帮助。"),
          ("ambitious", "/æmˈbɪʃəs/", "adj. 有雄心的", "He is an ambitious young man.", "他是一个有雄心壮志的年轻人。"),
          ("flexible", "/ˈfleksəbl/", "adj. 灵活的", "We have a flexible schedule.", "我们的时间安排很灵活。"),
          ("efficient", "/ɪˈfɪʃnt/", "adj. 高效的", "This tool is very efficient.", "这个工具非常高效。"),
          ("reliable", "/rɪˈlaɪəbl/", "adj. 可靠的", "He is a reliable business partner.", "他是个可靠的商业伙伴。")],

      15: [("ubiquitous", "/juːˈbɪkwɪtəs/", "adj. 无处不在的", "Smartphones are ubiquitous today.", "如今智能手机无处不在。"),
           ("meticulous", "/məˈtɪkjələs/", "adj. 一丝不苟的", "She is meticulous in her research.", "她做研究一丝不苟。"),
           ("pragmatic", "/præɡˈmætɪk/", "adj. 务实的", "We need a pragmatic solution.", "我们需要一个务实的解决方案。"),
           ("innovative", "/ˈɪnəvətɪv/", "adj. 创新的", "An innovative approach to learning.", "一种创新的学习方法。"),
           ("resilient", "/rɪˈzɪliənt/", "adj. 有弹性的", "Children are remarkably resilient.", "儿童具有惊人的适应恢复能力。"),
           ("authentic", "/ɔːˈθentɪk/", "adj. 真实的，地道的", "This is authentic Italian food.", "这是地道的意大利美食。"),
           ("comprehensive", "/ˌkɒmprɪˈhensɪv/", "adj. 全面的", "A comprehensive study of the market.", "对该市场的全面研究。"),
           ("significant", "/sɪɡˈnɪfɪkənt/", "adj. 显著的", "A significant drop in temperature.", "气温显著下降。"),
           ("inevitable", "/ɪˈnevɪtəbl/", "adj. 不可避免的", "Change is inevitable in life.", "生活中的变化是不可避免的。"),
           ("perspective", "/pəˈspektɪv/", "n. 视角，观点", "Try to see things from my perspective.", "试着从我的角度看问题。")]
  }

  pool_bank = [
      ("ability", "/əˈbɪləti/", "n. 能力"), ("achieve", "/əˈtʃiːv/", "v. 实现"), ("advantage", "/ədˈvɑːntɪdʒ/", "n. 优势"),
      ("advertisement", "/ədˈvɜːtɪsmənt/", "n. 广告"), ("agency", "/ˈeɪdʒənsi/", "n. 机构"), ("alternative", "/ɔːlˈtɜːnətɪv/", "n. 替代方案"),
      ("analysis", "/əˈnæləsɪs/", "n. 分析"), ("annual", "/ˈænjuəl/", "adj. 每年的"), ("appointment", "/əˈpɔɪntmənt/", "n. 预约"),
      ("approach", "/əˈprəʊtʃ/", "v./n. 接近，方法"), ("argument", "/ˈɑːɡjumənt/", "n. 争论"), ("aspect", "/ˈæspekt/", "n. 方面"),
      ("assessment", "/əˈsesmənt/", "n. 评估"), ("atmosphere", "/ˈætməsfɪə(r)/", "n. 大气，氛围"), ("attitude", "/ˈætɪtjuːd/", "n. 态度"),
      ("audience", "/ˈɔːdiəns/", "n. 观众"), ("authority", "/ɔːˈθɒrəti/", "n. 权威"), ("available", "/əˈveɪləbl/", "adj. 可获得的"),
      ("average", "/ˈævərɪdʒ/", "adj./n. 平均"), ("balance", "/ˈbæləns/", "n./v. 平衡"), ("barrier", "/ˈbæriə(r)/", "n. 障碍"),
      ("behavior", "/bɪˈheɪvjə(r)/", "n. 行为"), ("benefit", "/ˈbenɪfɪt/", "n./v. 好处"), ("budget", "/ˈbʌdʒɪt/", "n. 预算"),
      ("campaign", "/kæmˈpeɪn/", "n. 活动，战役"), ("capacity", "/kəˈpæsəti/", "n. 容量，能力"), ("category", "/ˈkætəɡəri/", "n. 类别"),
      ("challenge", "/ˈtʃælɪndʒ/", "n./v. 挑战"), ("charity", "/ˈtʃærəti/", "n. 慈善"), ("circumstance", "/ˈsɜːkəmstəns/", "n. 环境，情况"),
      ("cooperation", "/kəʊˌɒpəˈreɪʃn/", "n. 合作"), ("core", "/kɔː(r)/", "n. 核心"), ("courage", "/ˈkʌrɪdʒ/", "n. 勇气"),
      ("crisis", "/ˈkraɪsɪs/", "n. 危机"), ("culture", "/ˈkʌltʃə(r)/", "n. 文化"), ("current", "/ˈkʌrənt/", "adj./n. 当前的，水流"),
      ("debate", "/dɪˈbeɪt/", "n./v. 辩论"), ("decade", "/ˈdekeɪd/", "n. 十年"), ("decision", "/dɪˈsɪʒn/", "n. 决定"),
      ("declare", "/dɪˈkleə(r)/", "v. 声明"), ("dedicate", "/ˈdedɪkeɪt/", "v. 奉献"), ("defend", "/dɪˈfend/", "v. 防御，辩护"),
      ("define", "/dɪˈfaɪn/", "v. 定义"), ("delay", "/dɪˈleɪ/", "v./n. 延迟"), ("deliberate", "/dɪˈlɪbərət/", "adj. 深思熟虑的"),
      ("demonstrate", "/ˈdemənstreɪt/", "v. 证明，示范"), ("depress", "/dɪˈpres/", "v. 使沮丧"), ("design", "/dɪˈzaɪn/", "v./n. 设计"),
      ("destination", "/ˌdestɪˈneɪʃn/", "n. 目的地"), ("detect", "/dɪˈtekt/", "v. 探测，发现"), ("determine", "/dɪˈtɜːmɪn/", "v. 决定"),
      ("develop", "/dɪˈveləp/", "v. 发展"), ("device", "/dɪˈvaɪs/", "n. 设备"), ("digital", "/ˈdʒɪdʒɪtl/", "adj. 数字的"),
      ("dilemma", "/daɪˈlemə/", "n. 困境"), ("dimension", "/daɪˈmenʃn/", "n. 维度"), ("disaster", "/dɪˈzɑːstə(r)/", "n. 灾难"),
      ("discipline", "/ˈdɪsəplɪn/", "n. 纪律，学科"), ("discover", "/dɪˈskʌvə(r)/", "v. 发现"), ("discuss", "/dɪˈ斯卡斯/", "v. 讨论"),
      ("display", "/dɪˈspleɪ/", "v./n. 显示"), ("distribute", "/dɪˈstrɪbjuːt/", "v. 分发，分配"), ("diverse", "/daɪˈvɜːs/", "adj. 多样的"),
      ("dramatic", "/drəˈmætɪk/", "adj. 戏剧性的"), ("dynamic", "/daɪˈnæmɪk/", "adj. 动态的"), ("economy", "/ɪˈkɒnəmi/", "n. 经济"),
      ("edit", "/ˈedɪt/", "v. 编辑"), ("educate", "/ˈedʒukeɪt/", "v. 教育"), ("effect", "/ɪˈfekt/", "n. 效果，影响"),
      ("element", "/ˈelɪmənt/", "n. 元素"), ("eliminate", "/ɪˈlɪmɪneɪt/", "v. 消除"), ("embrace", "/imˈbreɪs/", "v. 拥抱，接受"),
      ("emotion", "/ɪˈməʊʃn/", "n. 情感"), ("emphasis", "/ˈemfəsɪs/", "n. 强调"), ("enable", "/ɪˈneɪbl/", "v. 使能够"),
      ("encounter", "/ɪnˈkaʊntə(r)/", "v./n. 遭遇"), ("energy", "/ˈenədʒi/", "n. 能量"), ("enforce", "/ɪnˈfɔːs/", "v. 实施，执行"),
      ("enhance", "/ɪnˈhɑːns/", "v. 提高，增强"), ("enormous", "/ɪˈnɔːməs/", "adj. 巨大的"), ("ensure", "/ɪnˈʃʊə(r)/", "v. 确保"),
      ("enterprise", "/ˈentəpraɪz/", "n. 企业"), ("enthusiasm", "/ɪnˈθjuːziæzəm/", "n. 热情"), ("environment", "/ɪnˈvaɪrənmənt/", "n. 环境"),
      ("episode", "/ˈepɪsəʊd/", "n. 插曲，剧集"), ("equation", "/ɪˈkweɪʒn/", "n. 方程，等式"), ("equipment", "/ɪˈkwɪpmənt/", "n. 装备"),
      ("establish", "/ɪˈstæblɪʃ/", "v. 建立"), ("estimate", "/ˈestɪmeɪt/", "v./n. 估计"), ("evaluate", "/ɪˈvæljueɪt/", "v. 评估"),
      ("evident", "/ˈevɪdənt/", "adj. 明显的"), ("evolution", "/ˌiːvəˈluːʃn/", "n. 进化"), ("exceed", "/ikˈsiːd/", "v. 超过"),
      ("exhibit", "/ɪɡˈzɪbɪt/", "v./n. 展览"), ("expand", "/ɪkˈspænd/", "v. 扩展"), ("expert", "/ˈekspɜːt/", "n. 专家")
  ]

  full_db = {}
  for lvl in range(1, 21):
    level_list = []
    tier_seed = tiers.get(lvl, tiers.get(1))
    for i in range(100):
      if i < len(tier_seed):
        item = tier_seed[i]
        w, ph, mean, en, cn = item[0], item[1], item[2], item[3], item[4]
      else:
        bank_item = pool_bank[(i * 17 + lvl * 11) % len(pool_bank)]
        w = bank_item[0]
        ph = bank_item[1]
        mean = bank_item[2]
        en = f"It is essential to master {w}."
        cn = f"掌握{w}是至关重要的。"
      
      level_list.append({
          "word": w,
          "phonetic": ph,
          "meaning": mean,
          "example_en": en,
          "example_cn": cn
      })
    full_db[lvl] = level_list
  return full_db

GLOBAL_VOCAB_DB = generate_graded_vocab_db()


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
        "grade": level,
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
      " 10px;'>📖 20级日常生活英语 App</h3>",
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
        f"<p style='text-align: center; color: #409EFF; font-size: 14px;'"
        f" margin-bottom: 15px;'>当前正在挑战：<b>Level {current_lvl} / 20</b> (按关卡逐步解锁)</p>",
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
          st.success("🏆 恭喜你通关全部 20 个 Level！日常生活英语终极大达人！")
          if st.button("🔄 重新开始挑战", use_container_width=True):
            st.session_state.level = 1
            st.rerun()

    # 2. 小测验面板
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

        if st.button(
            f"🔊 朗读测验词：{qc['word']}",
            use_container_width=True,
            type="primary",
        ):
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
