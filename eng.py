import random
import re
import time
import base64
import json
import uuid
from io import BytesIO
from datetime import date
import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client
from vocab_data import GLOBAL_VOCAB_DB

# =========================
# 📱 PWA / iPhone 界面配置
# =========================
st.set_page_config(
    page_title="AI 英语进阶闯关",
    page_icon="📚",
    layout="centered",
)

# 读取 Supabase 配置 (无密直连)
@st.cache_resource(show_spinner=False)
def get_supabase_client():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_ANON_KEY"]
    return create_client(url, key)

supabase = get_supabase_client()

@st.cache_data(show_spinner=False)
def get_all_words():
    return [item for lvl_items in GLOBAL_VOCAB_DB.values() for item in lvl_items]

# ==========================================
# 📱 手机端极限放大适配 CSS
# ==========================================
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
            padding-top: 0.65rem;
            padding-bottom: 1.2rem;
            padding-left: 0.8rem;
            padding-right: 0.8rem;
            max-width: 500px;
        }

        .stButton > button {
            border-radius: 18px !important;
            font-weight: 900 !important;
            padding: 16px 12px !important;
            font-size: 17px !important;
            min-height: 58px !important;
            box-shadow: 0 4px 0px rgba(0, 0, 0, 0.10) !important;
            transition: all 0.1s;
            line-height: 1.35 !important;
        }

        .home-hero { text-align:center; padding:18px 10px 14px; }
        .hero-icon { font-size:48px; line-height:1; margin-bottom:8px; }
        .hero-title { font-size:27px; font-weight:900; color:#303133; }
        .hero-subtitle { font-size:13px; color:#999; margin-top:5px; }
        .level-card {
            display:flex; justify-content:space-between; align-items:center;
            background:linear-gradient(135deg,#eef9ff,#f8fbff);
            border:1px solid #dceff9; border-radius:20px;
            padding:17px 18px; margin:8px 0 10px;
        }
        .level-label { font-size:12px; color:#8d9aa3; font-weight:700; }
        .level-number { font-size:24px; font-weight:900; color:#303133; margin-top:2px; }
        .level-number span { font-size:13px; color:#9aa3aa; font-weight:700; }
        .level-side { text-align:right; font-size:20px; font-weight:900; color:#1cb0f6; line-height:1.1; }
        .level-side span { font-size:11px; color:#9aa3aa; font-weight:700; }
        .progress-caption { display:flex; justify-content:space-between; margin:-5px 2px 12px; font-size:12px; color:#9aa3aa; }
        .progress-caption b { color:#58cc02; }
        .mini-stat {
            background:#fff; border:1px solid #e8e8e8; border-radius:16px;
            padding:10px 8px; text-align:center; margin-bottom:12px;
            font-size:19px;
        }
        .mini-stat b { margin:0 5px; color:#303133; }
        .mini-stat span { font-size:12px; color:#999; }
        
        .stButton > button:active {
            box-shadow: 0 0px 0px rgba(0, 0, 0, 0.1) !important;
            transform: translateY(6px) !important;
        }
        
        .quiz-card {
            background-color: #ffffff;
            border: 2px solid #e5e5e5;
            padding: 20px 18px;
            border-radius: 22px;
            margin-bottom: 12px;
            text-align: center;
        }
        
        .status-bar {
            display: flex; justify-content: space-between; font-size: 18px; font-weight: bold; margin-bottom: 15px; padding: 15px 20px; background: #ffffff; border-radius: 20px; border: 2px solid #e5e5e5;
        }
        
        .section-title { font-size: 16px; color: #afafaf; font-weight: bold; margin-top: 25px; margin-bottom: 15px; text-align: center; }
    </style>
    """,
    unsafe_allow_html=True,
)

def clean_word_for_speech(word):
    text = str(word or "").strip()
    text = re.sub(r"^(?:(?:n|v|adj|adv|prep|conj|pron|num|art|aux|vt|vi|det|phr|phrase)\.?\s+)+", "", text, flags=re.I)
    return text.strip()

def render_word_audio_button(word, button_text="🔊 点此朗读单词", autoplay=False):
    speech_word = clean_word_for_speech(word)
    escaped_word = speech_word.replace("'", "\\'")
    autoplay_script = f"""
    <script>
        if ({'true' if autoplay else 'false'}) {{
            setTimeout(() => {{
                window.speechSynthesis.cancel(); 
                let audio = new Audio('https://dict.youdao.com/dictvoice?audio={escaped_word}&type=2');
                audio.play();
            }}, 300);
        }}
    </script>
    """
    html_code = f"""
    <style>
        body {{ margin: 0; padding: 0; font-family: sans-serif; }}
        button {{ width: 100%; background-color: #ff4b4b; color: white; border: none; padding: 18px; font-size: 18px; font-weight: bold; border-radius: 18px; cursor: pointer; box-shadow: 0 5px 0px rgba(255, 75, 75, 0.3); transition: transform 0.1s, box-shadow 0.1s; }}
        button:active {{ transform: translateY(5px); box-shadow: 0 0px 0px rgba(0,0,0,0.1); }}
    </style>
    <button onclick="window.speechSynthesis.cancel(); new Audio('https://dict.youdao.com/dictvoice?audio={escaped_word}&type=2').play();">
        {button_text}
    </button>
    {autoplay_script}
    """
    components.html(html_code, height=75)

def render_ai_speech_recognition(target_word):
    target_word_lower = target_word.lower().replace("'", "\\'")
    unique_id = int(time.time() * 1000)
    html_code = f"""
    <style>
        body {{ margin: 0; padding: 0; font-family: sans-serif; text-align: center; }}
        button {{ width: 100%; background-color: #ff9600; color: white; border: none; padding: 18px; font-size: 18px; font-weight: bold; border-radius: 18px; cursor: pointer; box-shadow: 0 5px 0px rgba(255, 150, 0, 0.3); transition: transform 0.1s, box-shadow 0.1s, background-color 0.3s; }}
        button:active {{ transform: translateY(5px); box-shadow: 0 0px 0px rgba(0,0,0,0.1) !important; }}
    </style>
    <button id="recordBtn_{unique_id}">🎙️ AI 评测发音</button>
    <p id="statusText_{unique_id}" style="margin-top: 10px; color: #555; font-size: 14px; font-weight: bold;"></p>
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
                    btn.style.boxShadow = "0 5px 0px rgba(88, 204, 2, 0.3)";
                }} else {{
                    statusText.innerHTML = "❌ 识别为: " + speechResult + "，再试一次";
                    btn.style.backgroundColor = "#ff4b4b";
                    btn.style.boxShadow = "0 5px 0px rgba(255, 75, 75, 0.3)";
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
    components.html(html_code, height=105)

def render_blind_listen_button(word, button_text="🔊 播放神秘音频 (常速)", autoplay=False):
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
        button {{ width: 100%; background-color: #9c27b0; color: white; border: none; padding: 18px; font-size: 18px; font-weight: bold; border-radius: 18px; cursor: pointer; box-shadow: 0 5px 0px rgba(156, 39, 176, 0.3); transition: transform 0.1s, box-shadow 0.1s; }}
        button:active {{ transform: translateY(5px); box-shadow: 0 0px 0px rgba(0,0,0,0.1); }}
    </style>
    <script>
        function playTwice() {{
            window.speechSynthesis.cancel();
            new Audio('https://dict.youdao.com/dictvoice?audio={escaped_word}&type=2').play();
        }}
    </script>
    <button onclick="playTwice()">{button_text}</button>
    {autoplay_script}
    """
    components.html(html_code, height=75)

def render_highlight_example(example_en, example_cn):
    escaped_en = example_en.replace("'", "\\'")
    unique_id = int(time.time() * 1000) + random.randint(0, 1000)
    html_code = f"""
    <style>
        body {{ margin: 0; padding: 0; font-family: sans-serif; }}
        .example-card {{ background-color: #f7f7f7; padding: 22px; border-radius: 20px; box-sizing: border-box; width: 100%; border: 2px solid #e5e5e5; margin-bottom: 10px; }}
        .highlight {{ color: #1cb0f6; font-weight: 900; font-size: 115%; background-color: rgba(28, 176, 246, 0.15); border-radius: 6px; padding: 0 4px; transition: all 0.1s; }}
        .word {{ display: inline-block; margin: 0 2px; transition: all 0.1s; color: #4b4b4b; }}
        button:active {{ transform: translateY(5px); box-shadow: 0 0px 0px rgba(0,0,0,0.1) !important; }}
    </style>
    <div class="example-card">
        <div style="font-size: 17px; margin-bottom: 12px; line-height: 1.6;">📖 <b>例句：</b><span id="sentence-box_{unique_id}"></span></div>
        <div style="font-size: 15px; color: #777; margin-bottom: 18px; line-height: 1.5;">💡 <b>翻译：</b>{example_cn}</div>
        <button id="playBtn_{unique_id}" style="width: 100%; background-color: #1cb0f6; color: white; border: none; padding: 18px; font-size: 17px; font-weight: bold; border-radius: 18px; cursor: pointer; box-shadow: 0 5px 0px rgba(28, 176, 246, 0.3); transition: all 0.1s;">🔊 动态朗读例句</button>
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
            utterance.rate = 0.8;
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
    components.html(html_code, height=225)


# ==========================================
# 🚀 降速 1 秒版纯净挂机引擎 (带有暂停与保存的完全体)
# ==========================================
def render_autoplay_study_component(queue, mastered_words, current_lvl):
    return render_autoplay_review_component(
        queue,
        auto_mark=True,
        current_lvl=current_lvl,
        user_id=st.session_state.user.id if "user" in st.session_state else get_or_create_guest_id(),
        initial_mastered=mastered_words,
    )

def render_autoplay_review_component(mastered_words, auto_mark=False, current_lvl=None, user_id=None, initial_mastered=None):
    pool_json = json.dumps(mastered_words, ensure_ascii=False)
    auto_mark_js = "true" if auto_mark else "false"
    current_lvl_js = json.dumps(current_lvl)
    user_id_js = json.dumps(user_id or "")
    supabase_url_js = json.dumps(st.secrets["SUPABASE_URL"] if auto_mark else "")
    supabase_key_js = json.dumps(st.secrets["SUPABASE_ANON_KEY"] if auto_mark else "")

    html = r"""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { font-family: sans-serif; margin: 0; padding: 0; background: transparent; user-select: none; }
        .quiz-card { background: #fff; border: 2px solid #e5e5e5; padding: 25px 18px; border-radius: 22px; margin-bottom: 12px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
        .example-card { background: #f7f7f7; padding: 22px; border-radius: 20px; border: 2px solid #e5e5e5; text-align: left; margin-bottom: 20px; }
        .highlight { color: #1cb0f6; font-weight: 900; background-color: rgba(28, 176, 246, 0.15); border-radius: 6px; padding: 0 4px; }
        button { width: 100%; border: none; padding: 20px; font-size: 19px; font-weight: 900; border-radius: 18px; cursor: pointer; transition: transform 0.1s; margin-bottom: 15px; }
        button:active { transform: translateY(4px); box-shadow: 0 0px 0px transparent !important; }
        .start-btn { background: #1cb0f6; color: #fff; box-shadow: 0 5px 0px rgba(28,176,246,0.3); margin-top: 30px; height: 110px; font-size: 24px; line-height: 1.4; }
        .stop-btn { background: #ff4b4b; color: #fff; box-shadow: 0 5px 0px rgba(255,75,75,0.3); }
        .pause-btn { background: #ff9600; color: #fff; box-shadow: 0 5px 0px rgba(255,150,0,0.3); }
        .progress { font-size: 15px; color: #afafaf; font-weight: bold; margin-bottom: 10px; text-align: right; }
        .status-text { text-align: center; color: #1cb0f6; font-size: 16px; font-weight: bold; min-height: 22px; margin-bottom: 15px; }
    </style>

    <div id="start-screen">
        <button class="start-btn" onclick="startPlay()">▶️ 触摸这里<br>启动极速连读</button>
        <div style="margin-top: 25px; text-align: center;">
            <label style="font-size: 18px; color: #333; font-weight: bold; display: flex; align-items: center; justify-content: center; gap: 10px; cursor: pointer;">
                <input type="checkbox" id="readZhToggleStart" style="width: 24px; height: 24px;" onchange="syncToggle('start')" checked>
                🔊 连读时朗读中文释义
            </label>
        </div>
        <p id="miniText" style="text-align:center; color:#888; font-size:15px; margin-top:25px; line-height:1.5;">点一次开始，之后无需操作 · 自动循环</p>
    </div>

    <div id="play-screen" style="display: none;">
        <div class="progress" id="progress-text"></div>
        <div class="quiz-card">
            <div id="word" style="font-size: 48px; font-weight: 900; color: #303133; margin-bottom: 8px;"></div>
            <div id="phonetic" style="font-size: 18px; color: #afafaf; margin-bottom: 12px;"></div>
            <div id="meaning" style="font-size: 24px; font-weight: bold; color: #1cb0f6;"></div>
        </div>
        
        <div class="example-card">
            <div style="font-size: 17px; margin-bottom: 12px; line-height: 1.6; color: #333;">
                📖 <b>例句：</b><span id="example_en"></span>
            </div>
            <div style="font-size: 16px; color: #777; line-height: 1.5;">
                💡 <b>翻译：</b><span id="example_cn"></span>
            </div>
        </div>

        <div style="margin-bottom: 20px; text-align: center;">
            <label style="font-size: 16px; color: #555; font-weight: bold; display: flex; align-items: center; justify-content: center; gap: 8px; cursor: pointer;">
                <input type="checkbox" id="readZhTogglePlay" style="width: 20px; height: 20px;" onchange="syncToggle('play')" checked>
                🔊 连读时朗读中文释义
            </label>
        </div>

        <div class="status-text" id="status">正在准备…</div>
        <button class="pause-btn" id="pauseBtn" onclick="pauseToggle()">⏸ 暂停挂机 (保存进度)</button>
        <button class="stop-btn" onclick="saveAndExit()">⏹️ 退出挂机并返回</button>
    </div>

    <script>
      const pool = __POOL_JSON__;
      const autoMark = __AUTO_MARK__;
      const currentLvl = __CURRENT_LVL__;
      const userId = __USER_ID__;
      const supabaseUrl = __SUPABASE_URL__;
      const supabaseKey = __SUPABASE_KEY__;
      
      const seen = new Set();
      const queue = pool.filter(x => { const w = String(x.word||'').trim().toLowerCase(); if(!w || seen.has(w)) return false; seen.add(w); return true; });
      
      let index = -1, running = false, token = 0, timer = null, current = null, currentAudio = null;
      let mastered = __MASTERED_JSON__;

      if(autoMark) {
          document.getElementById('miniText').innerText = "⚠️ 必须由您的手指亲自点击一次\n才能解开静音限制并自动保存进度！";
      }

      function syncToggle(source) {
          let checked = source === 'start' ? document.getElementById('readZhToggleStart').checked : document.getElementById('readZhTogglePlay').checked;
          document.getElementById('readZhToggleStart').checked = checked;
          document.getElementById('readZhTogglePlay').checked = checked;
      }

      function clean() {
          if(timer) { clearTimeout(timer); timer=null; }
          window.speechSynthesis.cancel();
          if(currentAudio) { currentAudio.pause(); currentAudio=null; }
          token++;
      }

      function speak(text, lang, rate, t) {
          return new Promise(resolve => {
              if(!running || t !== token) return resolve();
              const value = String(text||"").trim();
              if(!value) return resolve();
              
              if(lang === "en-US") {
                  currentAudio = new Audio("https://dict.youdao.com/dictvoice?audio=" + encodeURIComponent(value) + "&type=2");
                  currentAudio.preload = "auto";
                  let finished = false;
                  const done = () => { if(finished) return; finished=true; currentAudio=null; resolve(); };
                  currentAudio.onended = done;
                  currentAudio.onerror = () => {
                      if(finished) return;
                      finished = true;
                      currentAudio = null;
                      const u = new SpeechSynthesisUtterance(value);
                      u.lang = "en-US";
                      u.rate = Math.min(rate||0.8, 0.8);
                      u.onend = resolve; u.onerror = resolve;
                      window.speechSynthesis.cancel();
                      if(running && t===token) window.speechSynthesis.speak(u); else resolve();
                  };
                  const p = currentAudio.play();
                  if(p && p.catch) p.catch(() => currentAudio.onerror());
              } else {
                  const u = new SpeechSynthesisUtterance(value);
                  u.lang = lang; u.rate = rate;
                  u.onend = resolve; u.onerror = resolve;
                  window.speechSynthesis.speak(u);
              }
          });
      }

      async function saveProgress() {
          if(!autoMark || !mastered.length) return;
          try {
              let url = new URL(window.parent.location.href);
              url.searchParams.set("lvl_" + currentLvl, mastered.join(","));
              url.searchParams.set("lvl", currentLvl);
              window.parent.history.replaceState(null, "", url.toString());
          } catch(e) {}
          
          const endpoint = supabaseUrl.replace(/\/$/, "") + "/rest/v1/user_profiles?user_id=eq." + encodeURIComponent(userId);
          try {
              const r = await fetch(endpoint, {
                  method: "PATCH",
                  headers: { "apikey": supabaseKey, "Authorization": "Bearer " + supabaseKey, "Content-Type": "application/json", "Prefer": "return=minimal" },
                  body: JSON.stringify({ grade: currentLvl, mastered_words: mastered.join(",") })
              });
              if(!r.ok) throw new Error(r.status);
          } catch(e) {
              throw e;
          }
      }

      function show(item) {
          document.getElementById('word').innerText = item.word || "";
          document.getElementById('phonetic').innerText = item.phonetic || "";
          document.getElementById('meaning').innerText = item.meaning || "";
          
          let safeWord = String(item.word||"").replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
          let exEn = String(item.example_en||"").replace(new RegExp(`\\b${safeWord}\\b`, 'gi'), '<span class="highlight">$&</span>');
          document.getElementById('example_en').innerHTML = exEn;
          document.getElementById('example_cn').innerText = item.example_cn || "";
          
          if(autoMark) {
              document.getElementById('progress-text').innerText = `已连读: ${index + 1} / ${queue.length} 词`;
          } else {
              document.getElementById('progress-text').innerText = `无限循环磨耳模式`;
          }
      }

      function speechWord(text) { return String(text||"").trim().replace(/^(?:(?:n|v|adj|adv|prep|conj|pron|num|art|aux|vt|vi|det|phr|phrase)\.?\s+)+/i,"").trim(); }
      function speechChinese(text) {
          return String(text||"").trim()
            .replace(/(^|[；;、,，\n])\s*(?:n|v|adj|adv|prep|conj|pron|num|art|aux|vt|vi|det|phr|phrase)\.?\s*/gi,"$1")
            .replace(/(^|[；;、,，\n])\s*(?:名词|动词|形容词|副词|介词|连词|代词|数词|冠词|助动词|及物动词|不及物动词)\s*[:：]?\s*/g,"$1")
            .replace(/\s{2,}/g," ").trim();
      }

      async function play() {
          const t = token;
          if(!running || !current) return;
          
          document.getElementById('status').innerText = "🔊 正在朗读…";
          await speak(speechWord(current.word), "en-US", 0.8, t);
          if(!running || t!==token) return;
          
          if(document.getElementById('readZhTogglePlay').checked && current.meaning) {
              await speak(speechChinese(current.meaning), "zh-CN", 1.0, t);
          }
          if(!running || t!==token) return;
          
          timer = setTimeout(() => next(), 1000);
      }

      function next() {
          if(!running) return;
          if(current && autoMark) {
              const w = String(current.word||"").trim();
              if(w && !mastered.includes(w)) mastered.push(w);
              saveProgress().catch(e=>{});
          }
          if (autoMark && index + 1 >= queue.length) {
              saveAndExit();
              return;
          }
          
          if(autoMark) {
              index++;
              current = queue[index];
          } else {
              current = queue[Math.floor(Math.random() * queue.length)];
          }
          
          show(current);
          clean();
          running = true;
          play();
      }

      function startPlay() {
          if(!queue.length) return;
          running = true;
          document.getElementById('start-screen').style.display = 'none';
          document.getElementById('play-screen').style.display = 'block';
          index = -1;
          next();
      }

      // ===========================
      // 🚀 核心：终极暂停功能 
      // ===========================
      function pauseToggle() {
          let btn = document.getElementById('pauseBtn');
          let status = document.getElementById('status');
          
          if(!running) {
              // ▶️ 用户点击：恢复播放
              running = true;
              if(window.speechSynthesis.paused) window.speechSynthesis.resume();
              if(currentAudio) currentAudio.play();
              
              btn.innerHTML = "⏸ 暂停挂机 (保存进度)";
              btn.style.backgroundColor = "#ff9600";
              btn.style.boxShadow = "0 5px 0px rgba(255,150,0,0.3)";
              status.innerText = "🔊 正在朗读…";
              
              // 防止意外卡死，强行打火重启
              if(!currentAudio && !window.speechSynthesis.speaking && !timer) { play(); }
          } else {
              // ⏸ 用户点击：暂停播放
              running = false;
              window.speechSynthesis.pause();
              if(currentAudio) currentAudio.pause();
              if(timer) { clearTimeout(timer); timer = null; }
              
              btn.innerHTML = "▶️ 继续连读";
              btn.style.backgroundColor = "#58cc02";
              btn.style.boxShadow = "0 5px 0px rgba(88,204,2,0.3)";
              
              if(autoMark) {
                  status.innerText = "⏳ 正在安全保存进度...";
                  saveProgress().then(() => {
                      status.innerText = "✅ 进度已保存！随时可继续";
                  }).catch(() => {
                      status.innerText = "⚠️ 进度已保存在本地，稍后自动同步";
                  });
              } else {
                  status.innerText = "⏸ 已暂停";
              }
          }
      }

      function saveAndExit() {
          running = false;
          clean();
          if(autoMark) {
              document.getElementById('status').innerText = "⏳ 正在保存退出...";
              saveProgress().then(() => {
                  let url = new URL(window.parent.location.href);
                  url.searchParams.set("lvl_" + currentLvl, mastered.join(","));
                  url.searchParams.set("lvl", currentLvl);
                  url.searchParams.set("exit_autoplay", "1");
                  window.parent.location.replace(url.toString());
              }).catch(() => {
                  let url = new URL(window.parent.location.href);
                  url.searchParams.set("exit_autoplay", "1");
                  window.parent.location.replace(url.toString());
              });
          } else {
              let url = new URL(window.parent.location.href);
              url.searchParams.set("exit_autoplay", "1");
              window.parent.location.replace(url.toString());
          }
      }
    </script>
    """
    html = html.replace("__POOL_JSON__", pool_json)
    html = html.replace("__MASTERED_JSON__", json.dumps(list(initial_mastered if initial_mastered is not None else mastered_words), ensure_ascii=False))
    html = html.replace("__AUTO_MARK__", auto_mark_js)
    html = html.replace("__CURRENT_LVL__", current_lvl_js)
    html = html.replace("__USER_ID__", user_id_js)
    html = html.replace("__SUPABASE_URL__", supabase_url_js)
    html = html.replace("__SUPABASE_KEY__", supabase_key_js)
    
    components.html(html, height=800)

def render_mobile_study_component(queue, mastered_words, current_lvl):
    queue_json = json.dumps(queue, ensure_ascii=False)
    mastered_json = json.dumps([w["word"] for w in mastered_words], ensure_ascii=False)
    supabase_url_js = json.dumps(st.secrets["SUPABASE_URL"])
    supabase_key_js = json.dumps(st.secrets["SUPABASE_ANON_KEY"])
    user_id_js = json.dumps(st.session_state.user.id if "user" in st.session_state else get_or_create_guest_id())

    html = f"""
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: sans-serif; margin: 0; padding: 0; background: transparent; user-select: none; }}
            .card {{ background:#fff; border:2px solid #e5e5e5; padding:22px 18px; border-radius:22px; margin-bottom:12px; text-align:center; box-shadow:0 4px 10px rgba(0,0,0,.05); }}
            .example {{ background:#f7f7f7; padding:20px; border-radius:20px; border:2px solid #e5e5e5; text-align:left; margin-bottom:14px; line-height:1.6; }}
            .highlight {{ color:#1cb0f6; font-weight:900; background:rgba(28,176,246,.15); border-radius:6px; padding:0 4px; }}
            .status {{ min-height:22px; text-align:center; color:#777; font-size:14px; font-weight:bold; margin:8px 0; }}
            button {{ width:100%; border:none; padding:18px; font-size:18px; font-weight:900; border-radius:18px; cursor:pointer; margin-top:9px; }}
            button:active {{ transform:translateY(4px); }}
            .start {{ background:#1cb0f6; color:#fff; box-shadow:0 5px 0 rgba(28,176,246,.3); font-size:21px; padding:22px; }}
            .audio {{ background:#9c27b0; color:#fff; box-shadow:0 5px 0 rgba(156,39,176,.25); }}
            .blur {{ background:#ff9600; color:#fff; box-shadow:0 5px 0 rgba(255,150,0,.25); }}
            .master {{ background:#58cc02; color:#fff; box-shadow:0 5px 0 rgba(88,204,2,.25); }}
            .kill {{ background:#777; color:#fff; box-shadow:0 5px 0 rgba(0,0,0,.12); }}
            .row {{ display:flex; gap:10px; }}
            .row button {{ flex:1; }}
        </style>
    </head>
    <body>
        <div id="start-screen">
            <button class="start" id="startBtn">▶️ 开始学习并朗读</button>
        </div>

        <div id="study-screen" style="display:none;">
            <div style="text-align:right;color:#888;font-size:14px;font-weight:bold;margin-bottom:8px;" id="progress"></div>
            <div class="card">
                <div id="word" style="font-size:46px;font-weight:900;color:#303133;margin-bottom:6px;"></div>
                <div id="phonetic" style="font-size:17px;color:#afafaf;margin-bottom:10px;"></div>
                <div id="meaning" style="font-size:22px;font-weight:bold;color:#1cb0f6;"></div>
            </div>
            <div class="example">
                <div style="font-size:17px;margin-bottom:8px;color:#333;">📖 <b>例句：</b><span id="example_en"></span></div>
                <div style="font-size:15px;color:#777;">💡 <b>翻译：</b><span id="example_cn"></span></div>
            </div>
            <div class="status" id="status"></div>
            <button class="audio" id="replayBtn">🔊 再听一次</button>
            <div class="row">
                <button class="blur" id="blurBtn">❌ 模糊 · 重练</button>
                <button class="master" id="masterBtn">✔ 认识 · 下一个</button>
            </div>
            <button class="kill" id="killBtn">🗑️ 太简单，斩掉它</button>
        </div>

        <audio id="wordAudio" preload="auto" playsinline></audio>

        <script>
            const remaining = {queue_json};
            const mastered = {mastered_json};
            const currentLvl = {current_lvl};
            const supabaseUrl = {supabase_url_js};
            const supabaseKey = {supabase_key_js};
            const userId = {user_id_js};
            let currentItem = null;
            let isPlaying = false;
            let audioToken = 0;

            const audio = document.getElementById("wordAudio");
            const preloadAudio = document.createElement("audio");
            preloadAudio.preload = "auto";
            preloadAudio.playsInline = true;
            let preloadedWord = "";
            const startScreen = document.getElementById("start-screen");
            const studyScreen = document.getElementById("study-screen");
            const status = document.getElementById("status");

            function cleanWordForSpeech(text) {{
                return String(text || "").trim().replace(/^(?:(?:n|v|adj|adv|prep|conj|pron|num|art|aux|vt|vi|det|phr|phrase)\.?\s+)+/i, "").trim();
            }}

            function audioUrl(word) {{
                return "https://dict.youdao.com/dictvoice?audio=" + encodeURIComponent(cleanWordForSpeech(word)) + "&type=2";
            }}

            function preloadNext() {{
                const nextItem = remaining[0];
                if (!nextItem || !nextItem.word || nextItem.word === preloadedWord) return;
                preloadedWord = nextItem.word;
                preloadAudio.src = audioUrl(nextItem.word);
                preloadAudio.load();
            }}

            function showItem(item) {{
                currentItem = item;
                document.getElementById("progress").innerText =
                    `本关已掌握：${{mastered.length}} 词 · 剩余：${{remaining.length}} 词`;
                document.getElementById("word").innerText = item.word || "";
                document.getElementById("phonetic").innerText = item.phonetic || "";
                document.getElementById("meaning").innerText = item.meaning || "";

                const safe = String(item.word || "").replace(/[.*+?^${{}}()|[\\]\\\\]/g, "\\\\$&");
                document.getElementById("example_en").innerHTML = String(item.example_en || "").replace(
                    new RegExp("\\\\b" + safe + "\\\\b", "gi"),
                    '<span class="highlight">$&</span>'
                );
                document.getElementById("example_cn").innerText = item.example_cn || "";
            }}

            function playCurrent() {{
                if (!isPlaying || !currentItem) return;
                audioToken++;
                const token = audioToken;
                window.speechSynthesis.cancel();
                audio.pause();
                const currentUrl = audioUrl(currentItem.word);
                if (preloadedWord === currentItem.word && preloadAudio.src) {{
                    audio.src = preloadAudio.src;
                    preloadedWord = "";
                }} else {{
                    audio.src = currentUrl;
                    audio.load();
                }}
                status.innerText = "🔊 正在播放：" + currentItem.word;

                audio.onended = () => {{
                    if (token !== audioToken || !isPlaying) return;
                    status.innerText = "";
                }};

                audio.onerror = () => fallbackSpeech(token);
                const p = audio.play();
                if (p && p.catch) p.catch(() => fallbackSpeech(token));
            }}

            function fallbackSpeech(token) {{
                if (!isPlaying || token !== audioToken || !currentItem) return;
                const u = new SpeechSynthesisUtterance(cleanWordForSpeech(currentItem.word));
                u.lang = "en-US";
                u.rate = 0.8;
                u.onend = () => {{ if (token === audioToken) status.innerText = ""; }};
                u.onerror = () => {{ if (token === audioToken) status.innerText = ""; }};
                window.speechSynthesis.cancel();
                window.speechSynthesis.speak(u);
            }}

            function startStudy() {{
                if (!remaining.length) {{ finishAndSave(); return; }}
                startScreen.style.display = "none";
                studyScreen.style.display = "block";
                isPlaying = true;
                currentItem = remaining.shift();
                showItem(currentItem);
                playCurrent();
                preloadNext();
            }}

            async function saveMasteredProgress() {{
                const masteredStr = mastered.join(",");
                const endpoint = supabaseUrl.replace(/\/$/, "") + "/rest/v1/user_profiles?user_id=eq." + encodeURIComponent(userId);
                try {{
                    const response = await fetch(endpoint, {{
                        method: "PATCH",
                        headers: {{
                            "apikey": supabaseKey,
                            "Authorization": "Bearer " + supabaseKey,
                            "Content-Type": "application/json",
                            "Prefer": "return=minimal"
                        }},
                        body: JSON.stringify({{ grade: currentLvl, mastered_words: masteredStr }})
                    }});
                    if (!response.ok) throw new Error("HTTP " + response.status);
                    status.innerText = "✓ 进度已保存";
                    setTimeout(() => {{ if (status.innerText === "✓ 进度已保存") status.innerText = ""; }}, 1000);
                }} catch (e) {{
                    status.innerText = "⚠️ 网络稍慢，结束时会再次保存";
                }}
            }}

            function next(action) {{
                if (!isPlaying || !currentItem) return;

                if (action === "master" || action === "kill") {{
                    if (!mastered.includes(currentItem.word)) mastered.push(currentItem.word);
                    if (action === "master") saveMasteredProgress();
                }} else if (action === "blur") {{
                    remaining.push(currentItem);
                }}

                if (!remaining.length) {{
                    finishAndSave();
                    return;
                }}

                currentItem = remaining.shift();
                showItem(currentItem);
                playCurrent();
                preloadNext();
            }}

            function replay() {{
                if (!isPlaying || !currentItem) return;
                playCurrent();
            }}

            function finishAndSave() {{
                isPlaying = false;
                window.speechSynthesis.cancel();
                audio.pause();
                const url = new URL(window.parent.location.href);
                url.searchParams.set("lvl_" + currentLvl, mastered.join(","));
                url.searchParams.set("lvl", String(currentLvl));
                url.searchParams.set("exit_autoplay", "1");
                window.parent.location.replace(url.toString());
            }}

            document.getElementById("startBtn").addEventListener("click", startStudy);
            document.getElementById("replayBtn").addEventListener("click", replay);
            document.getElementById("blurBtn").addEventListener("click", () => next("blur"));
            document.getElementById("masterBtn").addEventListener("click", () => next("master"));
            document.getElementById("killBtn").addEventListener("click", () => next("kill"));
        </script>
    </body>
    </html>
    """
    components.html(html, height=690)

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

def sync_progress_to_cloud(user_id, level, mastered_dict):
    try:
        mastered_words_list = [w['word'] for w in mastered_dict.get(level, [])]
        mastered_str = ",".join(mastered_words_list)
        
        st.query_params[f"lvl_{level}"] = mastered_str
        st.query_params["lvl"] = str(level)
        
        res = supabase.table("user_profiles").select("user_id").eq("user_id", user_id).execute()
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

class AutoLoginUser:
    def __init__(self, uid):
        self.id = uid

def get_or_create_guest_id():
    existing = str(st.query_params.get("uid", "")).strip()
    if existing and len(existing) <= 64:
        return existing
    new_id = "guest_" + uuid.uuid4().hex
    st.query_params["uid"] = new_id
    return new_id

# === 初始化 Session State ===
if "level" not in st.session_state:
    st.session_state.level = 1
if "queues" not in st.session_state:
    st.session_state.queues = {}
if "mastered" not in st.session_state:
    st.session_state.mastered = {lvl: [] for lvl in range(1, 21)}

def ensure_level_queue(level):
    if level not in st.session_state.queues:
        q = list(GLOBAL_VOCAB_DB.get(level, []))
        random.shuffle(q)
        st.session_state.queues[level] = q
    return st.session_state.queues[level]

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
if "study_history" not in st.session_state:
    st.session_state.study_history = []
if "auto_play" not in st.session_state:
    st.session_state.auto_play = False

# 处理挂机返回
if "exit_autoplay" in st.query_params:
    st.session_state.auto_play = False
    del st.query_params["exit_autoplay"]

# ==========================================
# 🛑 彻底干掉验证，隐身自动读档！
# ==========================================
if "user" not in st.session_state:
    st.session_state.user = AutoLoginUser(get_or_create_guest_id())
    
    try:
        profile = supabase.table("user_profiles").select("*").eq("user_id", st.session_state.user.id).execute()
        if len(profile.data) > 0:
            restore_progress_from_db(profile.data)
    except Exception:
        pass
        
    if "lvl" in st.query_params:
        try:
            url_lvl = int(st.query_params["lvl"])
            st.session_state.level = url_lvl
            param_key = f"lvl_{url_lvl}"
            if param_key in st.query_params:
                saved_str = st.query_params[param_key]
                if saved_str:
                    saved_words = saved_str.split(",")
                    full_level_words = GLOBAL_VOCAB_DB.get(url_lvl, [])
                    st.session_state.mastered[url_lvl] = [w for w in full_level_words if w["word"] in saved_words]
                    remaining = [w for w in full_level_words if w["word"] not in saved_words]
                    random.shuffle(remaining)
                    st.session_state.queues[url_lvl] = remaining
                    sync_progress_to_cloud(st.session_state.user.id, url_lvl, st.session_state.mastered)
        except Exception:
            pass
        

current_lvl = st.session_state.level
current_queue = ensure_level_queue(current_lvl)
mastered_list = st.session_state.mastered[current_lvl]
all_learned_pool = mastered_list 

if st.session_state.page != "home":
    st.markdown(f"""
    <div class='status-bar'>
        <span style='color: #ff9600;'><span class='anim-fire'>🔥</span> 连胜: {st.session_state.streak} 天</span>
        <span style='color: #ff4b4b; letter-spacing: 2px;'><span class='anim-heart'>{'❤️'*st.session_state.hearts}</span>{'🤍'*(5-st.session_state.hearts)}</span>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.page == "home":
    learned = len(mastered_list)
    remaining_count = len(current_queue)
    progress_pct = min(learned / 100.0, 1.0)

    st.markdown("""
    <div class="home-hero">
        <div class="hero-icon">🦉</div>
        <div class="hero-title">每日英语进阶</div>
        <div class="hero-subtitle">每天学一点，慢慢把英语变成习惯</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="level-card">
        <div>
            <div class="level-label">当前关卡</div>
            <div class="level-number">Level {current_lvl} <span>/ 20</span></div>
        </div>
        <div class="level-side">{learned}/100<br><span>已掌握</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.progress(progress_pct)
    st.markdown(
        f"<div class='progress-caption'><span>本关进度</span><b>{learned}%</b></div>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='mini-stat'>🔥<b>{st.session_state.streak}</b><span>天连胜</span></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='mini-stat'>❤️<b>{st.session_state.hearts}</b><span>颗红心</span></div>", unsafe_allow_html=True)

    if remaining_count:
        if st.button(f"🚀 继续学习  ·  剩 {remaining_count} 词", use_container_width=True, type="primary"):
            st.session_state.study_history.clear()
            st.session_state.page = "study"
            st.rerun()
    else:
        st.success("🎉 本关 100 个单词已经全部掌握！")
        if current_lvl < 20:
            if st.button("⬆️ 进入下一关", use_container_width=True, type="primary"):
                st.session_state.level += 1
                ensure_level_queue(st.session_state.level)
                st.session_state.study_history.clear()
                st.session_state.page = "study"
                st.rerun()

    if st.button("🔁 重温已学单词", use_container_width=True):
        st.session_state.page = "review"
        st.session_state.pop("review_current", None)
        st.rerun()

    st.markdown("<div class='section-title'>— 🎯 专项测验 —</div>", unsafe_allow_html=True)
    st.caption("用不同方式检查自己是不是真的记住了。")

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

else:
    if st.button("⬅️ 返回主页", type="secondary"):
        st.session_state.page = "home"
        st.session_state.pop("quiz_current", None)
        st.session_state.pop("quiz_answered", None)
        st.session_state.pop("quiz_current", None)
        st.session_state.pop("review_current", None)
        st.session_state.study_history.clear()
        st.session_state.auto_play = False
        st.rerun()

    # ==========================================
    # 📚 核心背单词模式 
    # ==========================================
    if st.session_state.page == "study":
        st.markdown(f"<div style='text-align:center;margin:4px 0 10px;color:#999;font-size:13px;'>Level {current_lvl} · 剩余 {len(current_queue)} 词</div>", unsafe_allow_html=True)

        if st.session_state.auto_play:
            if current_queue:
                render_autoplay_study_component(current_queue, mastered_list, current_lvl)
            else:
                st.success("🎉 当前关卡已经没有新词啦！")
                st.session_state.auto_play = False
        else:
            if st.button("🎧 挂机听 · 自动连读", use_container_width=True, type="primary"):
                st.session_state.auto_play = True
                st.rerun()

            st.caption("不想一直点按钮？开启挂机听，单词会自动连续朗读。")

            progress_pct = min(len(mastered_list) / 100.0, 1.0)
            st.progress(progress_pct)
            st.markdown(
                f"<p style='text-align: right; font-size: 12px; color: #58cc02; font-weight: bold;'>"
                f"Level {current_lvl} 进度: {len(mastered_list)}/100</p>",
                unsafe_allow_html=True
            )

            if current_queue:
                render_mobile_study_component(current_queue, mastered_list, current_lvl)
            else:
                if st.session_state.study_history:
                    if st.button("⏪ 哎呀点错了！返回上一个单词", use_container_width=True):
                        action, word_data, added_to_mastered = st.session_state.study_history.pop()
                        if action == "blur":
                            if current_queue and current_queue[-1] == word_data:
                                current_queue.pop()
                            current_queue.insert(0, word_data)
                        elif action == "master":
                            if added_to_mastered and word_data in mastered_list:
                                mastered_list.remove(word_data)
                            current_queue.insert(0, word_data)
                            sync_progress_to_cloud(
                                st.session_state.user.id,
                                st.session_state.level,
                                st.session_state.mastered
                            )
                        st.rerun()

                if current_lvl < 20:
                    st.success(f"🎉 太棒了！Level {current_lvl} 完美通关！")
                    if st.button(
                        f"🚀 冲刺进入 Level {current_lvl + 1}",
                        use_container_width=True,
                        type="primary"
                    ):
                        st.session_state.study_history.clear()
                        st.session_state.level += 1
                        sync_progress_to_cloud(
                            st.session_state.user.id,
                            st.session_state.level,
                            st.session_state.mastered
                        )
                        st.rerun()
                else:
                    st.success("🏆 恭喜你通关全部 20 个 Level！英语词汇终极大师！")
                    if st.button("🔄 重新开始挑战", use_container_width=True):
                        st.session_state.study_history.clear()
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
                    
                    all_flat_words = get_all_words()
                    
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

                if st.session_state.get("quiz_answered", False):
                    selected = st.session_state.selected_option
                    
                    render_word_audio_button(qc["word"], "🔊 再次朗读单词", autoplay=True)

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

                else:
                    if q_type == "normal":
                        render_word_audio_button(qc["word"], "🔊 点击听音", autoplay=True)
                        st.markdown(f"<div class='quiz-card' style='margin-top:10px;'><div style='font-size:38px; font-weight:bold; color:#303133;'>{qc['word']}</div></div>", unsafe_allow_html=True)
                        
                    elif q_type == "listen":
                        st.markdown("<h4 style='text-align:center; color:#9c27b0;'>🎧 盲听辨义</h4>", unsafe_allow_html=True)
                        render_blind_listen_button(qc["word"], "🔊 播放神秘音频 (常速)", autoplay=True)
                        st.markdown(f"<div class='quiz-card' style='margin-top:10px;'><div style='font-size:20px; font-weight:bold; color:#afafaf;'>❓❓❓</div></div>", unsafe_allow_html=True)

                    elif q_type == "fill_blank":
                        st.markdown("<h4 style='text-align:center; color:#1cb0f6;'>🔤 语境填空</h4>", unsafe_allow_html=True)
                        masked_en = re.sub(r'(?i)\b' + re.escape(qc['word']) + r'\b', '____', qc['example_en'])
                        st.markdown(f"<div class='quiz-card' style='margin-top:10px;'><div style='font-size:22px; font-weight:bold; color:#303133; line-height: 1.5;'>{masked_en}</div><div style='font-size:14px; color:#afafaf; margin-top:8px;'>{qc['example_cn']}</div></div>", unsafe_allow_html=True)

                    elif q_type == "spell":
                        st.markdown("<h4 style='text-align:center; color:#1cb0f6;'>✍️ 串字挑战</h4>", unsafe_allow_html=True)
                        render_word_audio_button(qc["word"], "🔊 听发音拼写", autoplay=True)
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
        st.markdown(f"<div style='text-align:center;margin:4px 0 12px;color:#999;font-size:13px;'>🔁 本关已掌握 {len(mastered_list)} 词</div>", unsafe_allow_html=True)
        if not mastered_list:
            st.info("📚 当前关卡还没有掌握单词。先去学习几个，再回来重温吧！")
            if st.button("🚀 去学习新词", use_container_width=True, type="primary"):
                st.session_state.page = "study"
                st.rerun()
        else:
            if st.session_state.auto_play:
                render_autoplay_review_component(mastered_list)
            else:
                if st.button("🎧 挂机听 · 自动连读", use_container_width=True, type="primary"):
                    st.session_state.auto_play = True
                    st.rerun()
                
                if "review_current" not in st.session_state:
                    st.session_state.review_current = random.choice(mastered_list)

                rc = st.session_state.review_current
                
                render_word_audio_button(rc["word"], "🔊 点此朗读单词", autoplay=True)

                st.markdown(
                    f"""
                        <div class="quiz-card" style="margin-bottom: 12px; margin-top: 10px;">
                            <div style="font-size: 42px; font-weight: bold; color: #303133; margin-bottom: 4px;">{rc['word']}</div>
                            <div style="font-size: 14px; color: #afafaf; margin-bottom: 10px;">{rc['phonetic']}</div>
                            <div style="font-size: 20px; font-weight: bold; color: #1cb0f6;">{rc['meaning']}</div>
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
