Bottom_Layer = -1
Top_Layer = 20

while True:

    target = input('input target layer: ')

    # 退出条件
    if target == 'exit':
        break
    # 校验
    if target.lstrip('-').isdigit():
        target_layer = int(target)
        if Bottom_Layer <= target_layer <= Top_Layer:
            # 输出实际楼层
            print(f"Actual Layer: {target}")
        else:
            # 错误提示
            print(f"target need between [{Bottom_Layer}, {Top_Layer}]")
    else:
        # 错误提示
        print("digit is need")

# 退出提示
print("shutdown")
