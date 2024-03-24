'''
A GUI application that allows user to input a query and get the most relevant search
results (items from heureka) from a neural network model. 
'''

import tkinter
from inference import Inference
import logging 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Heureka Search Engine")
        self.root.geometry("800x600")

        self.query = tkinter.StringVar()
        self.results = tkinter.StringVar()

        self.label = tkinter.Label(self.root, text="Enter a query:")
        self.label.pack()

        self.entry = tkinter.Entry(self.root, textvariable=self.query)
        self.entry.pack()

        self.button = tkinter.Button(self.root, text="Search", command=self.search)
        self.button.pack()

        self.listbox = tkinter.Listbox(self.root, listvariable=self.results)
        self.listbox.pack()

    def search(self):
        query = self.query.get()
        logger.info(f'Searching for the query: {query}')
        search_results = inference.get_search_results(query)
        self.results.set(search_results)

if __name__ == "__main__":
    inference = Inference(embed_file='kancelarska-kresla_embeddings.npy')
    root = tkinter.Tk()
    app = App(root)
    root.mainloop()


