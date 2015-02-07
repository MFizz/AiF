import random
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from itertools import accumulate
import numpy as np
import tkinter as Tk
import tkinter.messagebox

class PlotClassifier(Tk.Tk):
    def __init__(self, plot_generator_seed, plot_generator_agent,plot_generator_mean,bookers, seed_callback, *args, **kwargs):
        Tk.Tk.__init__(self, *args, **kwargs)
        self.title("Plotting of %i games" % len(bookers))
        self._plot_generator_seed = plot_generator_seed
        self._plot_generator_agent = plot_generator_agent
        self._plot_generator_mean = plot_generator_mean
        self._bookers = bookers
        self._seeds = ["Seed %i"%s for b,s in self._bookers]
        self._seed_args = [(list(accumulate(b.reward)), [b.upperBound for i in range(0, len(b.reward))], [b.greedyBound for i in range(0, len(b.reward))], s) for b,s in bookers]
        self._pos = 0
        self._agent_pos = 0
        self._seed_callback = seed_callback
        self._agents = []
        self._closed_adv_frame = False
        self._setup_gui()

    def _setup_gui(self):
        f = Figure()
        self._ax = f.add_subplot(111)

        self._agent_frame = Tk.Frame(self)
        self._agent_frame.pack(side=Tk.RIGHT, fill=Tk.BOTH, expand=True)
        agent = Figure()
        self._agent_ax = agent.add_subplot(111)

        buttons_seeds_frame = Tk.Frame(self)
        buttons_seeds_frame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=True)
        buttons_seed_class = []
        for i, cls in enumerate(self._seeds):
            buttons_seed_class.append(Tk.Button(master=buttons_seeds_frame, text=cls,
                                           command=lambda x=i: self.button_seeds_callback(self._current_args, x)))
            buttons_seed_class[-1].pack(side=Tk.LEFT)

        button_mean = Tk.Button(master=buttons_seeds_frame, text="Mean",
                                command=self.button_mean_callback)
        button_mean.pack(side=Tk.LEFT)

        self._agent_canvas = FigureCanvasTkAgg(agent, master=self._agent_frame)
        self._agent_canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1) #.grid(row=0, column=1, rowspan=3) #
        self._agent_canvas.show()

        self._buttons_agents_frame = Tk.Frame(self)
        label_mean_current_stats = Tk.Label(self._buttons_agents_frame,text="Agents in current iteration: ")
        label_mean_current_stats.pack()
        self._buttons_agents_frame.pack(side=Tk.RIGHT, fill=Tk.BOTH, expand=True)
        self._buttons_agents_class = []

        button_quit = Tk.Button(master=buttons_seeds_frame, text='Quit', command=self.destroy)
        button_quit.pack(side=Tk.RIGHT) #.grid(row=0,column=0)


        self._canvas = FigureCanvasTkAgg(f, master=self)
        self._canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1) #.grid(row=0, column=1, rowspan=3) #
        self._canvas.show()


        self._text_mean_current_upper = Tk.StringVar()
        self._text_mean_current_greedy = Tk.StringVar()
        self._text_open_adv = Tk.StringVar()
        self._text_completed_adv = Tk.StringVar()
        label_mean_current_stats = Tk.Label(self,text="Statistics of current iteration: ", anchor='w', justify='left', bg="#CCCCCC")
        label_mean_current_stats.pack(fill=Tk.BOTH, expand=1)
        label_mean_current_upper = Tk.Label(self,textvariable=self._text_mean_current_upper, anchor='w', justify='left', bg="#CCCCCC")
        label_mean_current_upper.pack(fill=Tk.BOTH, expand=1)
        label_mean_current_greedy = Tk.Label(self,textvariable=self._text_mean_current_greedy, anchor='w', justify='left', bg="#CCCCCC")
        label_mean_current_greedy.pack(fill=Tk.BOTH, expand=1)
        label_mean_current_greedy = Tk.Label(self,textvariable=self._text_open_adv, anchor='w', justify='left', bg="#CCCCCC")
        label_mean_current_greedy.pack(fill=Tk.BOTH, expand=1)
        label_mean_current_greedy = Tk.Label(self,textvariable=self._text_completed_adv, anchor='w', justify='left', bg="#CCCCCC")
        label_mean_current_greedy.pack(fill=Tk.BOTH, expand=1)


        hline=Tk.Frame(self,height=1,bg="black")
        hline.pack(fill='x')

        mean_percentage_upper = sum([sum(b.reward)/b.upperBound for b,s in self._bookers])/len(self._bookers)
        mean_percentage_greedy = sum([sum(b.reward)/b.greedyBound for b,s in self._bookers])/len(self._bookers)
        label_mean_stats = Tk.Label(self,text="Statistics over all iterations: ", anchor='w', justify='left', bg="#CCCCCC")
        label_mean_stats.pack(fill=Tk.BOTH, expand=1)
        label_mean_upper = Tk.Label(self,text="Mean percentage of upper bound: %f"%mean_percentage_upper, anchor='w', justify='left', bg="#CCCCCC")
        label_mean_upper.pack(fill=Tk.BOTH, expand=1)
        label_mean_greedy = Tk.Label(self,text="Mean percentage of upper bound: %f"%mean_percentage_greedy, anchor='w', justify='left', bg="#CCCCCC")
        label_mean_greedy.pack(fill=Tk.BOTH, expand=1)
        mean_open_adv = np.mean([len(b.adventures) for b,s in self._bookers])
        label_mean_open_adv = Tk.Label(self,text="Mean open adventures: %f"%mean_open_adv, anchor='w', justify='left', bg="#CCCCCC")
        label_mean_open_adv.pack(fill=Tk.BOTH, expand=1)
        mean_completed_adv = np.mean([len(b.completedAdventures) for b,s in self._bookers])
        label_mean_completed_adv = Tk.Label(self,text="Mean completed adventures: %f"%mean_completed_adv, anchor='w', justify='left', bg="#CCCCCC")
        label_mean_completed_adv.pack(fill=Tk.BOTH, expand=1)


        toolbar = NavigationToolbar2TkAgg( self._canvas, self )
        toolbar.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1) #.grid(row=3, column=1) #
        toolbar.update()


    def button_seeds_callback(self, args, seed_idx):
        self._seed_callback(args, self._seeds[seed_idx])
        self.seed_plot(seed_idx)

    def button_mean_callback(self):
        self.mean_plot()

    def button_agents_callback(self, agent_idx):
        self.agent_plot(agent_idx)

    def seed_next_plot(self):
        try:
            self.seed_plot(self._pos+1)
        except IndexError:
            tkinter.messagebox.showinfo("Complete!", "Start from Beginning")
            self.seed_plot(0)

    def mean_plot(self):
        self._ax.cla()
        averageGreedyBound = [np.mean([b.greedyBound for b,s in self._bookers]) for i in range(0,len(self._bookers[0][0].reward))]
        averageUpperBound = [np.mean([b.upperBound for b,s in self._bookers]) for i in range(0,len(self._bookers[0][0].reward))]
        averageAlgorithm = np.mean([list(accumulate(b.reward)) for b,s in self._bookers],axis=0)
        args = (averageAlgorithm,averageUpperBound,averageGreedyBound)
        self._plot_generator_mean(self._ax, args)
        self._canvas.draw()


    def seed_plot(self, loc):
        try:
            self._current_args = self._seed_args[loc]
            self._pos = loc
            self._ax.cla()
            self.update_agent_gui()
            self._plot_generator_seed(self._ax, self._current_args)
            self._canvas.draw()
            mean_percentage_upper = sum(self._bookers[loc][0].reward)/ self._bookers[loc][0].upperBound
            self._text_mean_current_upper.set("Mean percentage of upper bound: %f"%mean_percentage_upper)
            mean_percentage_greedy = sum(self._bookers[loc][0].reward)/ self._bookers[loc][0].greedyBound
            self._text_mean_current_greedy.set("Mean percentage of upper bound: %f"%mean_percentage_greedy)
            open_adv = len(self._bookers[loc][0].adventures)
            compl_adv = len(self._bookers[loc][0].completedAdventures)
            self._text_open_adv.set("Open adventures: %i"%open_adv)
            self._text_completed_adv.set("Completed adventures: %i"%compl_adv)
        except IndexError:
            tkinter.messagebox.showinfo("No such dataset")
            self.destroy()

    def agent_plot(self,pos):
        try:
            if self._closed_adv_frame:
                self._closed_adv_frame.destroy()
            self._closed_adv_frame = Tk.Frame(self._agent_frame)
            self._closed_adv_frame.pack(fill=Tk.BOTH, expand=1)
            cur_agent = self._bookers[self._pos][0].agents[pos]
            print(cur_agent.skillList)
            print(cur_agent.skillListBegin)
            agent_skills = ", ".join(["{}: {}".format(s.name, p) for s, p in cur_agent.skillList])
            agent_skills_beg = ", ".join(["{}: {}".format(s.name, p) for s, p in cur_agent.skillListBegin])
            label_agent_current_astats = Tk.Label(master=self._closed_adv_frame,text="Statistics of current agent: \n"
                                                                                 "Agent's skills: {} \n"
                                                                                 "At beginning: {}".format(agent_skills, agent_skills_beg)
                                              , anchor='w', justify='left', bg="#CCCCCC")
            label_agent_current_astats.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
            labels_adv=[]
            for adv, iter in cur_agent.closedAdvs:
                adv_skills = ", ".join(["{}: {}".format(s.name, p) for s, p in adv.skillMap.items()])
                agent_cur_skills = ", ".join(["{}: {}".format(s.name, p) for s, p in [s for a,s in adv.bestCoalition.agentList if a == cur_agent][0]])
                labels_adv.append(Tk.Label(master=self._closed_adv_frame, text="In round {} \n{} was comleted \n"
                                                                           "it needed: {} \n"
                                                                           "Agent put in: {}\n ".format(iter, adv, adv_skills, agent_cur_skills), anchor='w', justify='left', bg="#CCCCCC"))
                labels_adv[-1].pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)

            self._agent_ax.cla()
            args = (list(accumulate(self._bookers[self._pos][0].agents[pos].rewards)),
                    list(accumulate(self._bookers[self._pos][0].agents[pos].finalCosts)),
                    list(accumulate(self._bookers[self._pos][0].agents[pos].earnings)),
                    id(self._bookers[self._pos][0].agents[pos]))
            self._plot_generator_agent(self._agent_ax, args)
            toolbar = NavigationToolbar2TkAgg( self._agent_canvas, self._agent_frame)
            toolbar.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1) #.grid(row=3, column=1) #
            toolbar.update()
            self._agent_canvas.draw()

        except IndexError:
            tkinter.messagebox.showinfo("No such Agent")
            self.destroy()

    def update_agent_gui(self):
        for b in self._buttons_agents_class:
            b.destroy()

        self._buttons_agents_class = []

        self._agents = ["Agent %i earns: %i"%(id(a), sum(a.earnings)) for a in self._bookers[self._pos][0].agents]

        for i, cls in enumerate(self._agents):
            self._buttons_agents_class.append(Tk.Button(master=self._buttons_agents_frame, text=cls,
                                           command=lambda x=i: self.button_agents_callback(x)))
            self._buttons_agents_class[-1].pack()

        self.agent_plot(0)



def create_plot_mean(ax, args):

    ax.set_title("Means: ")
    ax.set_ylabel("Gold")
    ax.set_xlabel("Iterations")
    ax.plot(args[0], label = "Algorithm")
    ax.plot(args[1], label = "UpperBound")
    ax.plot(args[2], label = "GreedyBound")
    ax.grid(True)
    ax.legend(bbox_to_anchor=(1., 0.05), loc='lower right',
           ncol=1)


def create_plot_seed(ax, args):

    ax.set_title("Seed %i"%args[3])
    ax.set_ylabel("Gold")
    ax.set_xlabel("Iterations")
    ax.plot(args[0], label = "Algorithm")
    ax.plot(args[1], label = "UpperBound")
    ax.plot(args[2], label = "GreedyBound")
    ax.grid(True)
    ax.legend(bbox_to_anchor=(1., 0.05), loc='lower right',
           ncol=1)

def create_plot_agents(ax, args):
    ax.set_title("Agent %i"%args[3])
    ax.set_ylabel("Gold")
    ax.set_xlabel("Iterations")
    ax.plot(args[0], label = "Reward")
    ax.plot(args[1], label = "Costs")
    ax.plot(args[2], label = "Earnings")
    ax.grid(True)
    ax.legend(bbox_to_anchor=(1., 0.05), loc='lower right',
           ncol=1)

def announce_seed(arguments, class_):
    a =1
    #print(arguments, class_)

def plot(bookers):
    root = PlotClassifier(create_plot_seed, create_plot_agents, create_plot_mean, bookers, seed_callback=announce_seed)
    root.after(50, root.seed_plot(0))
    root.mainloop()

