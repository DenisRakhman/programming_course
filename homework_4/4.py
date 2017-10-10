

def poly_hash(s, x=31, p=997):
    h = 0
    for j in range(len(s)-1, -1, -1):
        h = (h * x + ord(s[j]) + p) % p
    return h

def search_rabin_multi(text, patterns):
    patterns = [p for p in patterns if p != '']
    indices = [[] for p in range (len (patterns))]
    #print (indices)
    patterns_hash = [poly_hash(pattern) for pattern in patterns]
    for i in range(len(text) - min([len(pattern) for pattern in patterns]) + 1):
        for p in range (len(patterns)):
            substr_hash = poly_hash(text[i: i + len(patterns[p])])
            if substr_hash == patterns_hash[p]:
                if text[i: i + len(patterns[p])] == patterns[p]:
                    indices[p].append(i)
    return indices

from unittest import *

class SearchRabinMultiTest(TestCase):
    def setUp(self):
        self.search = search_rabin_multi

    def test_empty(self):
        text = ''
        pattern = ['smth', 'smth2']
        self.assertEqual(self.search(text, pattern), [[], []])

    def test_big_pattern(self):
        text = 'blabla'
        pattern = ['blablabla', 'blab']
        self.assertEqual(self.search(text, pattern), [[], [0]])

    def test_count(self):
        text = 'Betty Botter bought some butter'
        pattern = ['tt', 'er']
        indices = [[2, 8, 27], [10, 29]]
        self.assertListEqual(self.search(text, pattern), indices)

case = SearchRabinMultiTest()
suite = TestLoader().loadTestsFromModule(case)
TextTestRunner().run(suite)

#Сложность алгоритма в худшем случае равна O(T + n_1P_1 + n_2P_2 + .. +n_kP_k), где T - длина исходной строки,
#k - количество паттернов, P_i - длина i-того паттерна, n_i - количесвто вхождений i-того паттерна.
#Алгоритм проходит по всей строке один раз (отсюда слагаемое T), плюс для каждого встреченного паттерна алгоритм проходит по паттерну,
#что дает слагаемые n_iP_i
