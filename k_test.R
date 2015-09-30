setwd("C:/Analytics Side Projects/1. Kate Project/Python")

## Libraries
library(XML); library(stringr); library(tm); library(RColorBrewer);
library(car); library(rvest);  library(NLP); library(wordcloud); library(SnowballC);
library(openNLP)

html_junk <- c("c\\(" = " ",
               "#34" = " ", 
               "<.*?>" = " ", 
               "\\\"" = " ")

k.txt = read.delim("k_reviews.txt", header = F, as.is=T) %>%
        tolower() %>%
        str_replace_all(html_junk) %>%
        removeWords(stopwords("english")) %>%
        removePunctuation() %>%
        stripWhitespace() 

## Prepare corpus
txt.corpus = Corpus(VectorSource(k.txt))
txt.tdm = TermDocumentMatrix(txt.corpus)

txt.m = as.matrix(txt.tdm)
txt.v = sort(rowSums(txt.m),decreasing=TRUE)
txt.d = data.frame(word=names(txt.v), freq=txt.v)

## Load sentiment dictionaries
snt.pos = scan('opinion-lexicon-English/positive-words.txt', what='character', comment.char=';')
snt.neg = scan('opinion-lexicon-English/negative-words.txt', what='character', comment.char=';')

## Match sentiment
txt.d$sentiment = factor(ifelse(txt.d$word %in% snt.pos, 'pos',
                         ifelse(txt.d$word %in% snt.neg, 'neg', 'neut')), levels = c('pos','neut','neg'))

head(txt.d)

## Preparing colour palette, create word cloud, and save to a png file
sel.pal = c('#E31A1C', '#999999', '#33A02C')
# sel.pal = brewer.pal(8,"Dark2")
png('output.png', width = 1280, height = 800)
wordcloud(txt.d$word, txt.d$freq, scale=c(8,.2), max.words=100, min.freq = 6,
          random.order=F, rot.per=0, colors=sel.pal[txt.d$sentiment], ordered.colors = T)
dev.off()

# Positive words only
txt.dp = txt.d[txt.d$sentiment == 'pos',]
png('pos.png', width = 1280, height = 800)
wordcloud(txt.dp$word,txt.dp$freq, scale=c(8,.2), max.words=50, 
          random.order=F, rot.per=0, colors='#33A02C')
dev.off()

# Negative words only
txt.dn = txt.d[txt.d$sentiment == 'neg',]
png('neg.png', width = 1280, height = 800)
wordcloud(txt.dn$word,txt.dn$freq, scale=c(8,.2), max.words=50, 
          random.order=F, rot.per=0, colors='#E31A1C')
dev.off()


