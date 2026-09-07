from io import BytesIO
import random
from gtts import gTTS
import streamlit as st

# 100个小学五年级核心英语单词库
VOCAB_LIST = [
    {
        "word": "active",
        "phonetic": "/ˈæktɪv/",
        "meaning": "adj. 积极的，活跃的",
        "example": "Be active in class.",
    },
    {
        "word": "activity",
        "phonetic": "/ækˈtɪvəti/",
        "meaning": "n. 活动",
        "example": "We have many school activities.",
    },
    {
        "word": "afraid",
        "phonetic": "/əˈfreɪd/",
        "meaning": "adj. 害怕的，担心的",
        "example": "Don't be afraid of dogs.",
    },
    {
        "word": "animal",
        "phonetic": "/ˈænɪml/",
        "meaning": "n. 动物",
        "example": "The panda is a cute animal.",
    },
    {
        "word": "answer",
        "phonetic": "/ˈɑːnsə(r)/",
        "meaning": "v./n. 回答，答案",
        "example": "Please answer my question.",
    },
    {
        "word": "autumn",
        "phonetic": "/ˈɔːtəm/",
        "meaning": "n. 秋天",
        "example": "Autumn is a harvest season.",
    },
    {
        "word": "become",
        "phonetic": "/bɪˈkʌm/",
        "meaning": "v. 变成，成为",
        "example": "I want to become a teacher.",
    },
    {
        "word": "begin",
        "phonetic": "/bɪˈɡɪn/",
        "meaning": "v. 开始",
        "example": "Class begins at 8:00.",
    },
    {
        "word": "behind",
        "phonetic": "/bɪˈhaɪnd/",
        "meaning": "prep. 在……后面",
        "example": "The cat is behind the door.",
    },
    {
        "word": "better",
        "phonetic": "/ˈbetə(r)/",
        "meaning": "adj./adv. 更好的（地）",
        "example": "Practice makes better.",
    },
    {
        "word": "breakfast",
        "phonetic": "/ˈbrekfəst/",
        "meaning": "n. 早餐",
        "example": "I eat eggs for breakfast.",
    },
    {
        "word": "bring",
        "phonetic": "/brɪŋ/",
        "meaning": "v. 带来，拿来",
        "example": "Bring your homework tomorrow.",
    },
    {
        "word": "building",
        "phonetic": "/ˈbɪldɪŋ/",
        "meaning": "n. 建筑物，房子",
        "example": "This is a tall building.",
    },
    {
        "word": "busy",
        "phonetic": "/ˈbɪzi/",
        "meaning": "adj. 忙碌的",
        "example": "My mother is busy cooking.",
    },
    {
        "word": "careful",
        "phonetic": "/ˈkeəfl/",
        "meaning": "adj. 小心的，仔细的",
        "example": "Be careful when you cross the road.",
    },
    {
        "word": "catch",
        "phonetic": "/kætʃ/",
        "meaning": "v. 抓住，接住",
        "example": "Catch the ball, please.",
    },
    {
        "word": "center",
        "phonetic": "/ˈsentə(r)/",
        "meaning": "n. 中心，中央",
        "example": "It is in the city center.",
    },
    {
        "word": "change",
        "phonetic": "/tʃeɪndʒ/",
        "meaning": "v./n. 改变，变化",
        "example": "Leaves change color in autumn.",
    },
    {
        "word": "cheap",
        "phonetic": "/tʃiːp/",
        "meaning": "adj. 便宜的",
        "example": "This book is cheap.",
    },
    {
        "word": "choose",
        "phonetic": "/tʃuːz/",
        "meaning": "v. 选择，挑选",
        "example": "Choose a gift you like.",
    },
    {
        "word": "climb",
        "phonetic": "/klaɪm/",
        "meaning": "v. 爬，攀登",
        "example": "We like to climb mountains.",
    },
    {
        "word": "cloudy",
        "phonetic": "/ˈklaʊdi/",
        "meaning": "adj. 多云的",
        "example": "It is cloudy today.",
    },
    {
        "word": "collect",
        "phonetic": "/kəˈlekt/",
        "meaning": "v. 收集，搜集",
        "example": "I like to collect stamps.",
    },
    {
        "word": "comfortable",
        "phonetic": "/ˈkʌmfətəbl/",
        "meaning": "adj. 舒适的，舒服的",
        "example": "This bed is very comfortable.",
    },
    {
        "word": "concert",
        "phonetic": "/ˈkɒnsət/",
        "meaning": "n. 音乐会",
        "example": "We went to a music concert.",
    },
    {
        "word": "cool",
        "phonetic": "/kuːl/",
        "meaning": "adj. 凉爽的，酷的",
        "example": "The weather is cool today.",
    },
    {
        "word": "country",
        "phonetic": "/ˈkʌntri/",
        "meaning": "n. 国家，乡村",
        "example": "China is a great country.",
    },
    {
        "word": "dangerous",
        "phonetic": "/ˈdeɪndʒərəs/",
        "meaning": "adj. 危险的",
        "example": "Fire is dangerous.",
    },
    {
        "word": "decide",
        "phonetic": "/dɪˈsaɪd/",
        "meaning": "v. 决定，下决心",
        "example": "Decide what to do next.",
    },
    {
        "word": "different",
        "phonetic": "/ˈdɪfrənt/",
        "meaning": "adj. 不同的",
        "example": "We have different hobbies.",
    },
    {
        "word": "difficult",
        "phonetic": "/ˈdɪfɪkəlt/",
        "meaning": "adj. 困难的",
        "example": "Math can be difficult sometimes.",
    },
    {
        "word": "direction",
        "phonetic": "/dəˈrekʃn/",
        "meaning": "n. 方向，说明",
        "example": "Which direction should we go?",
    },
    {
        "word": "discover",
        "phonetic": "/dɪˈskʌvə(r)/",
        "meaning": "v. 发现",
        "example": "Columbus discover new lands.",
    },
    {
        "word": "drive",
        "phonetic": "/draɪv/",
        "meaning": "v. 驾驶，开车",
        "example": "My father can drive a car.",
    },
    {
        "word": "early",
        "phonetic": "/ˈɜːli/",
        "meaning": "adj./adv. 早的（地）",
        "example": "Get up early in the morning.",
    },
    {
        "word": "earth",
        "phonetic": "/ɜːθ/",
        "meaning": "n. 地球，泥土",
        "example": "We live on the earth.",
    },
    {
        "word": "easily",
        "phonetic": "/ˈiːzɪli/",
        "meaning": "adv. 容易地",
        "example": "She can speak English easily.",
    },
    {
        "word": "energy",
        "phonetic": "/ˈenədʒi/",
        "meaning": "n. 能量，精力",
        "example": "Children have much energy.",
    },
    {
        "word": "environment",
        "phonetic": "/ɪnˈvaɪrənmənt/",
        "meaning": "n. 环境",
        "example": "Protect our environment.",
    },
    {
        "word": "example",
        "phonetic": "/ɪɡˈzɑːmpl/",
        "meaning": "n. 例子，榜样",
        "example": "Let me give you an example.",
    },
    {
        "word": "exciting",
        "phonetic": "/ɪkˈsaɪtɪŋ/",
        "meaning": "adj. 令人兴奋的",
        "example": "The football match is exciting.",
    },
    {
        "word": "expensive",
        "phonetic": "/ɪkˈspensɪv/",
        "meaning": "adj. 昂贵的",
        "example": "The watch is too expensive.",
    },
    {
        "word": "experiment",
        "phonetic": "/ɪkˈsperɪmənt/",
        "meaning": "n./v. 实验",
        "example": "We do a science experiment.",
    },
    {
        "word": "famous",
        "phonetic": "/ˈfeɪməs/",
        "meaning": "adj. 著名的",
        "example": "Beijing is a famous city.",
    },
    {
        "word": "favourite",
        "phonetic": "/ˈfeɪvərɪt/",
        "meaning": "adj./n. 特别喜爱的",
        "example": "Blue is my favourite color.",
    },
    {
        "word": "feel",
        "phonetic": "/fiːl/",
        "meaning": "v. 觉得，感到",
        "example": "I feel happy today.",
    },
    {
        "word": "festival",
        "phonetic": "/ˈfestɪvl/",
        "meaning": "n. 节日",
        "example": "Spring Festival is joyful.",
    },
    {
        "word": "finish",
        "phonetic": "/ˈfɪnɪʃ/",
        "meaning": "v. 完成，结束",
        "example": "Finish your homework first.",
    },
    {
        "word": "foreign",
        "phonetic": "/ˈfɒrən/",
        "meaning": "adj. 外国的",
        "example": "I want to learn a foreign language.",
    },
    {
        "word": "forest",
        "phonetic": "/ˈfɒrɪst/",
        "meaning": "n. 森林",
        "example": "Many animals live in the forest.",
    },
    {
        "word": "forget",
        "phonetic": "/fəˈɡet/",
        "meaning": "v. 忘记",
        "example": "Don't forget your umbrella.",
    },
    {
        "word": "friendly",
        "phonetic": "/ˈfrendli/",
        "meaning": "adj. 友好的",
        "example": "Our teachers are very friendly.",
    },
    {
        "word": "future",
        "phonetic": "/ˈfjuːtʃə(r)/",
        "meaning": "n. 未来",
        "example": "What will you be in the future?",
    },
    {
        "word": "garden",
        "phonetic": "/ˈɡɑːdn/",
        "meaning": "n. 花园",
        "example": "There are flowers in the garden.",
    },
    {
        "word": "gentle",
        "phonetic": "/ˈdʒentl/",
        "meaning": "adj. 温柔的，温和的",
        "example": "She has a gentle voice.",
    },
    {
        "word": "global",
        "phonetic": "/ˈɡləʊbl/",
        "meaning": "adj. 全球的",
        "example": "It is a global village.",
    },
    {
        "word": "grade",
        "phonetic": "/ɡreɪd/",
        "meaning": "n. 年级，成绩",
        "example": "I am in Grade Five.",
    },
    {
        "word": "group",
        "phonetic": "/ɡruːp/",
        "meaning": "n. 群，组",
        "example": "Work in groups, please.",
    },
    {
        "word": "habit",
        "phonetic": "/ˈhæbɪt/",
        "meaning": "n. 习惯",
        "example": "Reading is a good habit.",
    },
    {
        "word": "happily",
        "phonetic": "/ˈhæpɪli/",
        "meaning": "adv. 快乐地，高兴地",
        "example": "They live happily together.",
    },
    {
        "word": "healthy",
        "phonetic": "/ˈhelθi/",
        "meaning": "adj. 健康的",
        "example": "Eat fruit to stay healthy.",
    },
    {
        "word": "history",
        "phonetic": "/ˈhɪstəri/",
        "meaning": "n. 历史",
        "example": "I like reading history books.",
    },
    {
        "word": "holiday",
        "phonetic": "/ˈhɒlədeɪ/",
        "meaning": "n. 节日，假期",
        "example": "Where will you go for the holiday?",
    },
    {
        "word": "important",
        "phonetic": "/ɪmˈpɔːtnt/",
        "meaning": "adj. 重要的",
        "example": "English is an important language.",
    },
    {
        "word": "improve",
        "phonetic": "/ɪmˈpruːv/",
        "meaning": "v. 改进，改善",
        "example": "Practice helps improve your skills.",
    },
    {
        "word": "information",
        "phonetic": "/ˌɪnfəˈmeɪʃn/",
        "meaning": "n. 信息，资料",
        "example": "Search for more information.",
    },
    {
        "word": "interested",
        "phonetic": "/ˈɪntrəstɪd/",
        "meaning": "adj. 感兴趣的",
        "example": "I am interested in science.",
    },
    {
        "word": "invent",
        "phonetic": "/ɪnˈvent/",
        "meaning": "v. 发明，创造",
        "example": "Who did invent the light bulb?",
    },
    {
        "word": "journey",
        "phonetic": "/ˈdʒɜːni/",
        "meaning": "n. 旅行，旅程",
        "example": "Have a safe journey home.",
    },
    {
        "word": "knowledge",
        "phonetic": "/ˈnɒlɪdʒ/",
        "meaning": "n. 知识，学问",
        "example": "Books give us knowledge.",
    },
    {
        "word": "language",
        "phonetic": "/ˈlæŋɡwɪdʒ/",
        "meaning": "n. 语言",
        "example": "English is a global language.",
    },
    {
        "word": "laugh",
        "phonetic": "/lɑːf/",
        "meaning": "v./n. 笑，大笑",
        "example": "Do not laugh at others.",
    },
    {
        "word": "learn",
        "phonetic": "/lɜːn/",
        "meaning": "v. 学习，学会",
        "example": "Learn new words every day.",
    },
    {
        "word": "library",
        "phonetic": "/ˈlaɪbrəri/",
        "meaning": "n. 图书馆",
        "example": "We read books in the library.",
    },
    {
        "word": "listen",
        "phonetic": "/ˈlɪsn/",
        "meaning": "v. 听",
        "example": "Listen to the teacher carefully.",
    },
    {
        "word": "lovely",
        "phonetic": "/ˈlʌvli/",
        "meaning": "adj. 可爱的，美丽的",
        "example": "What a lovely day!",
    },
    {
        "word": "machine",
        "phonetic": "/məˈʃiːn/",
        "meaning": "n. 机器",
        "example": "This is a washing machine.",
    },
    {
        "word": "market",
        "phonetic": "/ˈmɑːkɪt/",
        "meaning": "n. 市场，集市",
        "example": "Mom buys fruit at the market.",
    },
    {
        "word": "message",
        "phonetic": "/ˈmesɪdʒ/",
        "meaning": "n. 消息，留言",
        "example": "Can I leave a message?",
    },
    {
        "word": "minute",
        "phonetic": "/ˈmɪnɪt/",
        "meaning": "n. 分钟",
        "example": "Wait for a minute, please.",
    },
    {
        "word": "modern",
        "phonetic": "/ˈmɒdn/",
        "meaning": "adj. 现代的，时髦的",
        "example": "This is a modern city.",
    },
    {
        "word": "mountain",
        "phonetic": "/ˈmaʊntən/",
        "meaning": "n. 山，山脉",
        "example": "They climbed the high mountain.",
    },
    {
        "word": "museum",
        "phonetic": "/mjuˈziːəm/",
        "meaning": "n. 博物馆",
        "example": "We visited the science museum.",
    },
    {
        "word": "natural",
        "phonetic": "/ˈnætʃrəl/",
        "meaning": "adj. 自然的",
        "example": "Enjoy the natural beauty.",
    },
    {
        "word": "necessary",
        "phonetic": "/ˈnesəsəri/",
        "meaning": "adj. 必要的，必需的",
        "example": "Water is necessary for life.",
    },
    {
        "word": "notice",
        "phonetic": "/ˈnəʊtɪs/",
        "meaning": "n./v. 通知，注意",
        "example": "Did you notice the sign?",
    },
    {
        "word": "ocean",
        "phonetic": "/ˈəʊʃn/",
        "meaning": "n. 海洋",
        "example": "Whales live in the ocean.",
    },
    {
        "word": "office",
        "phonetic": "/ˈɒfɪs/",
        "meaning": "n. 办公室",
        "example": "My dad works in an office.",
    },
    {
        "word": "often",
        "phonetic": "/ˈɒfn/",
        "meaning": "adv. 经常",
        "example": "I often play basketball.",
    },
    {
        "word": "opposite",
        "phonetic": "/ˈɒpəzɪt/",
        "meaning": "prep./adj. 在……对面",
        "example": "He lives opposite my house.",
    },
    {
        "word": "outside",
        "phonetic": "/ˌaʊtˈsaɪd/",
        "meaning": "prep./adv. 在……外面",
        "example": "It is raining outside.",
    },
    {
        "word": "packet",
        "phonetic": "/ˈpækɪt/",
        "meaning": "n. 小包，小袋",
        "example": "A packet of sweets.",
    },
    {
        "word": "passenger",
        "phonetic": "/ˈpæsɪndʒə(r)/",
        "meaning": "n. 乘客，旅客",
        "example": "Be a polite passenger on the bus.",
    },
    {
        "word": "patience",
        "phonetic": "/ˈpeɪʃns/",
        "meaning": "n. 耐心，毅力",
        "example": "Learning needs patience.",
    },
    {
        "word": "peaceful",
        "phonetic": "/ˈpiːsfl/",
        "meaning": "adj. 和平的，平静的",
        "example": "It is a peaceful village.",
    },
    {
        "word": "perfect",
        "phonetic": "/ˈpɜːfɪkt/",
        "meaning": "adj. 完美的，极好的",
        "example": "Today is a perfect day.",
    },
    {
        "word": "planet",
        "phonetic": "/ˈplænɪt/",
        "meaning": "n. 行星",
        "example": "Earth is a blue planet.",
    },
    {
        "word": "pleasure",
        "phonetic": "/ˈpleʒə(r)/",
        "meaning": "n. 高兴，荣幸",
        "example": "It's my pleasure.",
    },
    {
        "word": "popular",
        "phonetic": "/ˈpɒpjələ(r)/",
        "meaning": "adj. 受欢迎的，流行的",
        "example": "Football is a popular sport.",
    },
    {
        "word": "practice",
        "phonetic": "/ˈpræktɪs/",
        "meaning": "v./n. 练习，实践",
        "example": "Practice speaking English every day.",
    },
]


def get_audio_bytes(text):
  tts = gTTS(text=text, lang="en")
  fp = BytesIO()
  tts.write_to_fp(fp)
  fp.seek(0)
  return fp.read()


st.title("📖 小学五年级英语背单词训练营")

if "queue" not in st.session_state:
  st.session_state.queue = list(VOCAB_LIST)
  random.shuffle(st.session_state.queue)

total_count = len(VOCAB_LIST)
remaining_count = len(st.session_state.queue)
st.progress((total_count - remaining_count) / total_count)
st.write(f"📊 总词汇量：{total_count} 个 | 剩余待复习：{remaining_count} 个")

if st.session_state.queue:
  current = st.session_state.queue[0]

  with st.container():
    st.markdown(f"## **{current['word']}**")
    # 生成并播放声音按钮
    audio_bytes = get_audio_bytes(current["word"])
    st.audio(audio_bytes, format="audio/mp3")

    st.write(f"🔊 **音标**：`{current['phonetic']}`")
    st.write(f"💡 **释义**：**{current['meaning']}**")
    st.info(f"📝 **例句**：{current['example']}")

  col1, col2 = st.columns(2)
  with col1:
    if st.button("❌ 模糊 (放回队列重练)", use_container_width=True):
      st.session_state.queue.append(st.session_state.queue.pop(0))
      st.rerun()
  with col2:
    if st.button("✔ 认识 (下一个)", use_container_width=True):
      st.session_state.queue.pop(0)
      st.rerun()
else:
  st.success("🎉 太棒了！这 100 个五年级单词你已经全部顺利复习完了！")
  if st.button("🔄 重新开始新一轮背诵", use_container_width=True):
    st.session_state.queue = list(VOCAB_LIST)
    random.shuffle(st.session_state.queue)
    st.rerun()
        random.shuffle(st.session_state.queue)
        st.rerun()
