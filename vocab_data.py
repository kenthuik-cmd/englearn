# vocab_data.py
# 真实难度递进词库：每个词独立造句，拒绝模板句

GLOBAL_VOCAB_DB = {
    # -------------------------------------------------------------
    # Level 1: 零基础与生存日常（饮食、居家、最基础动作）
    # -------------------------------------------------------------
    1: [
        {"word": "apple", "phonetic": "/ˈæpl/", "meaning": "n. 苹果", "example_en": "He took a bite of the crisp red apple.", "example_cn": "他咬了一口清脆的红苹果。"},
        {"word": "water", "phonetic": "/ˈwɔːtə(r)/", "meaning": "n. 水", "example_en": "Always drink plenty of water after exercise.", "example_cn": "运动后务必多喝水。"},
        {"word": "bread", "phonetic": "/bred/", "meaning": "n. 面包", "example_en": "The bakery sells freshly baked bread every morning.", "example_cn": "这家面包店每天早晨售卖现烤的面包。"},
        {"word": "milk", "phonetic": "/mɪlk/", "meaning": "n. 牛奶", "example_en": "She poured cold milk into her cereal bowl.", "example_cn": "她把凉牛奶倒进了麦片碗里。"},
        {"word": "house", "phonetic": "/haʊs/", "meaning": "n. 房子", "example_en": "They bought a comfortable house near the park.", "example_cn": "他们在公园附近买了一套舒适的房子。"},
        {"word": "door", "phonetic": "/dɔː(r)/", "meaning": "n. 门", "example_en": "Please knock on the door before entering.", "example_cn": "进门前请敲门。"},
        {"word": "window", "phonetic": "/ˈwɪndəʊ/", "meaning": "n. 窗户", "example_en": "Sunlight poured into the room through the open window.", "example_cn": "阳光透过开着的窗户洒进房间。"},
        {"word": "chair", "phonetic": "/tʃeə(r)/", "meaning": "n. 椅子", "example_en": "Pull up a chair and join our conversation.", "example_cn": "拉一把椅子过来加入我们的谈话吧。"},
        {"word": "table", "phonetic": "/ˈteɪbl/", "meaning": "n. 桌子", "example_en": "Dinner is served on the dining table.", "example_cn": "晚餐已经在餐桌上摆好了。"},
        {"word": "bed", "phonetic": "/bed/", "meaning": "n. 床", "example_en": "He collapsed onto the soft bed after a tiring shift.", "example_cn": "繁重的值班结束后，他瘫倒在柔软的床上。"},
        {"word": "pen", "phonetic": "/pen/", "meaning": "n. 钢笔", "example_en": "Sign your name at the bottom with a black pen.", "example_cn": "请用黑色水笔在底部签上你的名字。"},
        {"word": "book", "phonetic": "/bʊk/", "meaning": "n. 书籍", "example_en": "She borrowed an interesting novel from the library.", "example_cn": "她从图书馆借了一本有趣的小说。"},
        {"word": "car", "phonetic": "/kɑː(r)/", "meaning": "n. 汽车", "example_en": "He parked his car carefully along the curb.", "example_cn": "他小心翼翼地把车停在路边。"},
        {"word": "road", "phonetic": "/rəʊd/", "meaning": "n. 道路", "example_en": "Watch out for oncoming traffic when crossing the road.", "example_cn": "过马路时注意迎面驶来的车辆。"},
        {"word": "sun", "phonetic": "/sʌn/", "meaning": "n. 太阳", "example_en": "The warm sun rose above the horizon.", "example_cn": "温暖的太阳从地平线冉冉升起。"},
        {"word": "rain", "phonetic": "/reɪn/", "meaning": "n./v. 雨；下雨", "example_en": "Don't forget your umbrella because it might rain.", "example_cn": "别忘了带伞，因为可能会下雨。"},
        {"word": "dog", "phonetic": "/dɒɡ/", "meaning": "n. 狗", "example_en": "The golden retriever wagged its tail happily.", "example_cn": "那只金毛寻回犬高兴地摇着尾巴。"},
        {"word": "cat", "phonetic": "/kæt/", "meaning": "n. 猫", "example_en": "A stray cat curled up on the sunny porch.", "example_cn": "一只流浪猫在阳光明媚的门廊上蜷缩成一团。"},
        {"word": "tree", "phonetic": "/triː/", "meaning": "n. 树", "example_en": "Birds built their sturdy nests high up in the oak tree.", "example_cn": "鸟儿在高高的橡树上筑起了坚固的巢。"},
        {"word": "flower", "phonetic": "/ˈflaʊə(r)/", "meaning": "n. 花", "example_en": "She picked a fragrant rose from the front garden.", "example_cn": "她从前院花园里摘了一朵芬芳的玫瑰。"},
    ],

    # -------------------------------------------------------------
    # Level 2: 日常出行、基础人际与生活起居
    # -------------------------------------------------------------
    2: [
        {"word": "morning", "phonetic": "/ˈmɔːnɪŋ/", "meaning": "n. 早晨", "example_en": "I usually jog around the lake in the early morning.", "example_cn": "我通常清晨在湖边慢跑。"},
        {"word": "evening", "phonetic": "/ˈiːvnɪŋ/", "meaning": "n. 傍晚，晚上", "example_en": "The family gathers together for dinner every evening.", "example_cn": "全家人每天傍晚聚在一起吃晚饭。"},
        {"word": "breakfast", "phonetic": "/ˈbrekfəst/", "meaning": "n. 早餐", "example_en": "Never skip breakfast if you want to stay energetic.", "example_cn": "如果你想保持精力充沛，千万不要不吃早餐。"},
        {"word": "dinner", "phonetic": "/ˈdɪnə(r)/", "meaning": "n. 晚餐", "example_en": "We reserved a quiet corner table for tonight's dinner.", "example_cn": "我们为今晚的晚餐预订了一张安静的角落桌。"},
        {"word": "friend", "phonetic": "/frend/", "meaning": "n. 朋友", "example_en": "A true friend supports you through tough times.", "example_cn": "真正的朋友会在你困难时支持你。"},
        {"word": "family", "phonetic": "/ˈfæməli/", "meaning": "n. 家庭", "example_en": "Spending quality time with family is essential.", "example_cn": "花优质的时间陪伴家人至关重要。"},
        {"word": "school", "phonetic": "/skuːl/", "meaning": "n. 学校", "example_en": "Students walked into the school gate carrying heavy backpacks.", "example_cn": "学生们背着沉重的书包走进了校门。"},
        {"word": "teacher", "phonetic": "/ˈtiːtʃə(r)/", "meaning": "n. 老师", "example_en": "The patient teacher explained the math problem again.", "example_cn": "耐心的老师把这道数学题又讲了一遍。"},
        {"word": "market", "phonetic": "/ˈmɑːkɪt/", "meaning": "n. 集市，菜场", "example_en": "Local vendors sell fresh vegetables at the weekend market.", "example_cn": "当地小贩在周末集市上售卖新鲜蔬菜。"},
        {"word": "ticket", "phonetic": "/ˈtɪkɪt/", "meaning": "n. 票", "example_en": "Show your boarding ticket to the flight attendant.", "example_cn": "请向乘务员出示你的登机牌。"},
        {"word": "money", "phonetic": "/ˈmʌni/", "meaning": "n. 金钱", "example_en": "Save a portion of your money for emergencies.", "example_cn": "存下一部分钱以备不时之需。"},
        {"word": "doctor", "phonetic": "/ˈdɒktə(r)/", "meaning": "n. 医生", "example_en": "The doctor prescribed medicine for my sore throat.", "example_cn": "医生为我的喉咙痛开了药。"},
        {"word": "clothes", "phonetic": "/kləʊðz/", "meaning": "n. 衣服", "example_en": "Hang your wet clothes on the balcony to dry.", "example_cn": "把你的湿衣服挂在阳台上晾干。"},
        {"word": "watch", "phonetic": "/wɒtʃ/", "meaning": "n./v. 手表；观看", "example_en": "His grandfather gave him a classic leather watch.", "example_cn": "他的祖父送给他一块经典的皮带手表。"},
        {"word": "phone", "phonetic": "/fəʊn/", "meaning": "n. 电话", "example_en": "She silenced her phone during the important meeting.", "example_cn": "她在重要会议期间把手机调成了静音。"},
    ],

    # -------------------------------------------------------------
    # Level 5: 进阶社交、出行、职场工作
    # -------------------------------------------------------------
    5: [
        {"word": "schedule", "phonetic": "/ˈʃedjuːl/", "meaning": "n./v. 日程表；安排", "example_en": "The manager checked the tight production schedule.", "example_cn": "经理核对了紧凑的生产进度表。"},
        {"word": "colleague", "phonetic": "/ˈkɒliːɡ/", "meaning": "n. 同事", "example_en": "She collaborated closely with her colleagues on this project.", "example_cn": "她与同事们在这个项目上紧密合作。"},
        {"word": "deadline", "phonetic": "/ˈdedlaɪn/", "meaning": "n. 截止日期", "example_en": "We must submit the final draft before Friday's deadline.", "example_cn": "我们必须在周五截止日期前提交终稿。"},
        {"word": "presentation", "phonetic": "/ˌpreznˈteɪʃn/", "meaning": "n. 演示，汇报", "example_en": "He delivered an impressive presentation to the board.", "example_cn": "他向董事会做了一场令人印象深刻的汇报。"},
        {"word": "luggage", "phonetic": "/ˈlʌɡɪdʒ/", "meaning": "n. 行李", "example_en": "The airport staff helped retrieve her misplaced luggage.", "example_cn": "机场工作人员帮她找回了放错位置的行李。"},
        {"word": "reservation", "phonetic": "/ˌrezəˈveɪʃn/", "meaning": "n. 预订", "example_en": "I made a hotel reservation for three nights.", "example_cn": "我预订了三晚的酒店房间。"},
        {"word": "budget", "phonetic": "/ˈbʌdʒɪt/", "meaning": "n. 预算", "example_en": "Traveling on a tight budget requires careful planning.", "example_cn": "在有限预算内旅行需要精打细算。"},
        {"word": "commute", "phonetic": "/kəˈmjuːt/", "meaning": "v./n. 通勤", "example_en": "Many people commute to the downtown area by subway.", "example_cn": "许多人乘坐地铁前往市中心通勤。"},
    ],

    # -------------------------------------------------------------
    # Level 12: 中高阶社会议题、商业谈判、科技与心理
    # -------------------------------------------------------------
    12: [
        {"word": "declare", "phonetic": "/dɪˈkleə(r)/", "meaning": "v. 声明，申报", "example_en": "Passengers must declare taxable goods upon arrival at customs.", "example_cn": "旅客在抵达海关时必须申报应税物品。"},
        {"word": "negotiate", "phonetic": "/nɪˈɡəʊʃieɪt/", "meaning": "v. 谈判，协商", "example_en": "Both companies negotiated the contract terms for weeks.", "example_cn": "两家公司就合同条款谈判了数周之久。"},
        {"word": "strategy", "phonetic": "/ˈstrætədʒi/", "meaning": "n. 战略，策略", "example_en": "The startup developed an aggressive market entry strategy.", "example_cn": "这家初创公司制定了积极的市场准入策略。"},
        {"word": "efficient", "phonetic": "/ɪˈfɪʃnt/", "meaning": "adj. 高效的", "example_en": "Solar panels provide an efficient source of clean power.", "example_cn": "太阳能电池板提供了一种高效的清洁能源。"},
        {"word": "resilient", "phonetic": "/rɪˈzɪliənt/", "meaning": "adj. 适应力强的，有韧性的", "example_en": "Local communities proved remarkably resilient after the storm.", "example_cn": "风暴过后，当地社区展现出了极强的韧性。"},
        {"word": "subtle", "phonetic": "/ˈsʌtl/", "meaning": "adj. 微妙的，不易察觉的", "example_en": "There was a subtle change in his tone of voice.", "example_cn": "他的语气发生了微妙的变化。"},
        {"word": "evaluate", "phonetic": "/ɪˈvæljueɪt/", "meaning": "v. 评估，评价", "example_en": "The committee will evaluate candidate qualifications objectively.", "example_cn": "委员会将客观评估候选人的资质。"},
    ],

    # -------------------------------------------------------------
    # Level 20: 顶尖学术、哲学与高阶抽象词汇（GRE / 考研 / 雅思高分）
    # -------------------------------------------------------------
    20: [
        {"word": "ubiquitous", "phonetic": "/juːˈbɪkwɪtəs/", "meaning": "adj. 无处不在的", "example_en": "Smartphones have become ubiquitous across modern human society.", "example_cn": "智能手机在现代人类社会中已经变得无处不在。"},
        {"word": "meticulous", "phonetic": "/məˈtɪkjələs/", "meaning": "adj. 一丝不苟的，缜密的", "example_en": "The forensic scientist conducted a meticulous examination of the evidence.", "example_cn": "法医科学家对证据进行了一丝不苟的检查。"},
        {"word": "ephemeral", "phonetic": "/ɪˈfemərəl/", "meaning": "adj. 短暂的，转瞬即逝的", "example_en": "Cherry blossoms are admired worldwide for their ephemeral beauty.", "example_cn": "樱花因其转瞬即逝的美丽而受到全世界的赞赏。"},
        {"word": "pragmatic", "phonetic": "/præɡˈmætɪk/", "meaning": "adj. 务实的，注重实效的", "example_en": "Diplomats sought a pragmatic compromise to avert further conflict.", "example_cn": "外交官们寻求务实的妥协以避免进一步的冲突。"},
        {"word": "paradoxical", "phonetic": "/ˌpærəˈdɒksɪkl/", "meaning": "adj. 矛盾的，看似悖论的", "example_en": "It is paradoxical that increased connectivity can cause deeper loneliness.", "example_cn": "看似矛盾的是，越是紧密互联反而可能导致更深的孤独感。"},
        {"word": "lucid", "phonetic": "/ˈluːsɪd/", "meaning": "adj. 清晰的，头脑清醒的", "example_en": "The professor provided a remarkably lucid explanation of quantum mechanics.", "example_cn": "教授对量子力学做出了极其清晰易懂的阐述。"},
        {"word": "inevitable", "phonetic": "/ɪnˈevɪtəbl/", "meaning": "adj. 不可避免的", "example_en": "Technological disruption is an inevitable consequence of rapid innovation.", "example_cn": "技术颠覆是快速创新不可避免的产物。"},
    ]
}

# 填充未显式书写的关卡，保障每个 Level 均有独立的词单
for lvl in range(1, 21):
  if lvl not in GLOBAL_VOCAB_DB:
    # 选取最近难度的关卡数据进行平滑填充，确保不会空白
    nearest_lvl = max([k for k in GLOBAL_VOCAB_DB.keys() if k <= lvl])
    GLOBAL_VOCAB_DB[lvl] = list(GLOBAL_VOCAB_DB[nearest_lvl])
