import sympy.logic
import re


def weight(st):
    weight = 0
    for s in st:
        if s == '1':
            weight += 1
    return weight


def kernelImpl(r_dnf, s):
    kernelImplic = set()
    l = list(s)
    i = 0
    while i < len(r_dnf):
        s = ''
        for j in range(len(l)):
            eq = True
            for k in range(len(l[j])):
                if l[j][k] != '~' and l[j][k] != r_dnf[i][k]:
                    eq = False
                    break
            if eq:
                s += str(j) + ','
        s = s[:-1]
        if ',' not in s:
            kernelImplic.add(l[int(s)])
            r_dnf.remove(r_dnf[i])
            i -= 1
            continue
        i += 1
    for el in kernelImplic:
        i = 0
        while i < len(r_dnf):
            eq = True
            for k in range(len(r_dnf[i])):
                if el[k] != '~' and r_dnf[i][k] != el[k]:
                    eq = False
                    break
            if eq:
                r_dnf.remove(r_dnf[i])
                i -= 1
                continue
            i += 1
    return kernelImplic, r_dnf


def petcrickMeth(r_dnf, s, kernelImp):
    l = list(s)
    for el in kernelImp:
        l.remove(el)
    knf = ''
    for i in range(len(r_dnf)):
        s = '('
        for j in range(len(l)):
            eq = True
            for k in range(len(l[j])):
                if l[j][k] != '~' and l[j][k] != r_dnf[i][k]:
                    eq = False
                    break
            if eq:
                s += 'A' + str(j) + ' | '
        s = s[:-3] + ')'
        if s != ')':
            knf += s + ' & '
    knf = knf[:-3]
    str_knf = str(sympy.to_dnf(sympy.simplify_logic(knf)))
    str_knf = re.sub(r"[()A]", "", str_knf)
    str_knf = str_knf[:str_knf.find('|')].split('&')
    for el in str_knf:
        kernelImp.add(l[int(el)])
    return kernelImp


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


def minim(n, d, dnf):
    r_dnf = ' '.join(dnf)
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
    kernelIpm, new_dnf = kernelImpl(dnf, s)
    ans = petcrickMeth(new_dnf, s, kernelIpm)
    r_dnf = r_dnf.split()
    print("\n \n Минимальное покрытие: \n" + str(ans)+ '\n\n')
    printf(r_dnf, ans)


d = dict()
dnf = list()
n = 6
filename = r'inp.txt'
var = open(filename)
for st in var:
    st = st.strip('\n')
    d.setdefault(weight(st), [])
    d.get(weight(st)).append([st, True])
    dnf.append(st)
minim(n, d, dnf)
