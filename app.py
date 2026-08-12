import streamlit as st
import requests
import json

# ==================== 设置网页界面 ====================
st.set_page_config(page_title="科幻导演技能 AI", layout="wide")
st.title("🚀 科幻导演 AI 助理")
st.markdown("请输入您的科幻故事，AI会自动分析锚点并生成镜头提示词。")

user_script = st.text_area("📝 请输入剧本或故事梗概：", height=200, placeholder="例如：一个宇航员登陆未知星球，发现了一个巨大的蓝色发光遗迹...")

# ==================== 这里配置您的 API Key ====================
# 如果您用的是 DeepSeek，替换成您的 DeepSeek API Key
# 如果您用的是 豆包/OpenAI，替换成对应的 Key
API_KEY = sk-cafd2efdc3db49e89f7764d1b5406b7b # <--- 把这里换成您的真实 Key

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
        "model": "deepseek-chat", # 如果用豆包，改为 "doubao-pro"
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"剧本内容：\n{script_text}"}
        ],
        "temperature": 0.7
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
