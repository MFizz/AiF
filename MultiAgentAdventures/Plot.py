import random
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from itertools import accumulate
import tkinter as Tk
import tkinter.messagebox

class PlotClassifier(Tk.Tk):
    def __init__(self, plot_generator, arguments, classes, classification_callback, *args, **kwargs):
        Tk.Tk.__init__(self, *args, **kwargs)
        self.title("Plotting of %i games" % len(arguments))
        self._plot_generator = plot_generator
        self._arguments = arguments
        self._pos = 0
        self._classes = [str(x) for x in classes]
        self._classification_callback = classification_callback
        self._setup_gui()

    def _setup_gui(self):
        #self.columnconfigure(0, minsize=100, weight=2)
        #self.columnconfigure(1, minsize=500, weight=8)
        f = Figure()
        self._ax = f.add_subplot(111)
        buttons_frame = Tk.Frame(self)
        buttons_frame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=True)
        buttons_class = []
        for i, cls in enumerate(self._classes):
            buttons_class.append(Tk.Button(master=buttons_frame, text=cls, 
                                           command=lambda x=i: self.button_classification_callback(self._current_args, x)))
            buttons_class[-1].pack(side=Tk.LEFT)
        button_quit = Tk.Button(master=buttons_frame, text='Quit', command=self.destroy)
        button_quit.pack(side=Tk.RIGHT) #.grid(row=0,column=0)

        self._canvas = FigureCanvasTkAgg(f, master=self)
        self._canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1) #.grid(row=0, column=1, rowspan=3) #
        self._canvas.show()

        toolbar = NavigationToolbar2TkAgg( self._canvas, self )
        toolbar.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1) #.grid(row=3, column=1) #
        toolbar.update()

    def button_classification_callback(self, args, class_idx):
        self._classification_callback(args, self._classes[class_idx])
        self.classify_plot(class_idx)

    def classify_next_plot(self):
        try:
            self._current_args = self._arguments[self._pos+1]
            self._pos += 1
            print(self._current_args)
            self._ax.cla()
            self._plot_generator(self._ax, self._current_args)
            self._canvas.draw()
        except IndexError:
            tkinter.messagebox.showinfo("Complete!", "Start from Beginning")
            self.classify_plot(0)

    def classify_plot(self, loc):
        try:
            self._current_args = self._arguments[loc]
            self._pos = loc
            print(self._current_args)
            self._ax.cla()
            self._plot_generator(self._ax, self._current_args)
            self._canvas.draw()
        except IndexError:
            tkinter.messagebox.showinfo("No such dataset")
            self.destroy()


def create_plot(ax, args):
    print(args)
    ax.set_title("Seed %i"%args[2])
    ax.set_ylabel("Gold")
    ax.set_xlabel("Iterations")
    ax.plot(args[0], label = "Algorithm")
    ax.plot(args[1], label = "UpperBound")
    ax.legend(bbox_to_anchor=(0., -0.11, 1, 0), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)

def announce_classification(arguments, class_):
    print(arguments, class_)

def plot(bookers):
    classes = ["Seed %i"%s for b,s in bookers]
    arguments_for_plot = [(list(accumulate(b.reward)), [b.upperBound for i in range(0, len(b.reward))], s) for b,s in bookers]
    print(arguments_for_plot)
    root = PlotClassifier(create_plot, arguments_for_plot, classes, classification_callback=announce_classification)
    root.after(50, root.classify_plot(0))
    root.mainloop()