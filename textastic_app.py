from textastic import Textastic
import textastic_parsers as tp
import pprint as pp

def main():

    tt = Textastic()
    tt.load_text(filename='data/Energy_Sector.json', label='Energy', parser=tp.custom_parser)
    tt.load_text(filename='data/Healthcare.json', label='Healthcare', parser=tp.custom_parser)
    tt.load_text(filename='data/Investment_Finance.json', label='Finance', parser=tp.custom_parser)
    tt.load_text(filename='data/Retail.json', label='Retail', parser=tp.custom_parser)
    tt.load_text(filename='data/Technology.json', label='Tech', parser=tp.custom_parser)
    tt.load_text(filename='data/Other.json', label='Other', parser=tp.custom_parser)
    
    tt.wordcount_sankey(k=5)
    tt.wordcloud_subplots(cols=3)
    tt.heatmap_word_frequencies(["clients", "customers", "improve", "services", "products", "world", "solutions", "communities"])


if __name__ == '__main__':
    main()