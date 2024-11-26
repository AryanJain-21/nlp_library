from linguify import Linguify
import linguify_parsers as lp
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

def main():

    client = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
    db = client['fortune_500']


    lg = Linguify()
    lg.load_text(documents=list(db['Energy_Sector'].find()), label='Energy', parser=lp.db_parser)
    lg.load_text(documents=list(db['Healthcare'].find()), label='Healthcare', parser=lp.db_parser)
    lg.load_text(documents=list(db['Investment_Finance'].find()), label='Finance', parser=lp.db_parser)
    lg.load_text(documents=list(db['Retail'].find()), label='Retail', parser=lp.db_parser)
    lg.load_text(documents=list(db['Technology'].find()), label='Tech', parser=lp.db_parser)
    lg.load_text(documents=list(db['Other'].find()), label='Other', parser=lp.db_parser)

    """lg = Linguify()
    lg.load_text(filename='data/Energy_Sector.json', label='Energy', parser=lp.json_parser)
    lg.load_text(filename='data/Healthcare.json', label='Healthcare', parser=lp.json_parser)
    lg.load_text(filename='data/Investment_Finance.json', label='Finance', parser=lp.json_parser)
    lg.load_text(filename='data/Retail.json', label='Retail', parser=lp.json_parser)
    lg.load_text(filename='data/Technology.json', label='Tech', parser=lp.json_parser)
    lg.load_text(filename='data/Other.json', label='Other', parser=lp.json_parser)"""

    lg.wordcount_sankey(k=5)
    lg.wordcloud_subplots(cols=3)
    lg.heatmap_word_frequencies(["clients", "customers", "services", "value", "world", "solutions", "communities"])


if __name__ == '__main__':
    main()