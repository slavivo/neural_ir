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

        self.label = tkinter.Label(self.root, text="Enter a query:", font=('Arial', 20))
        self.label.grid(row=0, column=0, sticky='W')

        self.entry = tkinter.Entry(self.root, textvariable=self.query, font=('Arial', 20))
        self.entry.grid(row=1, column=0, sticky='WE')  # Fill horizontally

        self.button = tkinter.Button(self.root, text="Search", command=self.search, font=('Arial', 20))
        self.button.grid(row=2, column=0)

        self.listbox = tkinter.Listbox(self.root, listvariable=self.results, font=('Arial', 20))
        self.listbox.grid(row=3, column=0, sticky='NSEW')  # Fill both horizontally and vertically

        # Configure the grid to expand properly
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

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


