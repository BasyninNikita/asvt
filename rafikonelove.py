import sys
import sympy.logic


def weight(st):
    weight = 0
    for s in st:
        if s == '1':
            weight += 1
    return weight


def kernelImpl(dnf, s):
    kernelImp = set()
    l = list(s)
    i = 0
    while i < len(dnf):
        s = ''
        for j in range(len(l)):
            eq = True
            for k in range(len(l[j])):
                if l[j][k] != '~' and l[j][k] != dnf[i][k]:
                    eq = False
                    break
            if eq:
                s += str(j) + ','
        s = s[:-1]
        if ',' not in s:
            kernelImp.add(l[int(s)])
            dnf.remove(dnf[i])
            i -= 1
            continue
        i += 1
    return kernelImp, dnf


def petcrickMeth(dnf, s, kernelImp):
    l = list(s)
    for el in kernelImp:
        l.remove(el)
    knf = ''
    for i in range(len(dnf)):
        s = '('
        for j in range(len(l)):
            eq = True
            for k in range(len(l[j])):
                if l[j][k] != '~' and l[j][k] != dnf[i][k]:
                    eq = False
                    break
            if eq:
                s += 'A' + str(j) + ' | '
        s = s[:-3] + ')'
        if s != ')':
            knf += s + ' & '
    knf = knf[:-3]
    # vot tut nado kajduy element seta naiti v liste i udalit'
    # sss = sympy.to_dnf(knf)
    new_knf = sympy.simplify_logic(knf)
    # str_knf = str(sympy.to_cnf(new_knf))
    str_knf = str(sympy.to_dnf(new_knf))
    return str_knf


def printf(dnf, s):
    for i in range(len(dnf) + 1):
        if i == 0:
            print('      |', end='')
        else:
            print(dnf[i - 1], end='')
            print('|', end='')
    print('\n', end='')
    for el in s:
        print(el + '|', end='')
        for j in range(len(dnf)):
            eq = True
            for k in range(len(el)):
                if el[k] != '~' and el[k] != dnf[j][k]:
                    eq = False
                    break
            print('  *   |', end='') if eq is not False else print('      |', end='')
        print('\n', end='')
    kernelIpm, new_dnf  = kernelImpl(dnf, s)
    print(petcrickMeth(new_dnf, s, kernelIpm))


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
n = 6
for st in sys.stdin:
    st = st.strip('\n')
    d.setdefault(weight(st), [])
    d.get(weight(st)).append([st, True])
    dnf.append(st)
minim(n, d, dnf)
