def s(n):
    summa_ch = 0
    for i in str(n):
        summa_ch += int(i)
    return summa_ch

def  m(n):
    min_ss = min(str(n))
    max_ss = max(str(n))
    M = int(min_ss) + int(max_ss)
    return M

def l(n):
    l = int(str(n)[0])
    return l


def r(n):
    r = int(str(n)[4])
    return r

max_n = []
for n in range(10000,100000): 
    z = 0
    p1 = s(n) - l(n)
    p2 = int(m(n)) - r(n)

    if p1<p2:
        z = int(str(p1) + str(p2))
    else:
        z = int(str(p2) + str(p1))
    if z == 222:
        max_n.append(n)

print(max(max_n))