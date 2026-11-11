import csv
import os

# 定义文件夹路径
folder_path = "./data"
# 如果data文件夹不存在就自动创建
if not os.path.exists(folder_path):
    os.mkdir(folder_path)

# 拼接完整文件路径
file_path = os.path.join(folder_path, "stu.csv")

# 写入csv
with open(file_path, "w", encoding="utf-8", newline="") as f:  #newline=""， 防止出现多余空行
    writer = csv.writer(f) #创建一个专门用来写csv格式文本的工具（写入器），绑定到你打开的文件，专门用来一行一行写入csv表格数据，调用这个写入器，自动帮你处理英文逗号、引号、换行，生成标准csv
    # 表头
    writer.writerow(["name", "age", "gender"])
    # 数据行
    writer.writerow(["王梓涵", 25, "男"])
    writer.writerow(["刘若曦", 22, "女"])
    writer.writerow(["陈俊宇", 20, "男"])
    writer.writerow(["赵思瑶", 28, "女"])
    writer.writerow(["黄浩然", 15, "男"])
    writer.writerow(["林雨桐", 20, "女"])
    writer.writerow(["周博文", 20, "男"])
    writer.writerow(["吴诗琪", 24, "女"])
    writer.writerow(["马子轩", 22, "男"])
    writer.writerow(["孙悦然", 27, "女"])

print(f"stu.csv 已经成功生成，路径：{file_path}")
