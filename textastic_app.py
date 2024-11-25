from textastic import Textastic
import textastic_parsers as tp
import pprint as pp

def main():

    tt = Textastic()
    tt.load_text('data/Energy_Sector.json')
    tt.load_text('data/Healthcare.json')
    tt.load_text('data/Investment_Finance.json')
    tt.load_text('data/Retail.json')
    tt.load_text('data/Technology.json')
    tt.load_text('data/Other.json')

    print(tt.data)

    #tt.compare_num_words()
    #tt.wordcount_sankey(word_list= ['customers'], k=5)
    #tt.wordcloud_subplots(cols=2)
    tt.heatmap_word_frequencies(["innovation", "customers", "growth", "sustainability", "technology"])


if __name__ == '__main__':
    main()