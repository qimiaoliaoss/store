def lowertoupper(number, recursive_depth=0):
    str_number = str(number)
    if len(str_number) > 4:
        str_number = str_number[-4:]
    bits = "零 一 二 三 四 五 六 七 八 九".split(" ")

    units = " 十 百 千".split(" ")
    large_unit = ' 万 亿 万'.split(" ")  # 可扩展,以万为单位
    number_len = len(str_number)
    result = ""

    for i in range(number_len):
        result += bits[int(str_number[i])]
        if str_number[i] != "0":
            result += units[number_len - i - 1]

    # 去除连续的零
    while "零零" in result:
        result = result.replace("零零", "零")
    # 去除尾部的零
    if result[-1] == "零":
        result = result[:-1]
    # 调整10~20之间的数
    if result[:2] == "一十":
        result = result[1:]
    # 字符串连接上大单位
    result += large_unit[recursive_depth]

    # 判断是否递归
    if len(str(number)) > 4:
        recursive_depth += 1
        return lowertoupper(str(number)[:-4], recursive_depth) + result
    else:
        return result

num = input()
print(lowertoupper(num))