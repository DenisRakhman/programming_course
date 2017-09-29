
class WikiParser:

    def __init__(self):
        pass

    def normalize(self, text):
        import string
        import re
        text = string.lower(text)
        text = ' '.join(text.split())
        text = re.sub('[^\w ]', '', text)
        return text

    def get_articles(self, start):
        from pattern.web import Wikipedia, plaintext
        file = open(start+'.txt', 'w')
        file.write('')
        file.close()
        list_of_strings = []
        start_article  = Wikipedia().article(start)
        links = set(start_article.links)
        for link in start_article.links:
            cur_article = Wikipedia().article(link)
            if cur_article != None:
                newtext = plaintext(cur_article.source)
                newtext = self.normalize(newtext)
                list_of_strings.append(newtext)
                file = open(start+'.txt', 'a')
                file.write(newtext.encode('utf-8'))
                file.write('\n\n-----\n\n')
                file.close()
        return list_of_strings

class TextStatistics:

    def __init__(self, articles):
        self.articles = []
        import re
        for article in articles:
                self.articles.append(re.sub('[^\w ]|[1234567890]', '', article))
        pass

    def get_3grams(self):
        for article in self.articles:
            for s in range(0, len(article)-3):
                newgram = article[s:s+3]

    def get_top_3grams(self):
        import collections as cl
        grams_freq = {}
        for article in self.articles:
            words = article.split()
            for w in range(0, len(words)):
                if w >= 2:
                    cur_gram = words[w-2] + ' ' + words[w-1] + ' ' + words[w]
                    if cur_gram not in grams_freq:
                        grams_freq[cur_gram] = 1
                    else:
                        grams_freq[cur_gram] += 1
        grams_freq = cl.OrderedDict(sorted(grams_freq.items(), key=lambda t: t[1], reverse=1))
        list_of_3grams_in_descending_order_by_freq = [gram for gram in grams_freq]
        list_of_their_corresponding_freq = [grams_freq[gram] for gram in grams_freq]
        return (list_of_3grams_in_descending_order_by_freq, list_of_their_corresponding_freq)

    def get_top_words(self):
        import collections as cl
        words_freq = {}
        banlist = ['a', 'an', 'the', 'aboard', 'about', 'above', 'across', 'between', 'afore', 'after', 'against', 'along', 'amid', 'amidst', 'among', 'amongst', 'around', 'as', 'aside', 'aslant', 'astride', 'at', 'athwart', 'atop', 'before', 'behind', 'below', 'beneath', 'beside', 'besides', 'between', 'betwixt', 'beyond', 'by', 'circa', 'despite','down', 'except', 'for', 'from', 'in', 'inside', 'into', 'like', 'near', 'neath', 'next', 'of', 'off', 'on', 'opposite', 'out', 'outside', 'over', 'per', 'through', 'till'', toward', 'towards', 'under', 'underneath', 'unlike', 'until', 'up', 'with', 'without']
        for article in self.articles:
            for w in article.split():
                if w not in banlist:
                    if w not in words_freq:
                        words_freq[w] = 1
                    else:
                        words_freq[w] += 1
        words_freq = cl.OrderedDict(sorted(words_freq.items(), key=lambda t: t[1], reverse=1))
        list_of_words_in_descending_order_by_freq = [word for word in words_freq]
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
        self.words = self.stats.get_top_words()
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
        self.nlp_top_words = [' - '.join([self.nlp_stats.get_top_words()[0][i], str(self.nlp_stats.get_top_words()[1][i])]) for i in range(20)][:5]



    def show_results(self):
        out  = 'Experiment results: \n\n Most frequent 3-grams throughout the corpus:\n' + '\n'.join(self.top_grams_out) +'\n\nMost frequent words throughout the corpus\n' + '\n'.join(self.top_words_out)
        out += '\n\n Most frequent 3-grams throughout NLP article:\n' + '\n'.join(self.nlp_top_grams)+'\n\nMost frequent words throughout the NLP article\n' + '\n'.join(self.nlp_top_words)
        print (out)


#  Most frequent 3-grams throughout the corpus:
# natural language processing - 336
# from the original - 306
# archived from the - 296
# v t e - 277
# the use of - 238
# the original on - 238
# as well as - 224
# one of the - 205
# a b c - 186
# proceedings of the - 182
# the european union - 163
# cambridge university press - 158
# of the european - 155
# such as the - 153
# the number of - 143
# a number of - 141
# university press isbn - 140
# for example the - 136
# a set of - 131
# based on the - 130
#
# Most frequent words throughout the corpus
# and - 16876
# to - 11980
# is - 8688
# that - 4823
# are - 4302
# language - 4074
# or - 3847
# be - 3398
# it - 2735
# this - 2528
# which - 2205
# can - 1966
# not - 1954
# was - 1805
# english - 1801
# speech - 1739
# retrieved - 1722
# languages - 1715
# such - 1700
# words - 1668
#
#  Most frequent 3-grams throughout NLP article:
# natural language processing - 16
# a chunk of - 6
# chunk of text - 6
# of natural language - 5
# systems based on - 4
#
# Most frequent words throughout the NLP article
# and - 72
# language - 59
# to - 54
# is - 48
# natural - 39
