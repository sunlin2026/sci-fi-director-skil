import streamlit as st
import requests
import json
from docx import Document
# ==================== 设置网页界面 ====================
st.set_page_config(page_title="科幻导演技能 AI", layout="wide")
st.title("🚀 科幻导演 AI 助理")
st.markdown("请输入您的科幻故事，AI会自动分析锚点并生成镜头提示词。")

# ==================== 文件上传 + 文本输入区 ====================
uploaded_file = st.file_uploader("📁 上传您的科幻剧本文件 (支持 .txt, .md 格式)", type=['txt', 'md'])

user_script = ""

if uploaded_file is not None:
    # 读取上传文件的内容
    try:
        stringio = uploaded_file.getvalue().decode("utf-8")
        user_script = stringio
        st.success(f"✅ 已成功读取文件：{uploaded_file.name}")
    except Exception as e:
        st.error(f"文件读取失败，请检查格式：{e}")

# 仍然保留一个手动输入框（防止用户不想传文件，或者传错了）
st.markdown("---")
manual_text = st.text_area("✍️ 或者直接在这里输入/粘贴剧本内容：", height=150, placeholder="如果您不想上传文件，直接在这里输入剧本...")

# 逻辑判断：如果上传了文件，就用文件内容；没上传文件且手动框有字，就用手动输入的内容
if user_script == "" and manual_text != "":
    user_script = manual_text

# ==================== 下面是您的 API Key 配置 ====================

# ==================== 这里配置您的 API Key ====================
# 如果您用的是 DeepSeek，替换成您的 DeepSeek API Key
# 如果您用的是 豆包/OpenAI，替换成对应的 Key
API_KEY ="sk-cafd2efdc3db49e89f7764d1b5406b7b"# <--- 把这里换成您的真实 Key

# ==================== 核心智能逻辑 ====================
def analyze_with_ai(script_text):
    url = "https://api.deepseek.com/v1/chat/completions"  # DeepSeek 接口，如果不用 DeepSeek 请修改
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 这里是让它扮演“科幻导演”的专业指令
    system_prompt = """
    你是一个科幻电影视觉策划师。请根据用户提供的剧本，输出以下内容：
    1. 世界锚点：描述该世界的核心物理/生态规则。
    2. 视觉核心：描述最震撼的场景画面。
    3. 推荐镜头：描述推荐使用的景别、运镜和风格。
    请用中文回答，保持电影级专业术语。
    """
        payload = {
        "model": "deepseek-v4-flash",  # 改用这个最新模型
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"剧本内容：\n{script_text}"}
        ],
        "temperature": 0.7,
        "reasoning_effort": "low"  # 关掉思考模式，更省Token且更快！
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        # 提取AI真正回答的内容
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"出错了：{str(e)}\n\n请检查您的 API Key 是否填写正确。"

# ==================== 运行按钮 ====================
if st.button("🎬 生成分析报告"):
    if user_script.strip():
        with st.spinner("AI 正在思考中，请稍候..."):
            # 把用户输入发给真实AI
            result_text = analyze_with_ai(user_script)
            
            st.success("分析完成！")
            st.markdown(result_text)
    else:
        st.warning("⚠️ 请先写点剧情再点击生成！")
