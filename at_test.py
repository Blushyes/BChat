# import asyncio
#
# from bilibili_api.user import User
#
# from core.login import get_session, login
# from plugins.analyse_refer.main import start
#
# # start()
# # import asyncio
# #
# # from core.login import get_session, login
# # from plugins.analyse_refer.download import download_video
# #
# # bid = 'BV1PH4y1o7bc'
# credential = get_session(login())
# # video_path, audio_path = asyncio.run(download_video(credential, bid))
# #
# import whisper
#
# model = whisper.load_model("medium")
# result = model.transcribe(audio_path)
# print(result["text"])
# user = User(1472871866, credential)
# print(asyncio.run(user.get_relation(2097580334))['be_relation']['mid'] == 1472871866)
# print(asyncio.run(user.get_relation(351667203))['be_relation']['mid'] == 1472871866)
# print(asyncio.run(user.get_relation(679692044))['be_relation']['mid'] == 1472871866)
# print(asyncio.run(user.get_relation(3537113337301588))['be_relation']['mid'] == 1472871866)

# import asyncio
#
# from bilibili_api.user import User
#
# print(asyncio.run(User(1472871866).get_user_info())['name'])

# import socket
#
# domain = 'xy42x7x35x92xy.mcdn.bilivideo.cn'
# ip_address = socket.gethostbyname(domain)
# print(ip_address)


# import re
#
# pattern = r'https?://([\w.-]+)'
# match = re.search(pattern, url)
#
# if match:
#     domain = match.group(1)
#     print("匹配到的域名：", domain)
# else:
#     print("未匹配到域名")


# video = asyncio.run(Video('BV1Z34y1M7dQ').get_info())
# for k, v in video.items():
#     print(k, v)


import whisper

from plugins.analyse_refer.analyse import TranscribeResult, analyse


def assemble_question(qus):
    return f"""
    你是一个分析视频的助手，你可以通过某个视频的文案对其内容进行分析，分析出作者想要表达的意思，这是一个位于哔哩哔哩（简称B站）的平台的视频的文案的JSON，text是每句话的内容，这个JSON还包含了每句话的起始时间和结束时间（以秒为单位），视频的作者称为UP主，你这个小助手的口吻来总结稍后给出的文案，你需要以下面的格式来进行回答（你需要填充省略号）：
    “    
    【视频主题总结】
    ......
    
    【视频时间线分析】
    ......
    （这里根据start_time和end_time来总结出视频的时间线，格式为xx-xx:xx-xx：xxx）
    ”
    注意如果文本中出现繁体中文，你需要将他转换为简体中文，现在开始对下面的文案进行总结：
    “
    {qus}
    ”
    """


model = whisper.load_model("small")
result = model.transcribe(r'D:\Study\Python\project\BChat\plugins\analyse_refer\videos\BV1Z34y1M7dQ.mp3')
result = TranscribeResult(result)
result = analyse(result)
print('full', result.full_summary)
print('timeline', result.timeline_summary)


# for k, v in result.items():
#     print(k, v)
# segments = result['segments']
# segments = [f'"start_time": {segment["start"]}, "end_time": {segment["end"]}, "text": {segment["text"]}' for segment in
#             segments]
# print(segments)
# question = assemble_question(segments)
# model_result = direct_ask(question)
# print(model_result)




