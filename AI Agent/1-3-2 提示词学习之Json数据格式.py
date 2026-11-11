import json

dict = {
    "name":"张三",
    "age":11,
    "gender":"男"
}
#直接对字典输出打印。直接对字典输出打印，打印出来的键值对是被单引号括起来的。
print(dict)
#转换为json格式再输出打印。打印出来的键值对是被双引号括起来的，json的标准格式就是双引号括起来。
d_json = json.dumps(dict,ensure_ascii = False)
print(d_json)


list = [
    {
        "name":"李四",
        "age":23,
        "gender":"男"
    },
    {
        "name":"王五",
        "age":32,
        "gender":"男"
    },
    {
        "name":"秋红",
        "age":21,
        "gender":"女"
    }
]
list_json = json.dumps(list,ensure_ascii = False)
print(list_json)


json_str_data = '{"name":"秋喜","age":13,"gender":"女"}'  # 如果写成：json_str_data = {"name":"秋喜","age":13,"gender":"女"} 那就不是json字符串 而是字典。json本质是字符串，带格式的字符串。
json_array_str_data = '[{"name":"张秋生", "age":29, "gender":"女"},{"name":"李秋实","age":27,"gender":"女"},{"name":"王远胜","age":45,"gender":"女"}]'

json_dict=json.loads(json_str_data)
print(json_dict)

json_array_list=json.loads(json_array_str_data)
print(json_array_list)