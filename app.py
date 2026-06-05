import streamlit as st
import os
from openai import OpenAI

st.set_page_config(page_title="裁员生存助手 AI版", page_icon="🧠")

st.title("🧠 裁员生存助手（OpenRouter AI版）")

# -----------------------
# API KEY
# -----------------------
api_key = os.getenv("OPENROUTER_API_KEY")

client = None

if api_key:
    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )

# -----------------------
# 输入
# -----------------------
industry = st.text_input("原行业（如 IT / HR / 外贸）")
age = st.number_input("年龄", 18, 70, 35)
skills = st.text_area("核心技能")

# -----------------------
# AI生成
# -----------------------
if st.button("生成AI生存方案"):

    if not api_key:
        st.error("请先配置 OPENROUTER_API_KEY")
        st.stop()

    if not industry or not skills:
        st.error("请填写完整信息")
        st.stop()

    prompt = f"""
你是一个现实主义职业规划顾问。

用户信息：
- 行业：{industry}
- 年龄：{age}
- 技能：{skills}

请输出：
1. 3条再就业路线
2. 每条路线难度（低/中/高）
3. 3个月行动计划
4. 现实风险提醒（不要鸡汤，要真实）
"""

    with st.spinner("AI生成中..."):

        try:
            response = client.chat.completions.create(
                model="openrouter/free",
                messages=[
                    {"role": "system", "content": "你是一个务实的职业规划顾问"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            result = response.choices[0].message.content

            st.subheader("📊 AI生存方案")
            st.write(result)

        except Exception as e:
            st.error(f"AI调用失败: {str(e)}")
