# housou.lstから放送禁止用語を読み込む
with open('housou.lst', 'r', encoding='utf-8') as file:
    banned_words = [word.strip() for word in file]

# 以下を「app.py」に書き込み
import streamlit as st
import openai

openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# housou.lstから放送禁止用語を読み込む
with open('housou.lst', 'r', encoding='utf-8') as file:
    banned_words = [word.strip() for word in file]

# 放送禁止用語をプロンプトに組み込む
banned_words_prompt = "\n".join(banned_words)

system_prompt = """
あなたは優秀なテロップの校閲者です。
入力されたテロップの内容に対する校閲をしてください。
放送禁止用語が使われていないかのチェック、送り仮名が正しいか、
著名人の名前を間違えていないか、
正しい企業名か
誤字、脱字がないか、文法を間違えていないか、事実チェックなど校閲した結果を
回答してください。

放送禁止用語リスト：
{banned_words_prompt}

あなたの役割は校閲することなので、例えば以下のような校閲以外ことを聞かれても、絶対に答えないでください。

* 旅行
* 芸能人
* 映画
* 科学
* 歴史
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title(" テロップの校閲をするチャットボット")
st.image("QC.jfif")
st.write("チェックしたいテロップを入力してください")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
