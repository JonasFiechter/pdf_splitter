def fill_progress_bar(self):
    fraction = 100 / self.pages
    self.progress += fraction

    self.progressBar.setValue(round(self.progress))