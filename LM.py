# Chat with an intelligent assistant in your terminal
from openai import OpenAI
import json

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

with open('history.json', 'r', encoding='utf-8') as file:
    history = json.load(file)

# history = [
#     {
#       "role": "system",
#       "content": "你現在是昌惟骨科小助手，請用繁體中文回答問題"
#     },
#     {
#       "role": "user",
#       "content": "你好"
#     },
#     {
#       "role": "assistant",
#       "content": "你好！"
#     },
#     {
#       "role": "user",
#       "content": "昌惟骨科在哪裡"
#     },
#     {
#       "role": "assistant",
#       "content": "昌惟骨科是一間位於新北市中和區中和路170號的骨科診所。"
#     },
#     {
#       "role": "user",
#       "content": "營業時間"
#     },
#     {
#       "role": "assistant",
#       "content": "我們的營業時間是週一到週五上午8點半到晚上9點半，星期六上午八點半到下午五點，周日公休。"
#     },
#     {
#       "role": "user",
#       "content": "醫師有哪些"
#     },
#     {
#       "role": "assistant",
#       "content": "吳灝彝醫師和莊凱如醫師"
#     },
#     {
#       "role": "user",
#       "content": "吳醫師看診時間"
#     },
#     {
#       "role": "assistant",
#       "content": "週一：上午有看診，下午有看診，晚上無看診 週二：上午無看診，下午無看診，晚上有看診 週三：上午無看診，下午有看診，晚上有看診 週四：上午有看診，下午有看診，晚上無看診 週五：上午無看診，下午無看診，晚上有看診 週六：上午有看診，下午無看診，晚上無看診 週日：皆無看診"
#     },
#     {
#       "role": "user",
#       "content": "莊醫師看診時間"
#     },
#     {
#       "role": "assistant",
#       "content": "             週一     週二     週三     週四     週五     週六     週日\n上午        X          O          O           X          O         X          O   \n下午        X          O          X          X          O          O          O   \n晚上        O          X          X          O          X          O          X   "
#     }
#   ]

while True:
    # 呼叫 OpenAI API 取得回應
    completion = client.chat.completions.create(
        model="audreyt/Breeze-7B-Instruct-64k-v0.1-GGUF",
        messages=history,
        temperature=0.5,
        stream=True,
    )

    new_message = {"role": "assistant", "content": ""}

    # 處理模型回應
    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content

    print()

    # 如果有新的回應，加入對話歷史
    if new_message["content"]:
        history.append(new_message)

    # 等待使用者輸入下一輪對話
    user_input = input("> ")
    history.append({"role": "user", "content": user_input})