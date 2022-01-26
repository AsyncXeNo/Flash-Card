import pandas


class WordsData(object):
    def __init__(self, csv_file_path):
        self.df = pandas.read_csv(csv_file_path)

    def get_headers(self):
        return self.df.columns.to_list()

    def get_entry(self):
        try:
            entry = self.df.sample()
            self.df.drop(index=entry.index, inplace=True)
            return{
                "front": entry[self.get_headers()[0]].to_list()[0],
                "back": entry[self.get_headers()[1]].to_list()[0]
            }
        except ValueError:
            return None
