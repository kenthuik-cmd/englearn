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
# -------------------------------------------------------------
    # Level 2: 身体、衣物、居家、天气、基础动作与情绪 - 100词
    # -------------------------------------------------------------
    2: [
        # 身体部位
        {"word": "head", "phonetic": "/hed/", "meaning": "n. 头", "example_en": "My head hurts from staring at the screen too long.", "example_cn": "盯着屏幕太久，我的头好痛。"},
        {"word": "face", "phonetic": "/feɪs/", "meaning": "n. 脸", "example_en": "She washed her face with cold water this morning.", "example_cn": "她今早用冷水洗了脸。"},
        {"word": "eye", "phonetic": "/aɪ/", "meaning": "n. 眼睛", "example_en": "He closed his eyes and listened to the music.", "example_cn": "他闭上眼睛，静静地听音乐。"},
        {"word": "ear", "phonetic": "/ɪə(r)/", "meaning": "n. 耳朵", "example_en": "The dog pricked up its ears at the sound.", "example_cn": "那只狗听到声音竖起了耳朵。"},
        {"word": "nose", "phonetic": "/nəʊz/", "meaning": "n. 鼻子", "example_en": "My nose is running because of the cold weather.", "example_cn": "天气太冷，我流鼻涕了。"},
        {"word": "mouth", "phonetic": "/maʊθ/", "meaning": "n. 嘴巴", "example_en": "Cover your mouth when you cough.", "example_cn": "咳嗽时请捂住嘴。"},
        {"word": "tooth", "phonetic": "/tuːθ/", "meaning": "n. 牙齿", "example_en": "My front tooth aches when I drink cold water.", "example_cn": "我喝冷水时门牙会痛。"},
        {"word": "hair", "phonetic": "/heə(r)/", "meaning": "n. 头发", "example_en": "She has long, curly brown hair.", "example_cn": "她有一头长长的棕色卷发。"},
        {"word": "hand", "phonetic": "/hænd/", "meaning": "n. 手", "example_en": "Please wash your hands before eating dinner.", "example_cn": "晚饭前请洗手。"},
        {"word": "foot", "phonetic": "/fʊt/", "meaning": "n. 脚", "example_en": "I accidentally stepped on his left foot.", "example_cn": "我不小心踩到了他的左脚。"},

        # 衣物与穿搭
        {"word": "clothes", "phonetic": "/kləʊðz/", "meaning": "n. 衣服", "example_en": "Put your dirty clothes in the washing machine.", "example_cn": "把你的脏衣服放进洗衣机里。"},
        {"word": "shirt", "phonetic": "/ʃɜːt/", "meaning": "n. 衬衫", "example_en": "He wore a crisp white shirt to the interview.", "example_cn": "他穿着挺括的白衬衫去面试。"},
        {"word": "pants", "phonetic": "/pænts/", "meaning": "n. 裤子", "example_en": "I need to buy a new pair of black pants for work.", "example_cn": "我需要买一条新的黑裤子上班穿。"},
        {"word": "dress", "phonetic": "/dres/", "meaning": "n. 连衣裙", "example_en": "She wore a beautiful red dress to the party.", "example_cn": "她穿了一条美丽的红裙子去参加派对。"},
        {"word": "shoe", "phonetic": "/ʃuː/", "meaning": "n. 鞋子", "example_en": "I can't find my other shoe anywhere.", "example_cn": "我到处都找不到我的另一只鞋。"},
        {"word": "hat", "phonetic": "/hæt/", "meaning": "n. 帽子", "example_en": "Put on a hat to protect yourself from the sun.", "example_cn": "戴上帽子防晒吧。"},
        {"word": "coat", "phonetic": "/kəʊt/", "meaning": "n. 外套", "example_en": "It's freezing outside, so put on a heavy coat.", "example_cn": "外面冷极了，穿上厚外套吧。"},
        {"word": "wear", "phonetic": "/weə(r)/", "meaning": "v. 穿，戴", "example_en": "What are you going to wear for the dinner tonight?", "example_cn": "今晚的晚宴你打算穿什么？"},
        {"word": "bag", "phonetic": "/bæɡ/", "meaning": "n. 包", "example_en": "I left my keys in my gym bag.", "example_cn": "我把钥匙忘在健身包里了。"},
        {"word": "wallet", "phonetic": "/ˈwɒlɪt/", "meaning": "n. 钱包", "example_en": "He panicked when he realized he lost his wallet.", "example_cn": "当他意识到丢了钱包时，他慌了。"},

        # 居家与生活环境
        {"word": "room", "phonetic": "/ruːm/", "meaning": "n. 房间", "example_en": "My bedroom is the quietest room in the house.", "example_cn": "我的卧室是家里最安静的房间。"},
        {"word": "door", "phonetic": "/dɔː(r)/", "meaning": "n. 门", "example_en": "Please lock the front door when you leave.", "example_cn": "离开时请锁好前门。"},
        {"word": "window", "phonetic": "/ˈwɪndəʊ/", "meaning": "n. 窗户", "example_en": "Open the window to let some fresh air in.", "example_cn": "打开窗户透透新鲜空气。"},
        {"word": "wall", "phonetic": "/wɔːl/", "meaning": "n. 墙壁", "example_en": "We decided to paint the living room wall blue.", "example_cn": "我们决定把客厅的墙刷成蓝色。"},
        {"word": "floor", "phonetic": "/flɔː(r)/", "meaning": "n. 地板", "example_en": "Be careful, the floor is wet and slippery.", "example_cn": "小心点，地板又湿又滑。"},
        {"word": "bed", "phonetic": "/bed/", "meaning": "n. 床", "example_en": "I was so tired that I went straight to bed.", "example_cn": "我太累了，直接上床睡觉了。"},
        {"word": "table", "phonetic": "/ˈteɪbl/", "meaning": "n. 桌子", "example_en": "The family sat around the dining table for supper.", "example_cn": "一家人围坐在餐桌旁吃晚饭。"},
        {"word": "chair", "phonetic": "/tʃeə(r)/", "meaning": "n. 椅子", "example_en": "Pull up a chair and join us.", "example_cn": "拉把椅子过来加入我们吧。"},
        {"word": "light", "phonetic": "/laɪt/", "meaning": "n. 灯光；灯", "example_en": "Turn off the light before you go to sleep.", "example_cn": "睡觉前把灯关掉。"},
        {"word": "key", "phonetic": "/kiː/", "meaning": "n. 钥匙", "example_en": "I can't find my house key anywhere.", "example_cn": "我哪儿也找不到我家的钥匙。"},

        # 颜色与基础形容词
        {"word": "color", "phonetic": "/ˈkʌlə(r)/", "meaning": "n. 颜色", "example_en": "What is your favorite color?", "example_cn": "你最喜欢的颜色是什么？"},
        {"word": "red", "phonetic": "/red/", "meaning": "adj. 红色的", "example_en": "She painted her nails a bright red.", "example_cn": "她把指甲涂成了明亮的红色。"},
        {"word": "blue", "phonetic": "/bluː/", "meaning": "adj. 蓝色的", "example_en": "The sky is clear and blue today.", "example_cn": "今天天空晴朗蔚蓝。"},
        {"word": "green", "phonetic": "/ɡriːn/", "meaning": "adj. 绿色的", "example_en": "The green traffic light means you can go.", "example_cn": "绿色交通灯意味着你可以通行。"},
        {"word": "yellow", "phonetic": "/ˈjeləʊ/", "meaning": "adj. 黄色的", "example_en": "The walls are painted a warm yellow.", "example_cn": "墙壁被漆成了温暖的黄色。"},
        {"word": "black", "phonetic": "/blæk/", "meaning": "adj. 黑色的", "example_en": "He prefers to drink his coffee black.", "example_cn": "他喜欢喝不加奶的黑咖啡。"},
        {"word": "white", "phonetic": "/waɪt/", "meaning": "adj. 白色的", "example_en": "She wrote the note on a blank white piece of paper.", "example_cn": "她在一张空白的白纸上写下了便条。"},
        {"word": "big", "phonetic": "/bɪɡ/", "meaning": "adj. 大的", "example_en": "They moved into a really big apartment.", "example_cn": "他们搬进了一间非常大的公寓。"},
        {"word": "small", "phonetic": "/smɔːl/", "meaning": "adj. 小的", "example_en": "The town is too small to have a shopping mall.", "example_cn": "这个镇太小了，连个购物中心都没有。"},
        {"word": "beautiful", "phonetic": "/ˈbjuːtɪfl/", "meaning": "adj. 美丽的", "example_en": "We enjoyed a beautiful sunset at the beach.", "example_cn": "我们在海滩上欣赏了美丽的日落。"},

        # 天气与自然
        {"word": "weather", "phonetic": "/ˈweðə(r)/", "meaning": "n. 天气", "example_en": "The weather is supposed to be nice this weekend.", "example_cn": "预计这周末天气会很好。"},
        {"word": "sun", "phonetic": "/sʌn/", "meaning": "n. 太阳", "example_en": "The sun rises in the east and sets in the west.", "example_cn": "太阳东升西落。"},
        {"word": "rain", "phonetic": "/reɪn/", "meaning": "n. 雨", "example_en": "We canceled the picnic because of the heavy rain.", "example_cn": "因为下大雨，我们取消了野餐。"},
        {"word": "snow", "phonetic": "/snəʊ/", "meaning": "n. 雪", "example_en": "The children went outside to play in the snow.", "example_cn": "孩子们跑出去在雪地里玩耍。"},
        {"word": "wind", "phonetic": "/wɪnd/", "meaning": "n. 风", "example_en": "A strong wind blew my hat off.", "example_cn": "一阵强风把我的帽子吹掉了。"},
        {"word": "sky", "phonetic": "/skaɪ/", "meaning": "n. 天空", "example_en": "There are no clouds in the sky tonight.", "example_cn": "今晚天空中一片云也没有。"},
        {"word": "tree", "phonetic": "/triː/", "meaning": "n. 树木", "example_en": "They planted an apple tree in their backyard.", "example_cn": "他们在后院种了一棵苹果树。"},
        {"word": "flower", "phonetic": "/ˈflaʊə(r)/", "meaning": "n. 花朵", "example_en": "He gave her a bunch of beautiful flowers.", "example_cn": "他送给她一束美丽的花。"},
        {"word": "dog", "phonetic": "/dɒɡ/", "meaning": "n. 狗", "example_en": "Our dog barks whenever the mailman arrives.", "example_cn": "邮递员一到，我家的狗就会叫。"},
        {"word": "cat", "phonetic": "/kæt/", "meaning": "n. 猫", "example_en": "The cat is sleeping peacefully on the sofa.", "example_cn": "猫正安详地睡在沙发上。"},

        # 时间与频率
        {"word": "year", "phonetic": "/jɪə(r)/", "meaning": "n. 年", "example_en": "I traveled to Japan last year.", "example_cn": "我去年去日本旅行了。"},
        {"word": "hour", "phonetic": "/ˈaʊə(r)/", "meaning": "n. 小时", "example_en": "The flight to London takes about twelve hours.", "example_cn": "飞往伦敦的航班大约需要十二个小时。"},
        {"word": "minute", "phonetic": "/ˈmɪnɪt/", "meaning": "n. 分钟", "example_en": "Please wait a minute, I'll be right with you.", "example_cn": "请稍等一分钟，我马上过来。"},
        {"word": "now", "phonetic": "/naʊ/", "meaning": "adv. 现在", "example_en": "We need to leave right now to catch the train.", "example_cn": "我们现在就得走才能赶上火车。"},
        {"word": "soon", "phonetic": "/suːn/", "meaning": "adv. 很快，不久", "example_en": "The movie is going to start very soon.", "example_cn": "电影很快就要开始了。"},
        {"word": "early", "phonetic": "/ˈɜːli/", "meaning": "adj./adv. 早的", "example_en": "I woke up early to watch the sunrise.", "example_cn": "我起得很早去看日出。"},
        {"word": "late", "phonetic": "/leɪt/", "meaning": "adj./adv. 迟的，晚的", "example_en": "Hurry up, or we will be late for the meeting.", "example_cn": "快点，否则我们开会要迟到了。"},
        {"word": "always", "phonetic": "/ˈɔːlweɪz/", "meaning": "adv. 总是", "example_en": "She always locks the door before leaving.", "example_cn": "她离开前总是会锁好门。"},
        {"word": "sometimes", "phonetic": "/ˈsʌmtaɪmz/", "meaning": "adv. 有时", "example_en": "Sometimes I prefer staying home rather than going out.", "example_cn": "有时我更喜欢待在家里而不是出门。"},
        {"word": "never", "phonetic": "/ˈnevə(r)/", "meaning": "adv. 从不", "example_en": "I have never been to a music festival before.", "example_cn": "我以前从未去过音乐节。"},

        # 方向与位置
        {"word": "left", "phonetic": "/left/", "meaning": "n./adv. 左边", "example_en": "Turn left at the next intersection.", "example_cn": "在下一个十字路口左转。"},
        {"word": "right", "phonetic": "/raɪt/", "meaning": "n./adv. 右边", "example_en": "Keep right on the highway unless you're passing.", "example_cn": "在高速公路上除非超车，否则请靠右行驶。"},
        {"word": "up", "phonetic": "/ʌp/", "meaning": "adv. 向上", "example_en": "Look up at the stars in the night sky.", "example_cn": "抬头看看夜空中的星星。"},
        {"word": "down", "phonetic": "/daʊn/", "meaning": "adv. 向下", "example_en": "Please sit down and make yourself comfortable.", "example_cn": "请坐下，别拘束。"},
        {"word": "here", "phonetic": "/hɪə(r)/", "meaning": "adv. 这里", "example_en": "I have lived here for over five years.", "example_cn": "我已经在这里住了五年多了。"},
        {"word": "there", "phonetic": "/ðeə(r)/", "meaning": "adv. 那里", "example_en": "Put the boxes over there in the corner.", "example_cn": "把那些箱子放在那边的角落里。"},
        {"word": "near", "phonetic": "/nɪə(r)/", "meaning": "prep./adv. 靠近", "example_en": "Is there a good supermarket near your house?", "example_cn": "你家附近有好的超市吗？"},
        {"word": "far", "phonetic": "/fɑː(r)/", "meaning": "adv. 远", "example_en": "The airport is quite far from the city center.", "example_cn": "机场离市中心挺远的。"},
        {"word": "front", "phonetic": "/frʌnt/", "meaning": "n. 前面", "example_en": "There is a small garden in front of the house.", "example_cn": "房子前面有一个小花园。"},
        {"word": "back", "phonetic": "/bæk/", "meaning": "n./adv. 后面", "example_en": "He stood at the back of the line.", "example_cn": "他站在队伍的最后面。"},

        # 交流与学习动作
        {"word": "speak", "phonetic": "/spiːk/", "meaning": "v. 说，讲话", "example_en": "Can you speak a little louder, please?", "example_cn": "请问你能说大声一点吗？"},
        {"word": "listen", "phonetic": "/ˈlɪsn/", "meaning": "v. 听", "example_en": "You should listen to your doctor's advice.", "example_cn": "你应该听从医生的建议。"},
        {"word": "read", "phonetic": "/riːd/", "meaning": "v. 阅读", "example_en": "I love to read a few pages before bed.", "example_cn": "我喜欢在睡前读几页书。"},
        {"word": "write", "phonetic": "/raɪt/", "meaning": "v. 写", "example_en": "Please write your name at the top of the paper.", "example_cn": "请在纸的顶部写上你的名字。"},
        {"word": "ask", "phonetic": "/ɑːsk/", "meaning": "v. 询问", "example_en": "Don't hesitate to ask if you have any questions.", "example_cn": "如果有任何问题，请随时提问。"},
        {"word": "answer", "phonetic": "/ˈɑːnsə(r)/", "meaning": "v./n. 回答", "example_en": "Nobody could answer the teacher's question.", "example_cn": "没有人能回答老师的问题。"},
        {"word": "call", "phonetic": "/kɔːl/", "meaning": "v. 打电话", "example_en": "I will call you as soon as I arrive.", "example_cn": "我一到就给你打电话。"},
        {"word": "word", "phonetic": "/wɜːd/", "meaning": "n. 单词；词", "example_en": "How do you spell this English word?", "example_cn": "这个英文单词怎么拼？"},
        {"word": "book", "phonetic": "/bʊk/", "meaning": "n. 书", "example_en": "I am reading a fascinating book about history.", "example_cn": "我正在读一本关于历史的迷人书籍。"},
        {"word": "pen", "phonetic": "/pen/", "meaning": "n. 钢笔", "example_en": "Do you have a pen I could borrow?", "example_cn": "你有一支我可以借用的笔吗？"},

        # 高频核心动作
        {"word": "go", "phonetic": "/ɡəʊ/", "meaning": "v. 去", "example_en": "We plan to go to the beach this weekend.", "example_cn": "我们计划这周末去海滩。"},
        {"word": "come", "phonetic": "/kʌm/", "meaning": "v. 来", "example_en": "Are you going to come to the party tonight?", "example_cn": "你今晚会来参加派对吗？"},
        {"word": "make", "phonetic": "/meɪk/", "meaning": "v. 制作", "example_en": "I am going to make some pancakes for breakfast.", "example_cn": "我打算做些煎饼当早餐。"},
        {"word": "take", "phonetic": "/teɪk/", "meaning": "v. 带走；拿", "example_en": "Don't forget to take your umbrella with you.", "example_cn": "别忘了带上你的雨伞。"},
        {"word": "give", "phonetic": "/ɡɪv/", "meaning": "v. 给", "example_en": "Could you give me a hand with this heavy box?", "example_cn": "你能帮我搬一下这个重箱子吗？"},
        {"word": "get", "phonetic": "/ɡet/", "meaning": "v. 得到；获得", "example_en": "I need to get some sleep before the long drive.", "example_cn": "在长途驾驶前我需要睡一觉。"},
        {"word": "find", "phonetic": "/faɪnd/", "meaning": "v. 找到", "example_en": "I finally managed to find my missing keys.", "example_cn": "我终于找到了我丢失的钥匙。"},
        {"word": "lose", "phonetic": "/luːz/", "meaning": "v. 丢失", "example_en": "Try not to lose your passport while traveling.", "example_cn": "旅行时尽量别把护照弄丢了。"},
        {"word": "need", "phonetic": "/niːd/", "meaning": "v. 需要", "example_en": "We need to buy more eggs and milk.", "example_cn": "我们需要买更多的鸡蛋和牛奶。"},
        {"word": "want", "phonetic": "/wɒnt/", "meaning": "v. 想要", "example_en": "I just want to relax on the sofa all day.", "example_cn": "我只想整天在沙发上放松。"},

        # 感官与高级情绪表达
        {"word": "look", "phonetic": "/lʊk/", "meaning": "v. 看", "example_en": "Look at that beautiful bird on the tree!", "example_cn": "看树上那只美丽的鸟！"},
        {"word": "see", "phonetic": "/siː/", "meaning": "v. 看见", "example_en": "I can clearly see the mountains from my window.", "example_cn": "从我的窗户能清楚地看到群山。"},
        {"word": "hear", "phonetic": "/hɪə(r)/", "meaning": "v. 听见", "example_en": "Did you hear that strange noise outside?", "example_cn": "你听到外面那个奇怪的声音了吗？"},
        {"word": "feel", "phonetic": "/fiːl/", "meaning": "v. 感觉", "example_en": "I feel much better after taking a hot shower.", "example_cn": "洗了个热水澡后我感觉好多了。"},
        {"word": "smell", "phonetic": "/smel/", "meaning": "v./n. 闻；气味", "example_en": "These freshly baked cookies smell amazing.", "example_cn": "这些刚烤好的饼干闻起来太棒了。"},
        {"word": "smile", "phonetic": "/smaɪl/", "meaning": "v./n. 微笑", "example_en": "She greeted every customer with a warm smile.", "example_cn": "她用温暖的微笑迎接每一位顾客。"},
        {"word": "cry", "phonetic": "/kraɪ/", "meaning": "v. 哭泣", "example_en": "The sad movie made everyone in the theater cry.", "example_cn": "那部悲伤的电影让电影院里的每个人都哭了。"},
        {"word": "angry", "phonetic": "/ˈæŋɡri/", "meaning": "adj. 生气的", "example_en": "My boss was angry because the report was late.", "example_cn": "老板很生气，因为报告交晚了。"},
        {"word": "afraid", "phonetic": "/əˈfreɪd/", "meaning": "adj. 害怕的", "example_en": "Many people are afraid of speaking in public.", "example_cn": "许多人都害怕在公众面前演讲。"},
        {"word": "excited", "phonetic": "/ɪkˈsaɪtɪd/", "meaning": "adj. 兴奋的", "example_en": "The kids are very excited about the trip to Disneyland.", "example_cn": "孩子们对去迪士尼乐园的旅行感到非常兴奋。"}
    ],
    # 后面可以继续追加 Level 3, Level 4...

# 为了保证程序不报错，其余 19 个关卡我们先用 Level 1 占位兜底
# 当你获取了新的 Level 词库后，可以直接贴进来替换
for lvl in range(2, 21):
    GLOBAL_VOCAB_DB[lvl] = list(GLOBAL_VOCAB_DB[1])
