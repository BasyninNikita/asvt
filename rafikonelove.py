import sys


def weight(str):
    weight = 0
    for s in str:
        if s == '1':
            weight += 1
    return weight


def equal(miniterm, dnf):
    symb = '*'
    for i in range(len(miniterm)):
        if miniterm[i] != '~' and miniterm[i] != dnf[i]:
            symb = ' '
            break
    return symb


def printf(dnf, s):
    # std::cout << std::endl << std::setw((n + 1) * (dnf.size() + 1)) << std::setfill('-') << ' ' << std::endl << std::setfill(' ');

    for i in range(len(dnf) + 1):
        if i == 0:
            print('  |', end='')
        else:
            print(dnf[i - 1], end= '')
            print('|', end='')
    print('\n', end='')
    for el in s:
        print(el + '|', end='')
        for j in range(len(dnf)):
            print(equal(el, dnf[j]) + ' |', end='')
        print('\n', end= '')


def minim(n, d, dnf):
    rep = False
    s = set()
    while True:
        rep = False
        new_dict = dict()
        for i in range(n):
            if d.get(i) is None:
                continue
            for el in d.get(i):
                if d.get(i + 1) is not None:
                    for j in range(len(d.get(i + 1))):
                        str1 = d.get(i + 1)[j][0]
                        str2 = el[0]
                        diff = pos = 0
                        for k in range(n):
                            if str1[k] == str2[k] or (k == n - 1 and diff == 0):
                                if k == n - 1:
                                    if diff == 1:
                                        str2 = str2[:pos] + '~' + str2[pos + 1:]
                                    else:
                                        str2 = str2[:n - 1] + '~'
                                    new_dict.setdefault(weight(str2), [])
                                    new_dict.get(weight(str2)).append([str2, True])
                                    el[1] = False
                                    d.get(i + 1)[j][1] = False
                                    rep = True
                            elif diff == 0:
                                pos = k
                                diff += 1
                            else:
                                break
                if el[1] is True:
                    s.add(el[0])
        d = new_dict
        if rep is False:
            break
    printf(dnf, s)



d = dict()
dnf = list()
n = 3
for str in sys.stdin:
    str = str.strip('\n')
    d.setdefault(weight(str), [])
    d.get(weight(str)).append([str, True])
    dnf.append(str)
minim(n, d, dnf)
