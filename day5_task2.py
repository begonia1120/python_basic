l1 = [100, 1000, 10, 400, 25, 40, 0]
l2 = l1.copy()
l2.sort()

fmt = "{:<8}{}"
print(fmt.format("l1", "l2"))

for i in range(len(l1)):
    print(fmt.format(str(l1[i]), str(l2[i])))