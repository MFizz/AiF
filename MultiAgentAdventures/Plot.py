import random
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from itertools import accumulate
import tkinter as Tk
import tkinter.messagebox

class PlotClassifier(Tk.Tk):
    def __init__(self, plot_generator_seed, bookers, seed_callback, *args, **kwargs):
        Tk.Tk.__init__(self, *args, **kwargs)
        self.title("Plotting of %i games" % len(bookers))
        self._plot_generator_seed = plot_generator_seed
        self._bookers = bookers
        self._seeds = ["Seed %i"%s for b,s in self._bookers]
        self._seed_args = [(list(accumulate(b.reward)), [b.upperBound for i in range(0, len(b.reward))], [b.greedyBound for i in range(0, len(b.reward))], s) for b,s in bookers]
        self._pos = 0
        self._seed_callback = seed_callback
        self._setup_gui()

    def _setup_gui(self):
        f = Figure()
        self._ax = f.add_subplot(111)
        buttons_seeds_frame = Tk.Frame(self)
        buttons_seeds_frame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=True)
        buttons_seed_class = []
        for i, cls in enumerate(self._seeds):
            buttons_seed_class.append(Tk.Button(master=buttons_seeds_frame, text=cls,
                                           command=lambda x=i: self.button_seeds_callback(self._current_args, x)))
            buttons_seed_class[-1].pack(side=Tk.LEFT)

        button_quit = Tk.Button(master=buttons_seeds_frame, text='Quit', command=self.destroy)
        button_quit.pack(side=Tk.RIGHT) #.grid(row=0,column=0)

        button_means = Tk.Button(master=buttons_seeds_frame, text='Means', command=self.destroy)
        button_means.pack(side=Tk.RIGHT) #.grid(row=0,column=0)
        #buttons_agent_frame = Tk.Frame
        #buttons_agent_frame.pack(side=Tk.RIGHT, fill=Tk.BOTH, expand=True)
        #buttons_agent_class = []


        self._canvas = FigureCanvasTkAgg(f, master=self)
        self._canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1) #.grid(row=0, column=1, rowspan=3) #
        self._canvas.show()

        toolbar = NavigationToolbar2TkAgg( self._canvas, self )
        toolbar.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1) #.grid(row=3, column=1) #
        toolbar.update()

    def button_seeds_callback(self, args, seed_idx):
        self._seed_callback(args, self._seeds[seed_idx])
        self.seed_plot(seed_idx)

    def seed_next_plot(self):
        try:
            self.seed_plot(self._pos+1)
        except IndexError:
            tkinter.messagebox.showinfo("Complete!", "Start from Beginning")
            self.seed_plot(0)

    def seed_plot(self, loc):
        try:
            self._current_args = self._seed_args[loc]
            self._pos = loc
            print(self._current_args)
            self._ax.cla()
            self._plot_generator_seed(self._ax, self._current_args)
            self._canvas.draw()
        except IndexError:
            tkinter.messagebox.showinfo("No such dataset")
            self.destroy()


def create_plot_seed(ax, args):
    print(args)
    ax.set_title("Seed %i"%args[3])
    ax.set_ylabel("Gold")
    ax.set_xlabel("Iterations")
    ax.plot(args[0], label = "Algorithm")
    ax.plot(args[1], label = "UpperBound")
    ax.plot(args[2], label = "GreedyBound")
    ax.legend(bbox_to_anchor=(1., 0.05), loc='lower right',
           ncol=1)

def announce_seed(arguments, class_):
    print(arguments, class_)

def plot(bookers):
    classes = ["Seed %i"%s for b,s in bookers]
    root = PlotClassifier(create_plot_seed, bookers, seed_callback=announce_seed)
    root.after(50, root.seed_plot(0))
    root.mainloop()

