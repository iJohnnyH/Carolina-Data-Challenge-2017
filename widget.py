import matplotlib.pyplot as plt
from matplotlib.widgets import Button

#plt.subplots_adjust(bottom=0.2)


class Index(object):
    ind = 1
    def next(self, event):
        self.ind += 1
        if (self.ind > 13):
            self.ind = 1
        for txt in text.texts:
            txt.set_visible(False)
        textvar = text.text(0, 0, self.ind, fontsize=28)
        plt.draw()
        print (self.ind)
    def prev(self, event):
        self.ind -= 1
        if (self.ind < 1):
            self.ind = 13
        for txt in text.texts:
            txt.set_visible(False)
        textvar = text.text(0, 0, self.ind, fontsize=28)
        plt.draw()
        print (self.ind)

callback = Index()
axprev = plt.axes([0.5, 0.05, 0.2, 0.075])
axnext = plt.axes([0.75, 0.05, 0.2, 0.075])
text = plt.axes([0.0, 0.05, 0.0, 0.075])
textvar = text.text(0, 0, 1, fontsize=28)
text.axis('off')
bnext = Button(axnext, 'Next district')
bnext.on_clicked(callback.next)
bprev = Button(axprev, 'Previous district')
bprev.on_clicked(callback.prev)

plt.show()
