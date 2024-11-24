from textastic import Textastic
import textastic_parsers as tp
import pprint as pp

def main():

    tt = Textastic()
    tt.load_text('data/fortune_500_one.json')
    tt.load_text('data/fortune_500_two.json')
    tt.load_text('data/fortune_500_three.json')
    tt.load_text('data/fortune_500_four.json')
    tt.load_text('data/fortune_500_five.json')

    print(tt.data)

    tt.compare_num_words()
    tt.wordcount_sankey(k=5)
    tt.wordcloud_subplots(cols=2)

if __name__ == '__main__':
    main()