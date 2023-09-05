count = 0
m = -20001
f = open('abc')
l = [int(i) for i in f]
for i in range(len(l) - 1):
    if (l[i] +l[i + 1] % 6 != 0) and (l[i] +l[i + 1] % 6 <= abs(10000)):
        count += 1
        m = max(m, l[i]+ l[i + 1])
print(count, m)