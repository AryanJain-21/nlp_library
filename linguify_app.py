from linguify import Linguify
import linguify_parsers as lp

def main():

    lg = Linguify()
    lg.load_text(filename='data/Energy_Sector.json', label='Energy', parser=lp.custom_parser)
    lg.load_text(filename='data/Healthcare.json', label='Healthcare', parser=lp.custom_parser)
    lg.load_text(filename='data/Investment_Finance.json', label='Finance', parser=lp.custom_parser)
    lg.load_text(filename='data/Retail.json', label='Retail', parser=lp.custom_parser)
    lg.load_text(filename='data/Technology.json', label='Tech', parser=lp.custom_parser)
    lg.load_text(filename='data/Other.json', label='Other', parser=lp.custom_parser)

    lg.wordcount_sankey(k=5)
    lg.wordcloud_subplots(cols=3)
    lg.heatmap_word_frequencies(["clients", "customers", "improve", "services", "products", "world", "solutions", "communities"])


if __name__ == '__main__':
    main()