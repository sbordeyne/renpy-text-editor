from librpydb.baseconf import DEBUGGER_PORT
from librpydb.debugger import Breakpoint, DebuggerState, RenpyDebugger
import tkinter as tk
import threading
import tkinter.font as tkfont
from RTE.config import config


class DebuggerView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        w = config.wm_width - config.side_notebook_width
        self.text = tk.Text(self, height=10)

        self.vsb = tk.Scrollbar(self, orient="vertical",
                                command=self.text.yview)

        font = tkfont.Font(font=self.text["font"])

        self.text.config(width=w // font.measure(" "),
                         yscrollcommand=self.vsb.set)

        self.text.bind("<Key>", self.on_key_press)

        self.debugger = RenpyDebugger("127.0.0.1",
                                      DEBUGGER_PORT)
        self.execution_paused_state = None
        self.execution_threads = []
        self.executed_thread = None
        self.executed_stack_frames = None
        self.executed_stack_frame = None
        self.showing_variables = None

        self.debugger.set_connected_callback(self.on_connected)
        self.debugger.set_disconnected_callback(self.on_disconnected)
        self.debugger.set_client_error_callback(self.on_client_error)
        self.debugger.set_pause_callback(self.on_paused)

        self.text.grid(row=0, column=0, columnspan=49)
        self.vsb.grid(row=0, column=50, sticky="ns")
        self.loop()

    def on_key_press(self, event):
        if event.keysym == "Return":
            self.on_key_return(event)
        else:
            self.text.insert(tk.END, event.char)
        return "break"

    def on_key_return(self, event):
        cmd = self.text.get("end -1 lines linestart", "end -1 lines lineend")
        try:
            command, *args = cmd.split()
            self.print()
            self.send_command(command, *args)
        except ValueError:
            self.print()
            self.send_command(cmd.rstrip())
        pass

    def send_command(self, cmd, *args):
        if cmd == "h":
            self.help_cmd()
        pass

    @property
    def is_paused(self):
        return self.execution_paused_state is not None and \
            self.execution_paused_state.is_valid()

    @property
    def thread_executing(self):
        return self.executed_thread is not None and \
            self.executed_thread.is_valid()

    def print(self, message="", end="\n"):
        self.text.insert(tk.END, message + end)

    def on_connected(self, *args, **kwargs):
        self.print("Connected!")


    def on_disconnected(self, *args, **kwargs):
        self.print("Disconnected!")
        self.execution_paused_state = None


    def on_paused(self, stop_reason, description, exc):
        class IThread(threading.Thread):
            def __init__(self, master, exc, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.master = master
                self.exc = exc

            def run(self):
                self.master.execution_paused_state = self.exc
                self.master.execution_threads = self.exc.get_threads()
                self.master.executed_thread = self.master.execution_threads[0]
                self.master.executed_stack_frames = self.master.executed_thread.get_stack_frames()
                self.master.executed_stack_frame = self.master.executed_stack_frames[0]

        t = IThread(self, exc)
        t.start()
        self.print(f"Paused for {stop_reason} ({description})")


    def on_client_error(*args, **kwargs):
        pass

    def help_cmd(self, **args):
        hlp_msg = """
Available commands:
connect - connects to debugged renpy game on port 14711
          will automatically sync breakpoints")
disconnect - stops debugging, but can still be attached later
b - sets the breakpoint: b game/script.rpy:10
rb - removes breakpoint - arguments can be source, source:line or nothing -> removes all
lb - lists breakpoints
sb - synchronized breakpoints
threads - lists threads, renpy only supports thread 0
bt - shows backtrace of thread
st - st # - switch to stack frame #
bytet - shows bytecode of current frame
scopes - shows scopes
v # - displays subfields of variable # or lists variables in scopes
c - continue (with the) execution
p - pauses execution wherever it is
s - moves execution by next step
si - moves execution into function call
so - moves execution out of call
dinfo - prints debugger state information
"""
        self.print(hlp_msg)

    def set_breakpoint(self, file, line, **args):
        try:
            self.debugger.add_breakpoint(Breakpoint(line, file))
        except BaseException:
            self.print("Failed to insert breakpoint, check syntax")

    def list_breakpoints(self, **args):
        for bp in self.debugger.breakpoints:
            self.print(f"Breakpoint at {bp.source}, line {bp.line}")

    def remove_breakpoint(self, file=None, line=None, **args):
        if file is None or line is None:
            self.debugger.clear_breakpoints()
            self.print("All breakpoints removed")
        elif line is None:
            self.debugger.remove_breakpoint_from_source(file)
        else:
            self.debugger.remove_breakpoint(Breakpoint(line, file))
        self.print("Don't forget to 'sb' to synchronize breakpoints!")

    def connect(self, **args):
        if self.debugger.get_state() == DebuggerState.NOT_CONNECTED:
            self.print("Establishing connection")
            try:
                self.debugger.connect()
            except Exception:
                self.print("Failed. Is a renpy debugged game running?")

    def synchronize_breakpoints(self, **args):
        if self.debugger.get_state() in (DebuggerState.CONNECTED, DebuggerState.CONNECTING):
            self.print("Not connected")
        else:
            self.debugger.sync_breakpoints()
            self.print("Breakpoints synchronized")

    def list_threads(self, **args):
        if self.debugger.get_state() == DebuggerState.NOT_CONNECTED:
            self.print("Not connected")
            return
        if self.is_paused:
            execution_threads = self.execution_paused_state.get_threads()
            self.print("Threads:")
            for it, renpy_thread in enumerate(execution_threads):
                self.print(f"Threads #{it} : {renpy_thread.get_thread_name()}")

    def show_backtrace(self, thread_id="0", **args):
        if self.debugger.get_state() == DebuggerState.NOT_CONNECTED:
            self.print("Not connected")
            return
        if self.is_paused:
            if int(thread_id) >= len(self.execution_threads):
                self.print(f"No thread {thread_id} available")
            else:
                self.print(f"Backtrace for thread [{thread_id}]")
                self.executed_thread = self.execution_threads[int(thread_id)]
                self.executed_stack_frames = self.executed_thread.get_stack_frames()
                id = 0
                for st in self.executed_stack_frames:
                    self.print(f"#{id}: <{st.get_source()}:{st.get_line()}> {st.get_line_of_code()} ")
                    id += 1

    def switch_stack_frame(self, stid=0, **args):
        if self.debugger.get_state() == DebuggerState.NOT_CONNECTED:
            self.print("Not connected")
            return
        if self.thread_executing:
            if stid >= len(self.executed_stack_frames):
                self.print(f"No such stack frame {stid}")
            else:
                self.executed_stack_frame = self.executed_stack_frames[stid]
                self.executed_stack_frame.set_active()
                self.print(f"#{stid}: <{self.executed_stack_frame.get_source()}:{self.executed_stack_frame.get_line()}> {self.executed_stack_frame.get_line_of_code()} ")

    def display_scopes(self, **args):
        if self.debugger.get_state() == DebuggerState.NOT_CONNECTED:
            self.print("Not connected")
            return
        if self.executed_stack_frame is not None and self.executed_stack_frame.is_valid():
            self.showing_variables = self.executed_stack_frame.get_scopes()
            for it, v in enumerate(self.showing_variables):
                self.print(f"#{it}: {v.get_name()} ({v.get_type()}) - {v.get_value()}")

    def display_variable_structure(self, var_ref=None, **args):
        if self.debugger.get_state() == DebuggerState.NOT_CONNECTED:
            self.print("Not connected")
            return
        if var_ref is None:
            self.print("Failed to get variable, check syntax")
            return
        if var_ref >= len(self.showing_variables):
            self.print(f"No such variable {var_ref}")
        else:
            self.showing_variables = list(self.showing_variables[var_ref].get_components().values())
            for it, v in enumerate(self.showing_variables):
                self.print(f"#{it}: {v.get_name()} ({v.get_type()}) - {v.get_value()}")

    def continue_execution(self, **args):
        if self.debugger.get_state() == DebuggerState.NOT_CONNECTED:
            self.print("Not connected")
            return
        if self.thread_executing:
            exct = self.executed_thread
            self.executed_thread = None
            exct.continue_execution()

    def pause_execution(self, **args):
        if self.debugger.get_state() == DebuggerState.NOT_CONNECTED:
            self.print("Not connected")
            return
        if self.debugger.get_state() == DebuggerState.CONNECTED:
            self.debugger.pause()

    def step_execution(self, **args):
        if self.debugger.get_state() == DebuggerState.NOT_CONNECTED:
            self.print("Not connected")
            return
        if self.thread_executing:
            self.executed_thread.step()

    def step_in_execution(self, **args):
        if self.debugger.get_state() == DebuggerState.NOT_CONNECTED:
            self.print("Not connected")
            return
        if self.thread_executing:
            self.executed_thread.step_in()

    def step_out_execution(self, **args):
        if self.debugger.get_state() == DebuggerState.NOT_CONNECTED:
            self.print("Not connected")
            return
        if self.thread_executing:
            self.executed_thread.step_out()

    def disconnect(self, **args):
        if self.debugger.get_state() == DebuggerState.NOT_CONNECTED:
            self.print("Not connected")
            return
        self.debugger.disconnect()

    def dinfo(self):
        msg = f"""
Debugger paused :       {self.execution_paused_state}
Execution threads :     {self.execution_threads}
Executed thread :       {self.executed_thread}
Executed stack frames : {self.executed_stack_frames}
Executed stack frame :  {self.executed_stack_frame}
Showing variables :     {self.showing_variables}
"""
        self.print(msg)

    def loop(self):
        self.after(1, self.loop)

    def resize(self, width, height):
        font = tkfont.Font(font=self.text["font"])
        self.text.config(width=width // font.measure(" "),
                         height=10)
