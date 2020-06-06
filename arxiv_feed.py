import arxiv
from arxiv_output import window_results, print_results

class Arxiv_Feed:

    def __init__(self, query="", n_results=10, n_result_chunks=1,
                 sorting="lastUpdatedDate", sorting_order="descending",
                 key_list=[], window=True):

        if not query:
            print("No query specified!")
        else:
            self.query = query
        self.keys = []
        if not key_list:
            print("No keys specified, using defaults")
            key_list = ["title", "summary", "pdf_url", "arxiv_primary_category/term"]
        for key in key_list:
            self.keys.append(key.split('/'))

        self.keywords = self.keyword_map(self.keys)
        self.n_results = n_results
        self.n_result_chunks = n_result_chunks
        self.sorting = sorting
        self.sorting_order = sorting_order
        self.window = window

    def run(self):
        res = self.query_arxiv()
        sorted_res = self.sort_results(res, "neutrino", "hep-ex", "hep-ph")
        print("Obtained ", len(sorted_res), " results")
        if len(res) is not 0:
            if self.window:
                window_results(sorted_res, self.keywords)
            else:
                print_results(sorted_res, self.keywords)
        else:
            print("No results received")

    def query_arxiv(self):
        # add time
        results = arxiv.query(query=self.query,
                              max_results=self.n_results,
                              max_chunk_results=self.n_result_chunks,
                              sort_by=self.sorting,
                              sort_order=self.sorting_order,
                              iterative=False)
        if not results:
            print("No results returned")
            return
        return self.parse_results(results)

    def parse_results(self, results):
        n_results = len(results)
        extracted_results = []
        try:
            for paper in results:
                paper_results = []
                for key in self.keys:
                    if len(key) is 1:
                        res = paper.get(key[0]).splitlines()
                    elif len(key) is 2:
                        res = paper.get(key[0]).get(key[1]).splitlines()
                    paper_results.append(' '.join(res))
                extracted_results.append(paper_results)
                n_results -= 1

            return extracted_results
        except KeyError:
            print("Key error, missed ", n_results, " results")
            return extracted_results

    @staticmethod
    def sort_results(result_list, kword, cat_order1, cat_order2):
        def contains_word(string, word):
            return f' {word} ' in f' {string} '

        first, second, third, fourth = [], [], [], []
        for paper in result_list:
            if contains_word(paper[0], kword) or contains_word(paper[1], kword):
                first.append(paper)
            elif paper[3] == cat_order1:
                second.append(paper)
            elif paper[3] == cat_order2:
                third.append(paper)
            else:
                fourth.append(paper)
        first.extend(second)
        first.extend(third)
        first.extend(fourth)
        return first

    @staticmethod
    def keyword_map(keys):
        kw = []
        for key in keys:
            if key[0] == "title":
                kw.append("Title")
            elif key[0] == "summary":
                kw.append("Abstract")
            elif key[0] == "pdf_url":
                kw.append("URL")
            elif key[0] == "arxiv_primary_category":
                kw.append("Category")
            else:
                kw.append("Other")
        return kw


if __name__ == '__main__':
    query_string = "hep-ex"
    arxiv_feed = Arxiv_Feed(query=query_string, n_results=10, window=True)
    arxiv_feed.run()
