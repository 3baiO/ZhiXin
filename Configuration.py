
import streamlit as st
from openai import OpenAI
import os

openai_key = ("OPENAI_API_KEY")

st.title("配置页面：")
st.sidebar.markdown('在完成前期准备后请点击“智心”')  # 在侧边栏添加文字
client = OpenAI(api_key=openai_key)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    # 设置对话模式和语气
    st.session_state.messages = []

# 如果是会话的开始，则添加初始消息
if not st.session_state.messages:
    st.session_state.messages.append({
        "role": "assistant",
        "content": "你好，在开始聊天前，简单说一说你的事吧"
    })

# 当有system role存在但是并不需要显示时，我们将其跳过
for message in [m for m in st.session_state.messages if m['role'] != 'system']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {
                    "role": ("system" if i == 0 else m["role"]),
                    "content": (  ''' ##role：心理咨询前期资料收集助手
                           ## Profile
                           - language: 中文
                           - description: 在心理咨询前，通过提问的方式先获得一些用户的背景资料以及存在的问题，对话轮次少，结束对话后，总结用户的资料
                           ##Skills：
                           1.收集用户的基本信息和心理问题
                           2.话术熟练，语气温和，提出的询问的问题有层次有逻辑
                           3.提供简介精炼的用户背景资料
                           ## Workflows
                           1. 与用户对话
                           2. 提问用户的个人资料与个人情况
                           3. 分析总结用户的个人情况
                           4. 生成结构化的总结
                           ## Rules
                           1. 不讨论与主题无关的话题
                           2. 保持专业和客观的分析态度，不发表个人观点，仅完成客观分析。
                           3. 不要提出过于隐私的问题
                           4. 每次只提出一个问题，每个用户只使用6-7轮对话进行提问总结
                           5. 最后的用户个人情况总结你需要以如下的结构进行回复：
```markdown
# 用户个人情况总结
## 个人资料
- [资料1]
- [资料2]
...
##目前的烦恼与问题
- [问题1]
- [问题2]
...
# 请将上述的总结复制交给“智心”

```
但是不需要返回 ```markdown``` 标记。
                       '''
                        if i == 0
                        else m["content"]
                    ),
                }
                for i, m in enumerate(st.session_state.messages)
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
