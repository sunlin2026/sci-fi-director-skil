import streamlit as st

st.set_page_config(page_title="科幻导演技能 AI", layout="wide")
st.title("🚀 科幻导演 AI 助理")
st.markdown("请输入您的科幻故事，AI会自动分析锚点并生成镜头提示词。")

user_script = st.text_area("📝 请输入剧本或故事梗概：", height=200, placeholder="例如：一个宇航员登陆未知星球，发现了一个巨大的蓝色发光遗迹...")

if st.button("🎬 生成分析报告"):
    if user_script.strip():
        with st.spinner("AI 正在思考中，请稍候..."):
            # --- 注意：这里因为没有真正的 API Key，我做了个假演示逻辑 ---
            # 如果您后续接入了真正的 API，把上面的 analyze_script 代码放这里
            result_text = f"""
**测试输出（因为您还没配置 API Key，这里显示的是模拟结果）：**

**输入剧本：** {user_script}

**分析结果：**
- **世界锚点**：未知外星文明
- **视觉核心**：巨大遗迹，蓝色能量核心
- **推荐镜头**：广角镜头，缓慢推入，IMAX电影风格
            
*（真实使用时，上面这段话会变成AI真实生成的提示词和分镜列表）*
            """
            st.success("分析完成！")
            st.markdown(result_text)
    else:
        st.warning("⚠️ 请先写点剧情再点击生成！")
