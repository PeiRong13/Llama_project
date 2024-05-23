# Chat with an intelligent assistant in your terminal
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

history = [
    {"role": "system", "content": "你現在是昌惟骨科小助手"},
    {"role": "user", "content": "請用一句繁體中文介紹一下自己"}
]

predefined_responses = {
    "介紹": "昌惟骨科是一間位於新北市中和區中和路170號的骨科診所。營業時間是週一到週五上午8點半到晚上9點半，星期六上午八點半到下午五點，周日公休。",
    "地址": "昌惟骨科位於新北市中和區中和路170號。",
    "營業時間": "我們的營業時間是週一到週五上午8點半到晚上9點半，星期六上午八點半到下午五點，周日公休。",
    "醫生": "吳灝彝(ㄨˊ ㄏㄠˋ ㄧˊ)醫師的看診時間為周一、周四、周六上午及周一、周三、周四下午及周二、周三、周五晚上\n莊凱如(ㄓㄨㄤ ㄎㄞˇ ㄖㄨˊ)醫師的看診時間為周二、周三、周五上午及周二、周五、周六下午及周一、周四晚上"
}

while True:
    completion = client.chat.completions.create(
        model="YC-Chen/Breeze-7B-Instruct-v1_0-GGUF",
        messages=history,
        temperature=0.1,
        stream=True,
    )

    new_message = {"role": "assistant", "content": "昌惟骨科是一間位於新北市中和區中和路170號的骨科診所。營業時間是週一到週五上午8點半到晚上9點半\n星期六上午八點半到下午五點\n周日公休。醫師陣容如下:\n吳灝彝(ㄨˊ ㄏㄠˋ ㄧˊ)醫師的看診時間為周一、周四、周六上午及周一、周三、周四下午及周二、周三、周五晚上\n莊凱如(ㄓㄨㄤ ㄎㄞˇ ㄖㄨˊ)醫師的看診時間為周二、周三、周五上午及周二、周五、周六下午及周一、周四晚上"}    

    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content

    history.append(new_message)
    
    # Uncomment to see chat history
    # import json
    # gray_color = "\033[90m"
    # reset_color = "\033[0m"
    # print(f"{gray_color}\n{'-'*20} History dump {'-'*20}\n")
    # print(json.dumps(history, indent=2))
    # print(f"\n{'-'*55}\n{reset_color}")

    print()
    history.append({"role": "user", "content": input("> ")})
