import streamlit as st
import requests
import json

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
API_KEY = st.secrets["OPENAI_API_KEY"]

# ==================== 核心智能逻辑 ====================
def analyze_with_ai(script_text):
    url = "https://api.deepseek.com/v1/chat/completions"  # DeepSeek 接口，如果不用 DeepSeek 请修改
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
        # 这里是让它扮演"科幻导演"的专业指令
system_prompt = """
请参考您知识库中的"8大科幻视觉流派参考库"（已更新为8个流派），在每一步（世界锚点、视觉核心、提示词）中，**必须明确写出**本片主要参考了**8大流派中的哪几个**，并以此风格为基础进行创作。

你是一个顶级的科幻电影视觉策划师。请根据用户提供的剧本，输出一份专业的视觉执行方案。
请务必按以下格式和板块输出，每个部分都要详细：

1. 人物定位与介绍：分析主要角色的性格特征、职业背景、核心动机和人物弧光。

2. 世界锚点：描述该世界的核心物理规律、生态规则或科技设定。

3. 视觉核心与画面描述：描绘故事中最震撼、最核心的场景画面（需包含色彩、构图、光影、质感描写）。

4. AI 绘画提示词 (Midjourney/SD/即梦/小云雀 通用)：
- 必须提供 3 个核心画面的提示词。
- 每个核心画面必须包含以下 4 个独立的内容模块，并严格按顺序输出：

【模块1：中文版提示词】
（请用详细中文描述主体、环境、景别、光影、风格，并融入已确定的风格流派）

【模块2：中文版负面提示词】
（请紧跟中文版提示词下方写出）：
最低质量，低画质，变形，扭曲，结构错误，解剖错误，多余肢体，缺失肢体，漂浮肢体，融合的手部，变异，畸形，难看，模糊，残缺，文字，水印，签名，丑陋的面部。

【模块3：英文版提示词】
（请提供专业英文 Prompt，纯英文，用逗号分隔）

【模块4：英文版负面提示词】
（请紧跟英文版提示词下方写出）：
(worst quality, low quality:1.4), deformed, distorted, disfigured, poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4), disconnected limbs, mutation, mutated, ugly, disgusting, blurry, amputation, out of focus, text, watermarks, signature, logo, ugly face.
5. 视频分镜脚本 (Storyboard)：
- 提供 3 个核心分镜。
- 每个分镜需包含：景别（如大远景）、运镜（如缓慢推入/平移）、时长（秒）、画面内容描述。

【极重要指令】：请严格按照第1至第5条的五个板块输出，千万不要在开头和结尾添加任何寒暄语或废话。输出完成后直接结束！
    """

def analyze_with_ai(script_text):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # 这里是让它扮演"科幻导演"的专业指令
    system_prompt = """
请参考您知识库中的"7大科幻视觉流派参考库"，在每一步（世界锚点、视觉核心、提示词）中，明确指出本片主要参考了哪个流派，并以此风格为基础进行创作。

你是一个顶级的科幻电影视觉策划师。请根据用户提供的剧本，输出一份专业的视觉执行方案。

请务必按以下格式和板块输出，每个部分都要详细：

1. 人物定位与介绍：分析主要角色的性格特征、职业背景、核心动机和人物弧光。

2. 世界锚点：描述该世界的核心物理规律、生态规则或科技设定。

3. 视觉核心与画面描述：描绘故事中最震撼、最核心的场景画面（需包含色彩、构图、光影、质感描写）。

4. AI 绘画提示词 (Midjourney/SD/即梦/小云雀 通用)：
- 必须提供 3 个核心画面。
- 每个画面需要分别提供：
  * 【中文版】：详细的中文画面描述（包含主体、环境、景别、光影、风格）。
  * 【英文版】：对应的专业英文 Prompt，用于 Midjourney、SD 等海外工具（必须为纯英文，用逗号分隔）。

5. 视频分镜脚本 (Storyboard)：
- 提供 3 个核心分镜。
- 每个分镜需包含：景别（如大远景）、运镜（如缓慢推入/平移）、时长（秒）、画面内容描述。

【极重要指令】：请严格按照第1至第5条的五个板块输出，千万不要在开头和结尾添加任何寒暄语或废话。输出完成后直接结束！
    """

    payload = {
        "model": "deepseek-v4-flash",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"剧本内容：\n{script_text}"}
        ],
        "temperature": 0.7,
        "reasoning_effort": "low"
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
     
