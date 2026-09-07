from io import BytesIO
import random
from gtts import gTTS
import streamlit as st
import streamlit.components.v1 as components

# 五年级单词库 (100个精选)
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

# 六年级升级单词库
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
    {
        "word": "delicious",
        "phonetic": "/dɪˈlɪʃəs/",
        "meaning": "adj. 美味的，可口的",
        "example_en": "Mom cooked a delicious dinner.",
        "example_cn": "妈妈做了一顿美味的晚餐。",
    },
    {
        "word": "digital",
        "phonetic": "/ˈdɪdʒɪtl/",
        "meaning": "adj. 数码的，数字的",
        "example_en": "We live in a digital age.",
        "example_cn": "我们生活在一个数字时代。",
    },
    {
        "word": "efficient",
        "phonetic": "/ɪˈfɪʃnt/",
        "meaning": "adj. 效率高的",
        "example_en": "An efficient way to study.",
        "example_cn": "一种高效的学习方法。",
    },
    {
        "word": "encourage",
        "phonetic": "/ɪnˈkʌrɪdʒ/",
        "meaning": "v. 鼓励，激励",
        "example_en": "Parents encourage their children.",
        "example_cn": "父母鼓励他们的孩子。",
    },
    {
        "word": "flexible",
        "phonetic": "/ˈfleksəbl/",
        "meaning": "adj. 灵活的",
        "example_en": "We have a flexible schedule.",
        "example_cn": "我们的时间表很灵活。",
    },
    {
        "word": "generation",
        "phonetic": "/ˌdʒenəˈreɪʃn/",
        "meaning": "n. 一代人",
        "example_en": "Understand the younger generation.",
        "example_cn": "理解年轻一代。",
    },
    {
        "word": "grateful",
        "phonetic": "/ˈɡreɪtfl/",
        "meaning": "adj. 感恩的，感激的",
        "example_en": "I am grateful for your help.",
        "example_cn": "我很感激你的帮助。",
    },
    {
        "word": "independent",
        "phonetic": "/ˌɪndɪˈpendənt/",
        "meaning": "adj. 独立的",
        "example_en": "Learn to be an independent person.",
        "example_cn": "学会做一个独立的人。",
    },
    {
        "word": "inspire",
        "phonetic": "/ɪnˈspaɪə(r)/",
        "meaning": "v. 启发，鼓舞",
        "example_en": "The teacher inspires students.",
        "example_cn": "老师鼓舞了学生们。",
    },
    {
        "word": "manage",
        "phonetic": "/ˈmænɪdʒ/",
        "meaning": "v. 管理，经营",
        "example_en": "Manage your time wisely.",
        "example_cn": "明智地管理你的时间。",
    },
    {
        "word": "opportunity",
        "phonetic": "/ˌɒpəˈtjuːnəti/",
        "meaning": "n. 机会，机遇",
        "example_en": "Grab every opportunity to learn.",
        "example_cn": "抓住每一个学习的机会。",
    },
    {
        "word": "positive",
        "phonetic": "/ˈpɒzətɪv/",
        "meaning": "adj. 积极的，乐观的",
        "example_en": "Keep a positive attitude.",
        "example_cn": "保持乐观的态度。",
    },
    {
        "word": "prepare",
        "phonetic": "/prɪˈpeə(r)/",
        "meaning": "v. 准备，预备",
        "example_en": "Prepare for the exam carefully.",
        "example_cn": "认真准备考试。",
    },
    {
        "word": "reliable",
        "phonetic": "/rɪˈlaɪəbl/",
        "meaning": "adj. 可靠的，可信赖的",
        "example_en": "He is a reliable friend.",
        "example_cn": "他是个可靠的朋友。",
    },
    {
        "word": "successful",
        "phonetic": "/səkˈsesfl/",
        "meaning": "adj. 成功的",
        "example_en": "Hard work leads to a successful life.",
        "example_cn": "努力工作带来成功的生活。",
    },
]


def get_audio_bytes(text):
  tts = gTTS(text=text, lang="en")
  fp = BytesIO()
  tts.write_to_fp(fp)
  fp.seek(0)
  return fp.read()


# 页面设置
st.set_page_config(page_title="背单词与小测应用", page_icon="📖", layout="centered")

# 初始化 Session State
if "grade" not in st.session_state:
  st.session_state.grade = 5
if "queue_g5" not in st.session_state:
  st.session_state.queue_g5 = list(VOCAB_GRADE_5)
  random.shuffle(st.session_state.queue_g5)
if "mastered_g5" not in st.session_state:
  st.session_state.mastered_g5 = []
if "queue_g6" not in st.session_state:
  st.session_state.queue_g6 = list(VOCAB_GRADE_6)
  random.shuffle(st.session_state.queue_g6)
if "mastered_g6" not in st.session_state:
  st.session_state.mastered_g6 = []
if "mode" not in st.session_state:
  st.session_state.mode = "study"

# 侧边栏菜单
st.sidebar.title("📌 导航菜单")
if st.sidebar.button("📚 背单词与AI跟读模式", use_container_width=True):
  st.session_state.mode = "study"
  st.rerun()

if st.sidebar.button("🎯 已学单词小测验", use_container_width=True):
  st.session_state.mode = "quiz"
  st.rerun()

if st.sidebar.button("🔁 已学单词重温", use_container_width=True):
  st.session_state.mode = "review"
  st.rerun()

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
# 1. 小测验面板 (先显示英文+选项，答题后展示P2卡片详情并自动发音)
# ==========================================
if st.session_state.mode == "quiz":
  st.markdown("### 🎯 已学单词小测验")

  if not all_learned_pool:
    st.info("当前还没有学过任何单词，请先去背诵页面学习！")
  else:
    if "quiz_current" not in st.session_state:
      q_item = random.choice(all_learned_pool)
      st.session_state.quiz_current = q_item
      wrong_meanings = [
          v["meaning"]
          for v in VOCAB_GRADE_5 + VOCAB_GRADE_6
          if v["meaning"] != q_item["meaning"]
      ]
      distractors = random.sample(wrong_meanings, min(3, len(wrong_meanings)))
      options = distractors + [q_item["meaning"]]
      random.shuffle(options)
      st.session_state.quiz_options = options
      st.session_state.quiz_answered = False
      st.session_state.selected_option = None

    qc = st.session_state.quiz_current
    opts = st.session_state.quiz_options

    # 1. 顶部先展示英文单词与发音音频
    audio_bytes = get_audio_bytes(qc["word"])
    st.audio(audio_bytes, format="audio/mp3")

    st.markdown(
        f"""
        <div style="background-color: #f7f9fa; border: 1px solid #dcdfe6; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px;">
            <div style="font-size: 38px; font-weight: bold; color: #303133; margin-bottom: 5px;">
                {qc['word']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("请选择正确的中文释义：")

    col_a, col_b = st.columns(2)
    labels = ["A", "B", "C", "D"]

    for idx, opt in enumerate(opts):
      current_col = col_a if idx % 2 == 0 else col_b
      with current_col:
        btn_label = f"{labels[idx]}. {opt}"
        if st.button(btn_label, use_container_width=True, key=f"opt_{idx}"):
          st.session_state.quiz_answered = True
          st.session_state.selected_option = opt

    # 2. 只有当用户点击选项回答后，才显示详细的 P2 卡片并自动朗读
    if st.session_state.get("quiz_answered", False):
      selected = st.session_state.selected_option

      # 自动读出单词
      st.audio(audio_bytes, format="audio/mp3", autoplay=True)

      if selected == qc["meaning"]:
        st.success("✅ 回答正确！太棒了！")
      else:
        st.error(f"❌ 回答错误。正确答案是：{qc['meaning']}")

      # 渲染完整的 P2 卡片详情
      st.markdown(
          f"""
            <div style="background-color: #f7f9fa; border: 1px solid #dcdfe6; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-top: 20px; margin-bottom: 20px;">
                <div style="display: flex; align-items: center; margin-bottom: 15px;">
                    <span style="background-color: #52c41a; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 14px; margin-right: 12px;">Lv.{st.session_state.grade} 核心</span>
                    <span style="color: #606266; font-size: 16px; font-weight: 500;">{qc['phonetic']}</span>
                </div>
                <div style="font-size: 36px; font-weight: bold; color: #303133; margin-bottom: 10px;">
                    {qc['word']}
                </div>
                <div style="font-size: 22px; color: #606266; margin-bottom: 20px; font-weight: 600;">
                    {qc['meaning']}
                </div>
                <hr style="border: none; border-top: 1px solid #e4e7ed; margin: 15px 0;">
                <div style="font-size: 15px; color: #606266; font-style: italic;">
                    📝 <b>例句：</b>{qc['example_en']} / {qc['example_cn']}
                </div>
            </div>
            """,
          unsafe_allow_html=True,
      )

      if st.button("➡️ 下一题", use_container_width=True):
        q_item = random.choice(all_learned_pool)
        st.session_state.quiz_current = q_item
        wrong_meanings = [
            v["meaning"]
            for v in VOCAB_GRADE_5 + VOCAB_GRADE_6
            if v["meaning"] != q_item["meaning"]
        ]
        distractors = random.sample(wrong_meanings, min(3, len(wrong_meanings)))
        options = distractors + [q_item["meaning"]]
        random.shuffle(options)
        st.session_state.quiz_options = options
        st.session_state.quiz_answered = False
        st.session_state.selected_option = None
        st.rerun()

# ==========================================
# 2. 已学单词重温面板
# ==========================================
elif st.session_state.mode == "review":
  st.subheader("🔁 已掌握单词重温大本营")
  if not mastered_list:
    st.info("你还没有完全掌握任何单词哦！先去“背单词模式”攻克单词吧。")
  else:
    if "review_current" not in st.session_state:
      st.session_state.review_current = random.choice(mastered_list)

    rc = st.session_state.review_current
    with st.container():
      st.markdown(f"## **{rc['word']}** (已掌握复习)")
      st.audio(get_audio_bytes(rc["word"]), format="audio/mp3")

      st.write(f"🔊 **音标**：`{rc['phonetic']}`")
      st.write(f"💡 **释义**：**{rc['meaning']}**")
      st.info(f"📝 **例句**：{rc['example_en']}\n\n🏷️ **翻译**：{rc['example_cn']}")

      if st.button("🔊 朗读例句"):
        st.audio(
            get_audio_bytes(rc["example_en"]), format="audio/mp3", autoplay=True
        )

    if st.button("➡️ 换一个复习", use_container_width=True):
      st.session_state.review_current = random.choice(mastered_list)
      st.rerun()

# ==========================================
# 3. 正常背诵与 AI 跟读模式
# ==========================================
else:
  if st.session_state.grade == 5:
    st.subheader("📖 小学五年级核心单词闯关")
  else:
    st.subheader("🚀 小学六年级进阶生活/日常英语单词闯关")

  if current_queue:
    current = current_queue[0]

    with st.container():
      st.markdown(f"## **{current['word']}**")
      st.audio(get_audio_bytes(current["word"]), format="audio/mp3")

      st.write(f"🔊 **音标**：`{current['phonetic']}`")
      st.write(f"💡 **释义**：**{current['meaning']}**")
      st.info(
          f"📝 **例句**：{current['example_en']}\n\n🏷️ **翻译**："
          f" {current['example_cn']}"
      )

      if st.button("🔊 朗读例句"):
        st.audio(
            get_audio_bytes(current["example_en"]),
            format="audio/mp3",
            autoplay=True,
        )

      # ---------------------------------------------------------
      # 🎤 AI 语音跟读测评模块
      # ---------------------------------------------------------
      st.markdown("---")
      st.markdown("#### 🎙️ AI 语音跟读评测")
      st.write(
          "点击下方按钮并对着麦克风大声读出上方单词，AI 会立即检测你的发音！"
      )

      target_word_lower = current["word"].lower()

      speech_component_html = (
          """
            <div style="font-family: sans-serif; text-align: center; padding: 10px;">
                <button id="recordBtn" style="background-color: #ff4b4b; color: white; border: none; padding: 10px 20px; font-size: 16px; border-radius: 8px; cursor: pointer;">🎙️ 点击开始说话跟读</button>
                <p id="statusText" style="margin-top: 10px; color: #555; font-size: 14px;"></p>
            </div>
            <script>
                const targetWord = "%s";
                const btn = document.getElementById('recordBtn');
                const statusText = document.getElementById('statusText');

                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (!SpeechRecognition) {
                    statusText.innerHTML = "❌ 你的浏览器不支持语音识别，请使用 Chrome 或手机自带浏览器。";
                    btn.disabled = true;
                } else {
                    const recognition = new SpeechRecognition();
                    recognition.lang = 'en-US';
                    recognition.interimResults = false;
                    recognition.maxAlternatives = 1;

                    btn.onclick = function() {
                        statusText.innerHTML = "👂 正在听你发音，请说话...";
                        btn.style.backgroundColor = "#ffa500";
                        recognition.start();
                    };

                    recognition.onresult = function(event) {
                        const speechResult = event.results[0][0].transcript.trim().toLowerCase();
                        const cleanResult = speechResult.replace(/[.,\/#!$%%^&*;:{}=\-_`~()]/g,"");
                        
                        if (cleanResult.includes(targetWord)) {
                            statusText.innerHTML = "✅ 识别成功！你读的是: <b>" + speechResult + "</b> 🎉 发音标准！";
                            btn.style.backgroundColor = "#28a745";
                        } else {
                            statusText.innerHTML = "❌ 识别结果为: <b>" + speechResult + "</b>，再试一次哦！";
                            btn.style.backgroundColor = "#dc3545";
                        }
                    };

                    recognition.onerror = function(event) {
                        statusText.innerHTML = "⚠️ 识别出错: " + event.error + "，请重试。";
                        btn.style.backgroundColor = "#ff4b4b";
                    };

                    recognition.onspeechend = function() {
                        recognition.stop();
                        btn.innerHTML = "🎙️ 再次跟读";
                    };
                }
            </script>
            """
          % target_word_lower
      )

      components.html(speech_component_html, height=120)

    col1, col2 = st.columns(2)
    with col1:
      if st.button("❌ 模糊 (放回队列重练)", use_container_width=True):
        current_queue.append(current_queue.pop(0))
        st.rerun()
    with col2:
      if st.button("✔ 认识 (下一个)", use_container_width=True):
        done_word = current_queue.pop(0)
        if done_word not in mastered_list:
          mastered_list.append(done_word)
        st.rerun()
  else:
    if st.session_state.grade == 5:
      st.success("🎉 太棒了！五年级单词已全部掌握，即将自动晋升到六年级！")
      if st.button("🚀 点击开始升入六年级生活单词", use_container_width=True):
        st.session_state.grade = 6
        st.rerun()
    else:
      st.success("🏆 恭喜你！六年级进阶日常词汇也已经全部通关大吉！")
      if st.button("🔄 重新复习全部课程", use_container_width=True):
        st.session_state.queue_g5 = list(VOCAB_GRADE_5)
        random.shuffle(st.session_state.queue_g5)
        st.session_state.queue_g6 = list(VOCAB_GRADE_6)
        random.shuffle(st.session_state.queue_g6)
        st.session_state.grade = 5
        st.rerun()
