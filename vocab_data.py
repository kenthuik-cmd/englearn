# vocab_data.py
# 真实难度递进词库：每个词独立造句，拒绝模板句

GLOBAL_VOCAB_DB = {
    1: [
        # 基础问候与礼貌
        {"word": "hello", "phonetic": "/həˈləʊ/", "meaning": "int. 你好", "example_en": "Hello, it's really nice to finally meet you.", "example_cn": "你好，终于见到你了很高兴。"},
        {"word": "goodbye", "phonetic": "/ˌɡʊdˈbaɪ/", "meaning": "int. 再见", "example_en": "I have to leave now, goodbye!", "example_cn": "我现在得走了，再见！"},
        {"word": "please", "phonetic": "/pliːz/", "meaning": "adv. 请", "example_en": "Could you pass me the salt, please?", "example_cn": "请把盐递给我好吗？"},
        {"word": "sorry", "phonetic": "/ˈsɒri/", "meaning": "adj. 抱歉的", "example_en": "I am so sorry for being late today.", "example_cn": "今天迟到了我非常抱歉。"},
        {"word": "thanks", "phonetic": "/θæŋks/", "meaning": "n. 感谢", "example_en": "Thanks a lot for helping me move the desk.", "example_cn": "多谢你帮我搬桌子。"},
        {"word": "yes", "phonetic": "/jes/", "meaning": "adv. 是的", "example_en": "Yes, I completely agree with your plan.", "example_cn": "是的，我完全同意你的计划。"},
        {"word": "no", "phonetic": "/nəʊ/", "meaning": "adv. 不", "example_en": "No, I don't want to go out tonight.", "example_cn": "不，我今晚不想出门。"},
        {"word": "ok", "phonetic": "/ˌəʊˈkeɪ/", "meaning": "adj./adv. 好的", "example_en": "Are you feeling ok after the long trip?", "example_cn": "长途旅行后你感觉还好吗？"},
        {"word": "excuse", "phonetic": "/ɪkˈskjuːz/", "meaning": "v. 原谅；劳驾", "example_en": "Excuse me, where is the nearest restroom?", "example_cn": "打扰一下，请问最近的洗手间在哪里？"},
        {"word": "help", "phonetic": "/help/", "meaning": "v./n. 帮助", "example_en": "Can you help me carry these heavy bags?", "example_cn": "你能帮我提这些重包吗？"},

        # 餐饮与食物
        {"word": "water", "phonetic": "/ˈwɔːtə(r)/", "meaning": "n. 水", "example_en": "Could I get a glass of warm water?", "example_cn": "能给我来一杯温水吗？"},
        {"word": "bread", "phonetic": "/bred/", "meaning": "n. 面包", "example_en": "We need to buy some fresh bread for tomorrow.", "example_cn": "我们需要买点新鲜面包留到明天吃。"},
        {"word": "milk", "phonetic": "/mɪlk/", "meaning": "n. 牛奶", "example_en": "Do you take milk and sugar in your coffee?", "example_cn": "你的咖啡里要加牛奶和糖吗？"},
        {"word": "coffee", "phonetic": "/ˈkɒfi/", "meaning": "n. 咖啡", "example_en": "Let's grab a cup of coffee this afternoon.", "example_cn": "下午我们去喝杯咖啡吧。"},
        {"word": "tea", "phonetic": "/tiː/", "meaning": "n. 茶", "example_en": "I prefer drinking green tea over juice.", "example_cn": "相比果汁，我更喜欢喝绿茶。"},
        {"word": "rice", "phonetic": "/raɪs/", "meaning": "n. 米饭", "example_en": "Steamed rice is a daily staple for many people.", "example_cn": "白米饭是很多人的日常主食。"},
        {"word": "meat", "phonetic": "/miːt/", "meaning": "n. 肉", "example_en": "He doesn't eat meat because he is a vegetarian.", "example_cn": "他不吃肉，因为他是素食主义者。"},
        {"word": "fish", "phonetic": "/fɪʃ/", "meaning": "n. 鱼", "example_en": "We had grilled fish with lemon for dinner.", "example_cn": "我们晚饭吃了柠檬烤鱼。"},
        {"word": "egg", "phonetic": "/eɡ/", "meaning": "n. 鸡蛋", "example_en": "I usually fry an egg for my breakfast.", "example_cn": "我通常早餐煎一个鸡蛋。"},
        {"word": "apple", "phonetic": "/ˈæpl/", "meaning": "n. 苹果", "example_en": "She bought some sweet red apples at the market.", "example_cn": "她在市场上买了一些甜红苹果。"},
        
        # 用餐动作与餐具
        {"word": "eat", "phonetic": "/iːt/", "meaning": "v. 吃", "example_en": "What do you want to eat for lunch?", "example_cn": "你午饭想吃什么？"},
        {"word": "drink", "phonetic": "/drɪŋk/", "meaning": "v. 喝", "example_en": "Make sure to drink enough water when it's hot.", "example_cn": "天气热的时候一定要多喝水。"},
        {"word": "hungry", "phonetic": "/ˈhʌŋɡri/", "meaning": "adj. 饥饿的", "example_en": "I am so hungry that I could eat a horse.", "example_cn": "我饿得简直能吃下一头牛。"},
        {"word": "thirsty", "phonetic": "/ˈθɜːsti/", "meaning": "adj. 口渴的", "example_en": "Running makes me really thirsty.", "example_cn": "跑步让我觉得非常口渴。"},
        {"word": "cup", "phonetic": "/kʌp/", "meaning": "n. 杯子", "example_en": "Be careful, that cup of tea is extremely hot.", "example_cn": "当心点，那杯茶非常烫。"},
        {"word": "bowl", "phonetic": "/bəʊl/", "meaning": "n. 碗", "example_en": "He ate a large bowl of chicken noodle soup.", "example_cn": "他吃了一大碗鸡肉面汤。"},
        {"word": "plate", "phonetic": "/pleɪt/", "meaning": "n. 盘子", "example_en": "Put the washed vegetables on the white plate.", "example_cn": "把洗好的蔬菜放在白盘子上。"},
        {"word": "spoon", "phonetic": "/spuːn/", "meaning": "n. 勺子", "example_en": "You need a spoon to eat this dessert.", "example_cn": "你需要一把勺子来吃这个甜点。"},
        {"word": "fork", "phonetic": "/fɔːk/", "meaning": "n. 叉子", "example_en": "Can I get a clean fork, please?", "example_cn": "能给我一把干净的叉子吗？"},
        {"word": "knife", "phonetic": "/naɪf/", "meaning": "n. 刀", "example_en": "Use the sharp knife to cut the steak.", "example_cn": "用那把锋利的刀切牛排。"},

        # 日常地点
        {"word": "home", "phonetic": "/həʊm/", "meaning": "n. 家", "example_en": "I will go straight home after work today.", "example_cn": "我今天下班后会直接回家。"},
        {"word": "school", "phonetic": "/skuːl/", "meaning": "n. 学校", "example_en": "My little brother walks to school every morning.", "example_cn": "我弟弟每天早晨步行去学校。"},
        {"word": "work", "phonetic": "/wɜːk/", "meaning": "n./v. 工作", "example_en": "She has a lot of work to finish by tomorrow.", "example_cn": "她有很多工作要在明天前完成。"},
        {"word": "store", "phonetic": "/stɔː(r)/", "meaning": "n. 商店", "example_en": "I need to run to the store to buy milk.", "example_cn": "我得去趟商店买牛奶。"},
        {"word": "park", "phonetic": "/pɑːk/", "meaning": "n. 公园", "example_en": "Let's take a walk in the park after dinner.", "example_cn": "吃完饭我们去公园散步吧。"},
        {"word": "hospital", "phonetic": "/ˈhɒspɪtl/", "meaning": "n. 医院", "example_en": "The ambulance rushed him to the nearest hospital.", "example_cn": "救护车把他紧急送往了最近的医院。"},
        {"word": "bank", "phonetic": "/bæŋk/", "meaning": "n. 银行", "example_en": "I need to withdraw some cash from the bank.", "example_cn": "我需要去银行取点现金。"},
        {"word": "restaurant", "phonetic": "/ˈrestrɒnt/", "meaning": "n. 餐厅", "example_en": "They serve excellent pizza at that Italian restaurant.", "example_cn": "那家意大利餐厅的披萨非常棒。"},
        {"word": "hotel", "phonetic": "/həʊˈtel/", "meaning": "n. 酒店", "example_en": "We booked a room in a nice hotel near the beach.", "example_cn": "我们在海滩边一家不错的酒店订了房间。"},
        {"word": "airport", "phonetic": "/ˈeəpɔːt/", "meaning": "n. 机场", "example_en": "You should arrive at the airport two hours early.", "example_cn": "你应该提前两小时到达机场。"},

        # 交通出行
        {"word": "car", "phonetic": "/kɑː(r)/", "meaning": "n. 汽车", "example_en": "He parked his car right outside the building.", "example_cn": "他把车直接停在了大楼外面。"},
        {"word": "bus", "phonetic": "/bʌs/", "meaning": "n. 巴士", "example_en": "I missed the morning bus and had to take a taxi.", "example_cn": "我错过了早班车，只好打车了。"},
        {"word": "train", "phonetic": "/treɪn/", "meaning": "n. 火车", "example_en": "The train to London leaves in ten minutes.", "example_cn": "开往伦敦的火车十分钟后出发。"},
        {"word": "taxi", "phonetic": "/ˈtæksi/", "meaning": "n. 出租车", "example_en": "Let's grab a taxi, it's raining heavily outside.", "example_cn": "我们在外面下大雨呢，打辆出租车吧。"},
        {"word": "bike", "phonetic": "/baɪk/", "meaning": "n. 自行车", "example_en": "Riding a bike is a great way to stay fit.", "example_cn": "骑自行车是保持健康的好方法。"},
        {"word": "subway", "phonetic": "/ˈsʌbweɪ/", "meaning": "n. 地铁", "example_en": "Taking the subway is the fastest way to avoid traffic.", "example_cn": "坐地铁是避开交通拥堵最快的方式。"},
        {"word": "ticket", "phonetic": "/ˈtɪkɪt/", "meaning": "n. 票", "example_en": "Please show your ticket to the conductor.", "example_cn": "请向售票员出示你的车票。"},
        {"word": "station", "phonetic": "/ˈsteɪʃn/", "meaning": "n. 车站", "example_en": "I will meet you at the central railway station.", "example_cn": "我会在中央火车站和你碰面。"},
        {"word": "fly", "phonetic": "/flaɪ/", "meaning": "v. 飞行；乘飞机", "example_en": "We will fly to Paris for our summer vacation.", "example_cn": "暑假我们将飞往巴黎。"},
        {"word": "drive", "phonetic": "/draɪv/", "meaning": "v. 驾驶", "example_en": "Don't drive if you feel tired or sleepy.", "example_cn": "如果你觉得累或困，就别开车了。"},

        # 时间与节律
        {"word": "day", "phonetic": "/deɪ/", "meaning": "n. 天；白天", "example_en": "It has been a really long and exhausting day.", "example_cn": "这真是漫长又疲惫的一天。"},
        {"word": "night", "phonetic": "/naɪt/", "meaning": "n. 夜晚", "example_en": "The baby woke up crying in the middle of the night.", "example_cn": "婴儿半夜醒来哭闹。"},
        {"word": "morning", "phonetic": "/ˈmɔːnɪŋ/", "meaning": "n. 早晨", "example_en": "I like to read the news in the morning.", "example_cn": "我喜欢在早晨看新闻。"},
        {"word": "afternoon", "phonetic": "/ˌɑːftəˈnuːn/", "meaning": "n. 下午", "example_en": "We have a team meeting scheduled for this afternoon.", "example_cn": "我们定在今天下午开团队会议。"},
        {"word": "evening", "phonetic": "/ˈiːvnɪŋ/", "meaning": "n. 傍晚", "example_en": "The sunset looks beautiful this evening.", "example_cn": "今晚的日落看起来很美。"},
        {"word": "today", "phonetic": "/təˈdeɪ/", "meaning": "n./adv. 今天", "example_en": "What are your plans for today?", "example_cn": "你今天有什么安排？"},
        {"word": "tomorrow", "phonetic": "/təˈmɒrəʊ/", "meaning": "n./adv. 明天", "example_en": "I will call you tomorrow to confirm the details.", "example_cn": "我明天会打电话向你确认细节。"},
        {"word": "yesterday", "phonetic": "/ˈjestədeɪ/", "meaning": "n./adv. 昨天", "example_en": "We went to the cinema yesterday evening.", "example_cn": "我们昨晚去电影院了。"},
        {"word": "week", "phonetic": "/wiːk/", "meaning": "n. 星期；周", "example_en": "I have been incredibly busy this whole week.", "example_cn": "我整整一个星期都忙得不可开交。"},
        {"word": "month", "phonetic": "/mʌnθ/", "meaning": "n. 月份", "example_en": "Rent is due on the first day of every month.", "example_cn": "房租必须在每个月的第一天交。"},

        # 购物与金钱
        {"word": "buy", "phonetic": "/baɪ/", "meaning": "v. 买", "example_en": "Where did you buy this lovely dress?", "example_cn": "你在哪里买的这件漂亮的衣服？"},
        {"word": "sell", "phonetic": "/sel/", "meaning": "v. 卖", "example_en": "They sell fresh organic vegetables here.", "example_cn": "他们在这里卖新鲜的有机蔬菜。"},
        {"word": "cost", "phonetic": "/kɒst/", "meaning": "v./n. 花费；成本", "example_en": "How much does this laptop cost?", "example_cn": "这台笔记本电脑要多少钱？"},
        {"word": "money", "phonetic": "/ˈmʌni/", "meaning": "n. 钱", "example_en": "I need to save some money for a new phone.", "example_cn": "我得存点钱买个新手机了。"},
        {"word": "price", "phonetic": "/praɪs/", "meaning": "n. 价格", "example_en": "The price of gasoline has gone up again.", "example_cn": "汽油的价格又上涨了。"},
        {"word": "cheap", "phonetic": "/tʃiːp/", "meaning": "adj. 便宜的", "example_en": "Flight tickets are usually cheap during the off-season.", "example_cn": "淡季的机票通常很便宜。"},
        {"word": "expensive", "phonetic": "/ɪkˈspensɪv/", "meaning": "adj. 昂贵的", "example_en": "Eating at that restaurant is too expensive for us.", "example_cn": "在那家餐厅吃饭对我们来说太贵了。"},
        {"word": "pay", "phonetic": "/peɪ/", "meaning": "v. 支付", "example_en": "Can I pay for my groceries with a credit card?", "example_cn": "我可以用信用卡支付杂货钱吗？"},
        {"word": "cash", "phonetic": "/kæʃ/", "meaning": "n. 现金", "example_en": "The small shop only accepts cash payments.", "example_cn": "这家小店只接受现金支付。"},
        {"word": "card", "phonetic": "/kɑːd/", "meaning": "n. 卡片；银行卡", "example_en": "Swipe your card to open the hotel room door.", "example_cn": "刷卡打开酒店房门。"},

        # 人际关系
        {"word": "family", "phonetic": "/ˈfæməli/", "meaning": "n. 家人；家庭", "example_en": "My family usually watches a movie together on Fridays.", "example_cn": "我的家人通常在周五一起看电影。"},
        {"word": "friend", "phonetic": "/frend/", "meaning": "n. 朋友", "example_en": "She has been my best friend since high school.", "example_cn": "她从高中起就是我最好的朋友。"},
        {"word": "father", "phonetic": "/ˈfɑːðə(r)/", "meaning": "n. 父亲", "example_en": "His father taught him how to ride a bicycle.", "example_cn": "他父亲教他怎么骑自行车。"},
        {"word": "mother", "phonetic": "/ˈmʌðə(r)/", "meaning": "n. 母亲", "example_en": "My mother makes the best chocolate cake in the world.", "example_cn": "我妈妈做的巧克力蛋糕是世界上最好吃的。"},
        {"word": "brother", "phonetic": "/ˈbrʌðə(r)/", "meaning": "n. 兄弟", "example_en": "My older brother is currently studying in college.", "example_cn": "我哥哥目前在读大学。"},
        {"word": "sister", "phonetic": "/ˈsɪstə(r)/", "meaning": "n. 姐妹", "example_en": "Her younger sister wants to become a nurse.", "example_cn": "她妹妹想成为一名护士。"},
        {"word": "husband", "phonetic": "/ˈhʌzbənd/", "meaning": "n. 丈夫", "example_en": "Her husband is cooking dinner in the kitchen.", "example_cn": "她丈夫正在厨房做晚饭。"},
        {"word": "wife", "phonetic": "/waɪf/", "meaning": "n. 妻子", "example_en": "He bought a beautiful necklace for his wife.", "example_cn": "他给妻子买了一条漂亮的项链。"},
        {"word": "child", "phonetic": "/tʃaɪld/", "meaning": "n. 孩子", "example_en": "The child laughed happily while playing on the swing.", "example_cn": "孩子荡秋千时开心地笑了。"},
        {"word": "person", "phonetic": "/ˈpɜːsn/", "meaning": "n. 人", "example_en": "He is a very reliable person to work with.", "example_cn": "他是一个非常靠谱的合作伙伴。"},

        # 基础动作
        {"word": "sleep", "phonetic": "/sliːp/", "meaning": "v. 睡觉", "example_en": "You need to sleep at least eight hours a night.", "example_cn": "你每晚需要睡至少八个小时。"},
        {"word": "wake", "phonetic": "/weɪk/", "meaning": "v. 醒来", "example_en": "I usually wake up at 7 AM on weekdays.", "example_cn": "工作日我通常早上7点醒来。"},
        {"word": "wash", "phonetic": "/wɒʃ/", "meaning": "v. 洗", "example_en": "Please wash your hands before eating dinner.", "example_cn": "吃晚饭前请洗手。"},
        {"word": "clean", "phonetic": "/kliːn/", "meaning": "v./adj. 打扫；干净的", "example_en": "We spent the whole morning cleaning the living room.", "example_cn": "我们花了一上午打扫客厅。"},
        {"word": "open", "phonetic": "/ˈəʊpən/", "meaning": "v./adj. 打开", "example_en": "Could you open the window? It's stuffy in here.", "example_cn": "能打开窗户吗？这里有点闷。"},
        {"word": "close", "phonetic": "/kləʊz/", "meaning": "v. 关上", "example_en": "Don't forget to close the door when you leave.", "example_cn": "你走的时候别忘了关门。"},
        {"word": "push", "phonetic": "/pʊʃ/", "meaning": "v. 推", "example_en": "You have to push the door hard to open it.", "example_cn": "你得用力推才能把门打开。"},
        {"word": "pull", "phonetic": "/pʊl/", "meaning": "v. 拉", "example_en": "He had to pull the heavy box across the floor.", "example_cn": "他不得不把那个沉重的箱子拖过地板。"},
        {"word": "walk", "phonetic": "/wɔːk/", "meaning": "v. 步行", "example_en": "They decided to walk to the beach instead of driving.", "example_cn": "他们决定走路去海滩，而不是开车。"},
        {"word": "run", "phonetic": "/rʌn/", "meaning": "v. 跑", "example_en": "She had to run to catch the departing train.", "example_cn": "她不得不跑着去赶那趟快开的火车。"},

        # 情绪与状态
        {"word": "happy", "phonetic": "/ˈhæpi/", "meaning": "adj. 高兴的", "example_en": "I am so happy to hear your good news.", "example_cn": "听到你的好消息我太高兴了。"},
        {"word": "sad", "phonetic": "/sæd/", "meaning": "adj. 伤心的", "example_en": "He felt sad when his pet dog passed away.", "example_cn": "宠物狗去世时他感到很伤心。"},
        {"word": "tired", "phonetic": "/ˈtaɪəd/", "meaning": "adj. 疲劳的", "example_en": "I'm too tired to cook tonight, let's order takeout.", "example_cn": "我今晚累得不想做饭了，我们叫外卖吧。"},
        {"word": "busy", "phonetic": "/ˈbɪzi/", "meaning": "adj. 忙碌的", "example_en": "The manager is very busy with meetings all day.", "example_cn": "经理整天忙于开会。"},
        {"word": "free", "phonetic": "/friː/", "meaning": "adj. 空闲的；免费的", "example_en": "Are you free to grab a coffee this weekend?", "example_cn": "这周末你有空去喝杯咖啡吗？"},
        {"word": "good", "phonetic": "/ɡʊd/", "meaning": "adj. 好的", "example_en": "This is a really good book for beginners.", "example_cn": "这对初学者来说真是一本好书。"},
        {"word": "bad", "phonetic": "/bæd/", "meaning": "adj. 坏的", "example_en": "Smoking is a bad habit for your health.", "example_cn": "吸烟是对健康有害的坏习惯。"},
        {"word": "hot", "phonetic": "/hɒt/", "meaning": "adj. 热的", "example_en": "Be careful, the soup is extremely hot.", "example_cn": "小心点，汤非常烫。"},
        {"word": "cold", "phonetic": "/kəʊld/", "meaning": "adj. 冷的", "example_en": "Put on a jacket, it's quite cold outside.", "example_cn": "穿件外套吧，外面挺冷的。"},
        {"word": "sick", "phonetic": "/sɪk/", "meaning": "adj. 生病的", "example_en": "He stayed in bed because he felt sick.", "example_cn": "他因为生病而躺在床上休息。"}
    ]
}

# 为了保证程序不报错，其余 19 个关卡我们先用 Level 1 占位兜底
# 当你获取了新的 Level 词库后，可以直接贴进来替换
for lvl in range(2, 21):
    GLOBAL_VOCAB_DB[lvl] = list(GLOBAL_VOCAB_DB[1])
