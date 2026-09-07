from io import BytesIO
import random
from gtts import gTTS
import streamlit as st

# 100个小学五年级核心英语单词库（统一使用 example_en 和 example_cn 字段）
VOCAB_LIST = [
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
    {
        "word": "breakfast",
        "phonetic": "/ˈbrekfəst/",
        "meaning": "n. 早餐",
        "example_en": "I eat eggs for breakfast.",
        "example_cn": "我早餐吃鸡蛋。",
    },
    {
        "word": "bring",
        "phonetic": "/brɪŋ/",
        "meaning": "v. 带来，拿来",
        "example_en": "Bring your homework tomorrow.",
        "example_cn": "明天把你的作业带来。",
    },
    {
        "word": "building",
        "phonetic": "/ˈbɪldɪŋ/",
        "meaning": "n. 建筑物，房子",
        "example_en": "This is a tall building.",
        "example_cn": "这是一栋高楼。",
    },
    {
        "word": "busy",
        "phonetic": "/ˈbɪzi/",
        "meaning": "adj. 忙碌的",
        "example_en": "My mother is busy cooking.",
        "example_cn": "我妈妈正忙着做饭。",
    },
    {
        "word": "careful",
        "phonetic": "/ˈkeəfl/",
        "meaning": "adj. 小心的，仔细的",
        "example_en": "Be careful when you cross the road.",
        "example_cn": "过马路时要小心。",
    },
    {
        "word": "catch",
        "phonetic": "/kætʃ/",
        "meaning": "v. 抓住，接住",
        "example_en": "Catch the ball, please.",
        "example_cn": "请接住球。",
    },
    {
        "word": "center",
        "phonetic": "/ˈsentə(r)/",
        "meaning": "n. 中心，中央",
        "example_en": "It is in the city center.",
        "example_cn": "它在市中心。",
    },
    {
        "word": "change",
        "phonetic": "/tʃeɪndʒ/",
        "meaning": "v./n. 改变，变化",
        "example_en": "Leaves change color in autumn.",
        "example_cn": "树叶在秋天变色。",
    },
    {
        "word": "cheap",
        "phonetic": "/tʃiːp/",
        "meaning": "adj. 便宜的",
        "example_en": "This book is cheap.",
        "example_cn": "这本书很便宜。",
    },
    {
        "word": "choose",
        "phonetic": "/tʃuːz/",
        "meaning": "v. 选择，挑选",
        "example_en": "Choose a gift you like.",
        "example_cn": "选择一个你喜欢的礼物。",
    },
    {
        "word": "climb",
        "phonetic": "/klaɪm/",
        "meaning": "v. 爬，攀登",
        "example_en": "We like to climb mountains.",
        "example_cn": "我们喜欢爬山。",
    },
    {
        "word": "cloudy",
        "phonetic": "/ˈklaʊdi/",
        "meaning": "adj. 多云的",
        "example_en": "It is cloudy today.",
        "example_cn": "今天多云。",
    },
    {
        "word": "collect",
        "phonetic": "/kəˈlekt/",
        "meaning": "v. 收集，搜集",
        "example_en": "I like to collect stamps.",
        "example_cn": "我喜欢集邮。",
    },
    {
        "word": "comfortable",
        "phonetic": "/ˈkʌmfətəbl/",
        "meaning": "adj. 舒适的，舒服的",
        "example_en": "This bed is very comfortable.",
        "example_cn": "这张床非常舒服。",
    },
    {
        "word": "concert",
        "phonetic": "/ˈkɒnsət/",
        "meaning": "n. 音乐会",
        "example_en": "We went to a music concert.",
        "example_cn": "我们去听了一场音乐会。",
    },
    {
        "word": "cool",
        "phonetic": "/kuːl/",
        "meaning": "adj. 凉爽的，酷的",
        "example_en": "The weather is cool today.",
        "example_cn": "今天天气很凉爽。",
    },
    {
        "word": "country",
        "phonetic": "/ˈkʌntri/",
        "meaning": "n. 国家，乡村",
        "example_en": "China is a great country.",
        "example_cn": "中国是一个伟大的国家。",
    },
    {
        "word": "dangerous",
        "phonetic": "/ˈdeɪndʒərəs/",
        "meaning": "adj. 危险的",
        "example_en": "Fire is dangerous.",
        "example_cn": "火是危险的。",
    },
    {
        "word": "decide",
        "phonetic": "/dɪˈsaɪd/",
        "meaning": "v. 决定，下决心",
        "example_en": "Decide what to do next.",
        "example_cn": "决定下一步做什么。",
    },
    {
        "word": "different",
        "phonetic": "/ˈdɪfrənt/",
        "meaning": "adj. 不同的",
        "example_en": "We have different hobbies.",
        "example_cn": "我们有不同的爱好。",
    },
    {
        "word": "difficult",
        "phonetic": "/ˈdɪfɪkəlt/",
        "meaning": "adj. 困难的",
        "example_en": "Math can be difficult sometimes.",
        "example_cn": "数学有时会很难。",
    },
    {
        "word": "direction",
        "phonetic": "/dəˈrekʃn/",
        "meaning": "n. 方向，说明",
        "example_en": "Which direction should we go?",
        "example_cn": "我们应该走哪个方向？",
    },
    {
        "word": "discover",
        "phonetic": "/dɪˈskʌvə(r)/",
        "meaning": "v. 发现",
        "example_en": "Columbus discovered new lands.",
        "example_cn": "哥伦布发现了新大陆。",
    },
    {
        "word": "drive",
        "phonetic": "/draɪv/",
        "meaning": "v. 驾驶，开车",
        "example_en": "My father can drive a car.",
        "example_cn": "我爸爸会开车。",
    },
    {
        "word": "early",
        "phonetic": "/ˈɜːli/",
        "meaning": "adj./adv. 早的（地）",
        "example_en": "Get up early in the morning.",
        "example_cn": "早上早点起床。",
    },
    {
        "word": "earth",
        "phonetic": "/ɜːθ/",
        "meaning": "n. 地球，泥土",
        "example_en": "We live on the earth.",
        "example_cn": "我们住在地球上。",
    },
    {
        "word": "easily",
        "phonetic": "/ˈiːzɪli/",
        "meaning": "adv. 容易地",
        "example_en": "She can speak English easily.",
        "example_cn": "她能轻松地说英语。",
    },
    {
        "word": "energy",
        "phonetic": "/ˈenədʒi/",
        "meaning": "n. 能量，精力",
        "example_en": "Children have much energy.",
        "example_cn": "孩子们精力充沛。",
    },
    {
        "word": "environment",
        "phonetic": "/ɪnˈvaɪrənmənt/",
        "meaning": "n. 环境",
        "example_en": "Protect our environment.",
        "example_cn": "保护我们的环境。",
    },
    {
        "word": "example",
        "phonetic": "/ɪɡˈzɑːmpl/",
        "meaning": "n. 例子，榜样",
        "example_en": "Let me give you an example.",
        "example_cn": "让我给你举个例子。",
    },
    {
        "word": "exciting",
        "phonetic": "/ɪkˈsaɪtɪŋ/",
        "meaning": "adj. 令人兴奋的",
        "example_en": "The football match is exciting.",
        "example_cn": "这场足球赛令人兴奋。",
    },
    {
        "word": "expensive",
        "phonetic": "/ɪkˈspensɪv/",
        "meaning": "adj. 昂贵的",
        "example_en": "The watch is too expensive.",
        "example_cn": "这块手表太贵了。",
    },
    {
        "word": "experiment",
        "phonetic": "/ɪkˈsperɪmənt/",
        "meaning": "n./v. 实验",
        "example_en": "We do a science experiment.",
        "example_cn": "我们做一个科学实验。",
    },
    {
        "word": "famous",
        "phonetic": "/ˈfeɪməs/",
        "meaning": "adj. 著名的",
        "example_en": "Beijing is a famous city.",
        "example_cn": "北京是一个著名的城市。",
    },
    {
        "word": "favourite",
        "phonetic": "/ˈfeɪvərɪt/",
        "meaning": "adj./n. 特别喜爱的",
        "example_en": "Blue is my favourite color.",
        "example_cn": "蓝色是我最喜欢的颜色。",
    },
    {
        "word": "feel",
        "phonetic": "/fiːl/",
        "meaning": "v. 觉得，感到",
        "example_en": "I feel happy today.",
        "example_cn": "我今天感觉很高兴。",
    },
    {
        "word": "festival",
        "phonetic": "/ˈfestɪvl/",
        "meaning": "n. 节日",
        "example_en": "Spring Festival is joyful.",
        "example_cn": "春节是快乐的。",
    },
    {
        "word": "finish",
        "phonetic": "/ˈfɪnɪʃ/",
        "meaning": "v. 完成，结束",
        "example_en": "Finish your homework first.",
        "example_cn": "先完成你的作业。",
    },
    {
        "word": "foreign",
        "phonetic": "/ˈfɒrən/",
        "meaning": "adj. 外国的",
        "example_en": "I want to learn a foreign language.",
        "example_cn": "我想学一门外语。",
    },
    {
        "word": "forest",
        "phonetic": "/ˈfɒrɪst/",
        "meaning": "n. 森林",
        "example_en": "Many animals live in the forest.",
        "example_cn": "许多动物住在森林里。",
    },
    {
        "word": "forget",
        "phonetic": "/fəˈɡet/",
        "meaning": "v. 忘记",
        "example_en": "Don't forget your umbrella.",
        "example_cn": "别忘带你的伞。",
    },
    {
        "word": "friendly",
        "phonetic": "/ˈfrendli/",
        "meaning": "adj. 友好的",
        "example_en": "Our teachers are very friendly.",
        "example_cn": "我们的老师非常友好。",
    },
    {
        "word": "future",
        "phonetic": "/ˈfjuːtʃə(r)/",
        "meaning": "n. 未来",
        "example_en": "What will you be in the future?",
        "example_cn": "你将来想成为什么？",
    },
    {
        "word": "garden",
        "phonetic": "/ˈɡɑːdn/",
        "meaning": "n. 花园",
        "example_en": "There are flowers in the garden.",
        "example_cn": "花园里有花。",
    },
    {
        "word": "gentle",
        "phonetic": "/ˈdʒentl/",
        "meaning": "adj. 温柔的，温和的",
        "example_en": "She has a gentle voice.",
        "example_cn": "她有一个温柔的声音。",
    },
    {
        "word": "global",
        "phonetic": "/ˈɡləʊbl/",
        "meaning": "adj. 全球的",
        "example_en": "It is a global village.",
        "example_cn": "这是一个地球村。",
    },
    {
        "word": "grade",
        "phonetic": "/ɡreɪd/",
        "meaning": "n. 年级，成绩",
        "example_en": "I am in Grade Five.",
        "example_cn": "我在五年级。",
    },
    {
        "word": "group",
        "phonetic": "/ɡruːp/",
        "meaning": "n. 群，组",
        "example_en": "Work in groups, please.",
        "example_cn": "请分组合作。",
    },
    {
        "word": "habit",
        "phonetic": "/ˈhæbɪt/",
        "meaning": "n. 习惯",
        "example_en": "Reading is a good habit.",
        "example_cn": "读书是个好习惯。",
    },
    {
        "word": "happily",
        "phonetic": "/ˈhæpɪli/",
        "meaning": "adv. 快乐地，高兴地",
        "example_en": "They live happily together.",
        "example_cn": "他们快乐地生活在一起。",
    },
    {
        "word": "healthy",
        "phonetic": "/ˈhelθi/",
        "meaning": "adj. 健康的",
        "example_en": "Eat fruit to stay healthy.",
        "example_cn": "吃水果保持健康。",
    },
    {
        "word": "history",
        "phonetic": "/ˈhɪstəri/",
        "meaning": "n. 历史",
        "example_en": "I like reading history books.",
        "example_cn": "我喜欢读历史书。",
    },
    {
        "word": "holiday",
        "phonetic": "/ˈhɒlədeɪ/",
        "meaning": "n. 节日，假期",
        "example_en": "Where will you go for the holiday?",
        "example_cn": "假期你要去哪里？",
    },
    {
        "word": "important",
        "phonetic": "/ɪmˈpɔːtnt/",
        "meaning": "adj. 重要的",
        "example_en": "English is an important language.",
        "example_cn": "英语是一门重要的语言。",
    },
    {
        "word": "improve",
        "phonetic": "/ɪmˈpruːv/",
        "meaning": "v. 改进，改善",
        "example_en": "Practice helps improve your skills.",
        "example_cn": "练习有助于提高你的技能。",
    },
    {
        "word": "information",
        "phonetic": "/ˌɪnfəˈmeɪʃn/",
        "meaning": "n. 信息，资料",
        "example_en": "Search for more information.",
        "example_cn": "搜索更多信息。",
    },
    {
        "word": "interested",
        "phonetic": "/ˈɪntrəstɪd/",
        "meaning": "adj. 感兴趣的",
        "example_en": "I am interested in science.",
        "example_cn": "我对科学感兴趣。",
    },
    {
        "word": "invent",
        "phonetic": "/ɪnˈvent/",
        "meaning": "v. 发明，创造",
        "example_en": "Who invented the light bulb?",
        "example_cn": "谁发明了电灯泡？",
    },
    {
        "word": "journey",
        "phonetic": "/ˈdʒɜːni/",
        "meaning": "n. 旅行，旅程",
        "example_en": "Have a safe journey home.",
        "example_cn": "祝你一路平安回家。",
    },
    {
        "word": "knowledge",
        "phonetic": "/ˈnɒlɪdʒ/",
        "meaning": "n. 知识，学问",
        "example_en": "Books give us knowledge.",
        "example_cn": "书籍给我们知识。",
    },
    {
        "word": "language",
        "phonetic": "/ˈlæŋɡwɪdʒ/",
        "meaning": "n. 语言",
        "example_en": "English is a global language.",
        "example_cn": "英语是一门全球语言。",
    },
    {
        "word": "laugh",
        "phonetic": "/lɑːf/",
        "meaning": "v./n. 笑，大笑",
        "example_en": "Do not laugh at others.",
        "example_cn": "不要嘲笑别人。",
    },
    {
        "word": "learn",
        "phonetic": "/lɜːn/",
        "meaning": "v. 学习，学会",
        "example_en": "Learn new words every day.",
        "example_cn": "每天学习新单词。",
    },
    {
        "word": "library",
        "phonetic": "/ˈlaɪbrəri/",
        "meaning": "n. 图书馆",
        "example_en": "We read books in the library.",
        "example_cn": "我们在图书馆看书。",
    },
    {
        "word": "listen",
        "phonetic": "/ˈlɪsn/",
        "meaning": "v. 听",
        "example_en": "Listen to the teacher carefully.",
        "example_cn": "认真听老师讲课。",
    },
    {
        "word": "lovely",
        "phonetic": "/ˈlʌvli/",
        "meaning": "adj. 可爱的，美丽的",
        "example_en": "What a lovely day!",
        "example_cn": "多美好的一天啊！",
    },
    {
        "word": "machine",
        "phonetic": "/məˈʃiːn/",
        "meaning": "n. 机器",
        "example_en": "This is a washing machine.",
        "example_cn": "这是一台洗衣机。",
    },
    {
        "word": "market",
        "phonetic": "/ˈmɑːkɪt/",
        "meaning": "n. 市场，集市",
        "example_en": "Mom buys fruit at the market.",
        "example_cn": "妈妈在市场买水果。",
    },
    {
        "word": "message",
        "phonetic": "/ˈmesɪdʒ/",
        "meaning": "n. 消息，留言",
        "example_en": "Can I leave a message?",
        "example_cn": "我可以留言吗？",
    },
    {
        "word": "minute",
        "phonetic": "/ˈmɪnɪt/",
        "meaning": "n. 分钟",
        "example_en": "Wait for a minute, please.",
        "example_cn": "请等一会儿。",
    },
    {
        "word": "modern",
        "phonetic": "/ˈmɒdn/",
        "meaning": "adj. 现代的，时髦的",
        "example_en": "This is a modern city.",
        "example_cn": "这是一个现代化的城市。",
    },
    {
        "word": "mountain",
        "phonetic": "/ˈmaʊntən/",
        "meaning": "n. 山，山脉",
        "example_en": "They climbed the high mountain.",
        "example_cn": "他们爬上了高山。",
    },
    {
        "word": "museum",
        "phonetic": "/mjuˈziːəm/",
        "meaning": "n. 博物馆",
        "example_en": "We visited the science museum.",
        "example_cn": "我们参观了科学博物馆。",
    },
    {
        "word": "natural",
        "phonetic": "/ˈnætʃrəl/",
        "meaning": "adj. 自然的",
        "example_en": "Enjoy the natural beauty.",
        "example_cn": "享受自然美景。",
    },
    {
        "word": "necessary",
        "phonetic": "/ˈnesəsəri/",
        "meaning": "adj. 必要的，必需的",
        "example_en": "Water is necessary for life.",
        "example_cn": "水对生命是必需的。",
    },
    {
        "word": "notice",
        "phonetic": "/ˈnəʊtɪs/",
        "meaning": "n./v. 通知，注意",
        "example_en": "Did you notice the sign?",
        "example_cn": "你注意到那个标志了吗？",
    },
    {
        "word": "ocean",
        "phonetic": "/ˈəʊʃn/",
        "meaning": "n. 海洋",
        "example_en": "Whales live in the ocean.",
        "example_cn": "鲸鱼生活在海洋里。",
    },
    {
        "word": "office",
        "phonetic": "/ˈɒfɪs/",
        "meaning": "n. 办公室",
        "example_en": "My dad works in an office.",
        "example_cn": "我爸爸在办公室工作。",
    },
    {
        "word": "often",
        "phonetic": "/ˈɒfn/",
        "meaning": "adv. 经常",
        "example_en": "I often play basketball.",
        "example_cn": "我经常打篮球。",
    },
    {
        "word": "opposite",
        "phonetic": "/ˈɒpəzɪt/",
        "meaning": "prep./adj. 在……对面",
        "example_en": "He lives opposite my house.",
        "example_cn": "他住在我的房子对面。",
    },
    {
        "word": "outside",
        "phonetic": "/ˌaʊtˈsaɪd/",
        "meaning": "prep./adv. 在……外面",
        "example_en": "It is raining outside.",
        "example_cn": "外面在下雨。",
    },
    {
        "word": "packet",
        "phonetic": "/ˈpækɪt/",
        "meaning": "n. 小包，小袋",
        "example_en": "A packet of sweets.",
        "example_cn": "一包糖果。",
    },
    {
        "word": "passenger",
        "phonetic": "/ˈpæsɪndʒə(r)/",
        "meaning": "n. 乘客，旅客",
        "example_en": "Be a polite passenger on the bus.",
        "example_cn": "做公交车上一个有礼貌的乘客。",
    },
    {
        "word": "patience",
        "phonetic": "/ˈpeɪʃns/",
        "meaning": "n. 耐心，毅力",
        "example_en": "Learning needs patience.",
        "example_cn": "学习需要耐心。",
    },
    {
        "word": "peaceful",
        "phonetic": "/ˈpiːsfl/",
        "meaning": "adj. 和平的，平静的",
        "example_en": "It is a peaceful village.",
        "example_cn": "这是一个宁静的村庄。",
    },
    {
        "word": "perfect",
        "phonetic": "/ˈpɜːfɪkt/",
        "meaning": "adj. 完美的，极好的",
        "example_en": "Today is a perfect day.",
        "example_cn": "今天是个完美的一天。",
    },
    {
        "word": "planet",
        "phonetic": "/ˈplænɪt/",
        "meaning": "n. 行星",
        "example_en": "Earth is a blue planet.",
        "example_cn": "地球是一个蓝色的星球。",
    },
    {
        "word": "pleasure",
        "phonetic": "/ˈpleʒə(r)/",
        "meaning": "n. 高兴，荣幸",
        "example_en": "It's my pleasure.",
        "example_cn": "我的荣幸。",
    },
    {
        "word": "popular",
        "phonetic": "/ˈpɒpjələ(r)/",
        "meaning": "adj. 受欢迎的，流行的",
        "example_en": "Football is a popular sport.",
        "example_cn": "足球是一项受欢迎的运动。",
    },
    {
        "word": "practice",
        "phonetic": "/ˈpræktɪs/",
        "meaning": "v./n. 练习，实践",
        "example_en": "Practice speaking English every day.",
        "example_cn": "每天练习说英语。",
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

    # 单词发音
    word_audio = get_audio_bytes(current["word"])
    st.audio(word_audio, format="audio/mp3")

    st.write(f"🔊 **音标**：`{current['phonetic']}`")
    st.write(f"💡 **释义**：**{current['meaning']}**")

    # 例句与翻译
    st.info(
        f"📝 **例句**：{current['example_en']}\n\n🏷️ **翻译**："
        f" {current['example_cn']}"
    )

    if st.button("🔊 朗读例句"):
      example_audio = get_audio_bytes(current["example_en"])
      st.audio(example_audio, format="audio/mp3", autoplay=True)

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
