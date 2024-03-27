# import re
#
# import pymysql
#
# from software.models import SoftWare
#
#
# # Create your tests here.
# # os.chdir("C:/Users/VincentAdamNemessis/Downloads/Documents/test")
# # files = os.listdir()
# # for file in files:
# #     os.rename(file, file.replace(".download", ""))
# # print(os.listdir())
#
# # def test():
# #     from django.contrib.auth.models import User
# #     x = User.objects.get().date_joined
#
# def extract_software_info(title, text):
#     # 使用正则表达式匹配和提取信息
#     name_match = title
#     version_match = re.search(r'\*\*本站版本：\*\*(\d+\.\d+\.\d+)', text)
#     language_match = re.search(r'\*\*语言：\*\*(\w+)', text)
#     run_os_version_match = re.search(r'\*\*\[x-span class="text-success"\](.*?)\[/x-span\]\*\*', text)
#     file_size_match = re.search(r'\*\*安装包大小：\*\*(.*?)\n', text)
#     description_match = re.search(r'</div>(.*?)----------', text, re.DOTALL)
#     official_link_match = re.search(r'x-btn type="secondary".*?href="(.*?)".*?content="软件官网"', text)
#     link_123_match = re.search(r'href="(https://www.123pan.com/s/.*?)"', text)
#     aliyun_drive_link_match = re.search(r'href="(https://www.aliyundrive.com/s/[^"]+)"', text)
#     icon_match = re.search(r'<img height=50px src="(.*?)"', text)
#
#     # 创建一个字典来存储提取的信息
#     software_info = {
#         'name': name_match if name_match else '',
#         'version': version_match.group(1) if version_match else '',
#         'language': language_match.group(1) if language_match else '',
#         'platform': 'Mac',
#         'run_os_version': run_os_version_match.group(1).replace(' &nbsp;&nbsp;&nbsp;', ';')
#         .replace('[/x-span] [x-span class="text-warning"]', '') if run_os_version_match else '',
#         'description': description_match.group(1).strip().replace('\r\n\r\n<!--more-->',
#                                                                   '') if description_match else '',
#         'official_link': official_link_match.group(1) if official_link_match else '',
#         'link_adrive': aliyun_drive_link_match.group(1) if aliyun_drive_link_match else '',
#         'link_123': link_123_match.group(1) if link_123_match else '',
#         'icon': icon_match.group(1)[:100] if icon_match else '',
#         'state': 2,
#         'category_id': 1,
#         'user_id': 1,
#         'tags': '',
#         'file_size': file_size_match.group(1).replace('\r', '') if file_size_match else None,
#         # 其他字段可以根据需要添加
#     }
#
#     return software_info
#
#
# def write_something():
#     # 连接到数据库
#     connection = pymysql.connect(host='localhost',
#                                  user='root',
#                                  password='ic3344',
#                                  database='synthesisyouwantmacapplicationdistributioncenter')
#
#     try:
#         with connection.cursor() as cursor:
#             # SQL 查询语句
#             sql = "SELECT * FROM apps"
#             cursor.execute(sql)
#
#             # 获取所有记录列表
#             results = cursor.fetchall()
#             software_list = []
#             for row in results:
#                 # 这里的column1, column2是表的字段名
#                 column1 = row[3].decode('utf-8')
#                 column2 = row[6].decode('utf-8')
#                 software_info = extract_software_info(column1, column2)
#                 software_list.append(software_info)
#                 # print(column2)
#             # 处理结果，写入数据库
#             for software in software_list:
#                 # SQL 插入语句
#                 SoftWare.objects.create(**software)
#     finally:
#         # 关闭数据库连接
#         connection.close()
