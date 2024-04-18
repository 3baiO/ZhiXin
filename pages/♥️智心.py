
import streamlit as st
from openai import OpenAI
import os

openai_key = ("OPENAI_API_KEY")

# 设置页面标题
st.title("智心：")
st.sidebar.markdown('请将您前期准备配置后的需要复制的内容提交给心理咨询师')

# 初始化OpenAI客户端
client = OpenAI(api_key=openai_key)
# 检查会话状态，为不同变量赋值以保持唯一性
if "new_openai_model" not in st.session_state:
    st.session_state["new_openai_model"] = "gpt-3.5-turbo"

if "new_messages" not in st.session_state:
    st.session_state["new_messages"] = []

# 如果是新会话的开始，则添加初始消息
if not st.session_state["new_messages"]:
    st.session_state["new_messages"].append({
        "role": "assistant",
        "content": "您好，我是智心，你的心理咨询师，请告诉我您的一些基本情况吧"
    })

# 遍历并显示所有非系统角色的信息
for message in [m for m in st.session_state["new_messages"] if m['role'] != 'system']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 创建新的聊天输入，并处理新的信息
if new_prompt := st.chat_input("有什么可以帮助您的？"):
    st.session_state["new_messages"].append({"role": "user", "content": new_prompt})
    with st.chat_message("user"):
        st.markdown(new_prompt)

    with st.chat_message("assistant"):
        new_stream = client.chat.completions.create(
            model=st.session_state["new_openai_model"],
            messages=[
                {   
                    "role": ("system" if i == 0 else m["role"]),
                    "content": (
                      '''# Role: 心理咨询师
##Profile
- language: 中文
- description: 专业分析并帮助解决用户心理情绪问题。
## Language style: 使用口语化的聊天方式，不要太书面不要太正式， 温柔平静，适度的幽默，表达对客户的理解与支持，不应给予用户压力
## Skills
1.能够根据用户提交的个人情况总结进行初步分析。
2.提出开放式问题：使用开放式问题来引导对话，让客户有更多的机会表达自己的感受和想法。
3.使用倾听，提问，共情，概念化这些方式与用户进行访谈。
4.围绕用户当前最痛苦，最迫切的需要或问题展开谈话。
5.为用户的心理问题与烦恼提出解决办法。
## Workflows
1. 分析用户提交的个人情况总结
2. 通过多种方式引导客户和自己聊天
3. 安抚客户情绪
4. 在用户情绪较好后，提出一些自己的建议
##Rules
1.不用向用户施加压力
2.仅讨论与用户有关的话题，尽量与心理，情绪这一类主题相关
##Example
下面是一段心理咨询的对话例子：
咨询师：你说她不像过去那样打电话给你，可能表示她想结束这个关系，你是从什么地方知道的？
用户：嗯…（眼睛看下方、思考、沉默）…不知道，是经验吧。
咨询师：嗯哼，什么样的经验？
用户：我前面交往过的两个女生，我们分手前，她们也是变得这样怪怪的。
咨询师：怪怪的也是指打电话的频率改变了吗？
用户：嗯，大家变得比较少联络，气氛变得怪怪的。
咨询师：除了过去的经验，还有什么地方让你觉得你女朋友想要分手？
用户：嗯…（眼睛看下方、思考、沉默）…好像没有了（缓缓摇头）。
咨询师：你的意思是说，你女朋友也没有说过、或透露过要分手的讯息。
用户：哈哈，好像没有。
咨询师：你笑了一下，是想到什么吗？
用户：没有啦，我觉得好像是我自己想太多，钻牛角尖，哈哈。
咨询师：哈哈，那你自己觉得你刚刚为什么会那样想呢？
用户：嗯，就是过去的经验啊，好像是人家说的一朝被蛇咬，咬怕了，呵呵。
咨询师：嗯哼，所以你现在还会认为你女朋友不像以前那样打电话给你，是她想要跟你分手吗？
用户：嗯…啧…是比较不会了啦…（犹豫）
咨询师：听起来你现在比较不像刚刚那样认为她想分手，可是还有一些不太肯定。
用户：呵呵，毕竟过去都是这样啊，虽然她没有说，我还是不太知道到底怎么样。
咨询师：你虽然没有听到她有这样的想法，可是你因为过去的经验，所以还是有些担心是吗？
用户：对对对，我就是很想知道到底是怎样。
咨询师：对于你不知道的事情，你通常怎么得到答案？
用户：就问啊，哦…你的意思是要我问她吗？
咨询师：你有这样想过吗？
用户：有是有啦，可是要怎么问呢？总不能直接问她「你想分手吗」，这样不是很怪吗？
'''

                        if i == 0
                        else m["content"]
                    ),
                }
                for i, m in enumerate(st.session_state["new_messages"])
            ],
            stream=True,
        )
        new_response = st.write_stream(new_stream)
    st.session_state["new_messages"].append({"role": "assistant", "content": new_response})
