import tkinter
import random
import zono.song
import tkinter.simpledialog
import tkinter.messagebox
import time
import matplotlib.pyplot as plt

class Test:
    def __init__(self,table,questions=None):
        self.tabel = table
        if questions:self.questions = questions
        else:self.questions = [(self.tabel,i) for i in range(1,self.tabel+1)]
        random.shuffle(self.questions)
        self.questions_iter = iter(self.questions)
        self.timeout_id = None
        self.current_question = next(self.questions_iter)
        self.question_times = {}
        self.root = tkinter.Tk()
        self.qlabel = tkinter.Label(self.root,text=self.form_q())    
        self.qentry = tkinter.Entry(self.root)
        self.qsubmit = tkinter.Button(self.root,text='submit',command=self.submit)
        self.root.bind('<Return>',lambda x:self.submit())
        self.qlabel.pack()
        self.qentry.pack()
        self.qsubmit.pack()
        self.lastqstime = None
        self.question_index = 0
        self.correct = 0

    def form_q(self):
        return f'{self.current_question[0]}X{self.current_question[1]}'
    def end_test(self):
        self.root.destroy()
        avrg = sum(self.question_times.values())/len(self.question_times)
        tkinter.messagebox.showinfo('Test over',f'Average time to awnser {round(avrg,2)}s')
        if self.correct==0:msg = 'You should practice more'
        elif (len(self.questions)/self.correct)>80:msg = 'You should practice more'
        else:msg = 'Good job!'
        tkinter.messagebox.showinfo(f'Test over {msg}',f'{msg},you scored {self.correct}/{len(self.questions)}')
        self.plot_results()

    def save_question_results(self,q):
        if self.lastqstime is None:return
        tta = time.time()-self.lastqstime
        self.question_times[q] = tta

    def timeout(self,qid):
        if qid != self.question_index:return
        s = zono.song.song('./wrong.mp3')
        s.play(100)
        s.mp3.set_time(2100)
        self.next_question()

    def plot_results(self):
        plt.bar(list(self.question_times.keys()), list(self.question_times.values()), color ='maroon',width = 0.4)
        plt.xlabel("Question")
        plt.ylabel("Time taken")
        plt.title("Time taken per awnser")
        plt.show()

    def submit(self):
        value = self.qentry.get()
        if not value:return
        try:int(value)
        except:return
        if self.current_question[0]*self.current_question[1] == int(value):  
            zono.song.song('./beep.mp3').play(100)
            self.correct+=1
        else:
            s = zono.song.song('./wrong.mp3')
            s.play(100)
            s.mp3.set_time(2100)
        self.next_question()
        
    def next_question(self):
        self.save_question_results(self.form_q())
        _nq = next(self.questions_iter,None)
        if _nq is None:return self.end_test()
        self.current_question = _nq
        self.question_index+=1
        self.qlabel.config(text=self.form_q())
        self.qentry.delete(0,'end')
        self.lastqstime = time.time()
        if self.timeout_id:self.root.after_cancel(self.timeout_id)
        self.timeout_id = self.root.after(3000,self.timeout,self.question_index)

    def run(self):
        self.timeout_id = self.root.after(3000,self.timeout,self.question_index)
        self.lastqstime = time.time()
        self.root.mainloop()
if tkinter.messagebox.askyesno('Mode','Would you a random test?'):
    _max = tkinter.simpledialog.askinteger('Table','Enter the biggest timetable to be used')
    if _max:Test(0,[(random.randint(1,_max),random.randint(1,_max)) for _ in range(12)]).run()
else:
    a = tkinter.simpledialog.askinteger('Table','Enter times table to use for test')
    if a:Test(a).run()