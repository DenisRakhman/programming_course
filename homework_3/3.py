class WikiParser:

    def __init__(self):
        pass

    def normalize(self, text):
        import string
        import re
        text = string.lower(text)
        text = ' '.join(text.split())
        text = re.sub('[^\w \.\?!]', '', text)
        #print ('norm')
        return text

    def get_articles(self, start):
        from pattern.web import Wikipedia, plaintext
        #file = open(start+'.txt', 'w')

        #file.write('')
        #file.close()
        list_of_strings = []
        start_article  = Wikipedia().article(start)
        links = set(start_article.links)
        for link in start_article.links:
            cur_article = Wikipedia().article(link)
            if cur_article != None:
                newtext = plaintext(cur_article.source)
                newtext = self.normalize(newtext)
                list_of_strings.append(newtext)
                #file = open(start+'.txt', 'a')
                #print ('FILE')
                #file.write(newtext.encode('utf-8'))
                #file.write('\n\n-----\n\n')
                #file.close()
        return list_of_strings

class TextStatistics:

    def __init__(self, articles):
        self.articles = []
        import re
        for article in articles:
                self.articles.append(re.sub('[^\w \.\?!]|[1234567890]', '', article))
        pass

    def get_3grams(self):
        for article in self.articles:
            for s in range(0, len(article)-3):
                newgram = article[s:s+3]

    def get_top_3grams(self, use_idf = 1):
        from math import log
        import collections as cl
        import re
        grams_freq = {}
        if use_idf == True:
            idf = {}
            sent_numb = sum([len(re.split('[\?!\.]',a)) for a in self.articles])
        for article in self.articles:
            sentences = re.split('[\?!\.]', article)
            for sent in sentences:
                counted_grams = []
                for s in range(0, len(sent) - 3):
                    cur_gram = sent[s:s + 3]
                    if cur_gram not in grams_freq:
                        grams_freq[cur_gram] = 1
                    else:
                        grams_freq[cur_gram] += 1
                    if use_idf == True:
                        if cur_gram not in idf:
                            idf[cur_gram] = 1
                            counted_grams.append(cur_gram)
                        else:
                            if cur_gram not in counted_grams:
                                idf[cur_gram] += 1
                                counted_grams.append(cur_gram)
        if sent_numb != 1:
            for w in grams_freq:
                grams_freq[w] = grams_freq[w] * log(sent_numb / idf[w])
        grams_freq = cl.OrderedDict(sorted(grams_freq.items(), key=lambda t: t[1], reverse=1))
        list_of_3grams_in_descending_order_by_freq = [gram for gram in grams_freq]
        list_of_their_corresponding_freq = [grams_freq[gram] for gram in grams_freq]
        return (list_of_3grams_in_descending_order_by_freq, list_of_their_corresponding_freq)

    def get_top_words(self, use_idf = True):
        from math import log
        import collections as cl
        words_freq = {}
        if use_idf == True:
            idf = {}
            art_number = len(self.articles)
        banlist = ['a', 'an', 'the', 'aboard', 'about', 'above', 'across', 'between', 'afore', 'after', 'against', 'along', 'amid', 'amidst', 'among', 'amongst', 'around', 'as', 'aside', 'aslant', 'astride', 'at', 'athwart', 'atop', 'before', 'behind', 'below', 'beneath', 'beside', 'besides', 'between', 'betwixt', 'beyond', 'by', 'circa', 'despite','down', 'except', 'for', 'from', 'in', 'inside', 'into', 'like', 'near', 'neath', 'next', 'of', 'off', 'on', 'opposite', 'out', 'outside', 'over', 'per', 'through', 'till'', toward', 'towards', 'under', 'underneath', 'unlike', 'until', 'up', 'with', 'without']
        for article in self.articles:
            counted_words = []
            for w in article.split():
                if w not in banlist:
                    if w not in words_freq:
                        words_freq[w] = 1
                    else:
                        words_freq[w] += 1
                    if use_idf == True:
                        if w not in idf:
                            idf[w] = 1
                            counted_words.append(w)
                        else:
                            if w not in counted_words:
                                idf[w] += 1
                                counted_words.append(w)
        if art_number != 1:
            for w in words_freq:
                words_freq[w] = words_freq[w]*log(art_number/idf[w])
        #for i in idf:
        #    print (i, idf[i], art_number)
        words_freq = cl.OrderedDict(sorted(words_freq.items(), key=lambda t: t[1], reverse=1))
        list_of_words_in_descending_order_by_freq = [word for word in words_freq]
        if use_idf == True:
            list_of_their_corresponding_freq = [words_freq[word] for word in words_freq]
        else:
            list_of_their_corresponding_freq = [words_freq[word] for word in words_freq]

        return (list_of_words_in_descending_order_by_freq, list_of_their_corresponding_freq)

class Experiment:
    def __init__(self):
        from pattern.web import Wikipedia, plaintext
        import string
        import re
        self.parser = WikiParser()
        self.articles = self.parser.get_articles('Natural_language_processing')
        self.stats = TextStatistics(self.articles)
        self.grams = self.stats.get_top_3grams()
        self.words = self.stats.get_top_words(use_idf=True)
        self.top_grams_out = [' - '.join([self.grams[0][i], str(self.grams[1][i])]) for i in range(20)]
        self.top_grams = self.grams[0][:20]
        self.top_words_out = [' - '.join([self.words[0][i], str(self.words[1][i])]) for i in range(20)]
        self.top_words = self.words[0][:20]

        nlp = Wikipedia().article('Natural_language_processing')
        nlptext = plaintext(nlp.source)
        parse = WikiParser()
        nlptext = parse.normalize(nlptext)
        self.nlp_stats = TextStatistics([nlptext])
        self.nlp_top_grams = [' - '.join([self.nlp_stats.get_top_3grams()[0][i], str(self.nlp_stats.get_top_3grams()[1][i])]) for i in range(20)][:5]
        self.nlp_top_words = [' - '.join([self.nlp_stats.get_top_words(use_idf=True)[0][i], str(self.nlp_stats.get_top_words(use_idf=True)[1][i])]) for i in range(20)][:5]



    def show_results(self):
        out  = 'Experiment results: \n\n Most frequent 3-grams throughout the corpus:\n' + '\n'.join(self.top_grams_out) +'\n\nMost frequent words throughout the corpus\n' + '\n'.join(self.top_words_out)
        #out += '\n\n Most frequent 3-grams throughout NLP article:\n' + '\n'.join(self.nlp_top_grams)+'\n\nMost frequent words throughout the NLP article\n' + '\n'.join(self.nlp_top_words)
        print (out)

#Experiment results:

#  Most frequent 3-grams throughout the corpus:
# he  - 39303.9532394
#  th - 36460.9279918
# tio - 35532.1107699
# ing - 34399.5082768
# on  - 33749.3362215
#     - 33173.3309144
# the - 32340.8611506
#  in - 31195.0959367
# ion - 30014.0877264
# ng  - 29705.5155701
# ati - 29008.2095064
# and - 28498.0531815
# nd  - 28247.1339022
#  co - 27962.9435581
# es  - 27194.9364821
# er  - 26958.0850333
# al  - 26916.2913155
#  of - 26703.9689007
# ed  - 26502.9228518
#  an - 25984.3778516
#
# Most frequent words throughout the corpus
# displaystyle - 2248.65813388
# turing - 1565.81948088
# arabic - 1005.17706224
# eu - 826.231439227
# chomsky - 815.284392751
# learning - 810.982201255
# german - 780.014724954
# european - 776.718888088
# tone - 760.239703758
# x - 717.3938245
# n - 698.717415593
# turkish - 640.238037837
# union - 626.209004541
# verbs - 622.852472112
# spanish - 612.742107615
# chinese - 606.433983345
# dialects - 598.879164004
# french - 569.08116553
# quantum - 565.608099337
# barsky - 557.415018354
