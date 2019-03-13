# py23 compatible
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import

import threading
import time
import socket
import traceback

from collections import OrderedDict

from .protocol import *
from .utils import Counter


class DebuggerState(object):
    NOT_CONNECTED = 0
    CONNECTING = 1
    CONNECTED = 2
    EXECUTION_PAUSED = 3


class TerminationReason(object):
    ASKED_TO_TERMINATE = 0
    CLIENT_TERMINATED = 1
    UNRECOVERABLE_DEBUGGER_ERROR = 2
    UNRECOVERABLE_DEBUGGEE_ERROR = 3


class StopReason(object):
    PAUSED = 0
    BREAKPOINT = 1


class Breakpoint(object):
    def __init__(self, line, source):
        self.line = line
        self.source = source

    def __eq__(self, o):
        return self.line == o.line and self.source == o.source

    def __hash__(self):
        return self.line.__hash__() ^ self.source.__hash__()


def _wait_cycle(return_method):
    """
    Applies decorator to two methods, one that is internal return method and one that is
    actuall request method.

    If callback is present in kwargs, this wrapper returns immediately otherwise
    it will block until data is returned.
    """
    def inner_cycle(request_method):

        def request_method_wrapper(self, pass_arg=None, callback=None, *args, **kwargs):
            if not self.is_valid():
                raise RuntimeError("%s is not valid!" % (repr(self)))

            real_self = self

            if not isinstance(self, RenpyDebugger):
                self = self.get_debugger()

            if callback is not None:
                def wait_callback(request_id):
                    if pass_arg is not None:
                        callback(return_method(real_self, pass_arg))
                    else:
                        callback(return_method(real_self))

                self._wait_callback = wait_callback

            request_id = request_method(real_self, *args, **kwargs)

            if callback is None:
                while not self._requests[request_id].ready:
                    time.sleep(0.1)  # spinlock
                if pass_arg is not None:
                    return return_method(real_self, pass_arg)
                else:
                    return return_method(real_self)
            else:
                self._requests[request_id].set_callback(self._wait_callback)
                return None  # NO WAIT
        return request_method_wrapper
    return inner_cycle


class RenpyDebugger(threading.Thread):
    """
    Renpy debugger instance. This should be created once for debugged game.

    It can be reset multiple times though.
    """
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.daemon = True

        self._ip = ip
        self._port = port
        self.stopped = False

        self.socket = None
        self._cleanup()
        self.breakpoints = set()
        self.removed_breakpoints = set()

        # initialize no op callbacks
        self.set_connected_callback()
        self.set_disconnected_callback()
        self.set_client_error_callback()
        self.set_pause_callback()

        self._wait_callback = None
        self._request_lock = threading.Lock()

        self.start()

    def run(self):
        self._run()

    def _run(self):
        try:
            while not self.stopped:
                if self.state == DebuggerState.NOT_CONNECTED:
                    time.sleep(0.1)
                    continue

                try:
                    message = DAPBaseMessage.recv(self.socket)
                except BaseException as e:
                    # failure while communicating
                    traceback.print_exc()

                    self._stop_debugging()
                    self.disconnected_callback(TerminationReason.UNRECOVERABLE_DEBUGGER_ERROR, e)

                # print(message)  # debug print
                if message is None:
                    self._client_disconnected()
                elif message is not None:
                    if isinstance(message, DAPErrorResponse):
                        # TODO implement
                        pass

                    else:
                        # valid message

                        # initialization
                        if isinstance(message, DAPInitializeResponse):
                            self._init_handshake2()
                        if isinstance(message, DAPInitializedEvent):
                            self._init_handshake3()
                        if isinstance(message, DAPLaunchResponse):
                            self._connected()

                        # disconnect
                        if isinstance(message, DAPDisconnectResponse):
                            self._client_disconnected()

                        # data responses
                        if isinstance(message, DAPStoppedEvent):
                            self._resolve_stopped_event(message)
                        if isinstance(message, DAPThreadsResponse):
                            self._resolve_threads(message)
                        if isinstance(message, DAPStackTraceResponse):
                            self._resolve_stack_traces(message)
                        if isinstance(message, DAPScopesResponse):
                            self._resolve_scopes(message)
                        if isinstance(message, DAPVariablesResponse):
                            self._resolve_variables(message)

                        if isinstance(message, DAPResponse):
                            if message.get_request_seq() in self._requests:
                                request = self._requests[message.get_request_seq()]
                                request.set_ready()

                        # rest of messages ignored!


        finally:
            self._stop_debugging()

    def is_valid(self):
        return not self.stopped

    def _client_disconnected(self):
        self._cleanup()
        self.disconnected_callback(TerminationReason.CLIENT_TERMINATED, None)

    def _stop_debugging(self):
        self.stopped = True
        self._cleanup()

    def _continue_with_the_execution(self):
        if self.state != DebuggerState.EXECUTION_PAUSED:
            raise RuntimeError("bad state")

        self.current_states = set()
        self.state = DebuggerState.CONNECTED

    def _cleanup(self):
        self.rq_counter = Counter()
        self._requests = {}
        self.state = DebuggerState.NOT_CONNECTED
        self.current_states = set()

        try:
            if self.socket is not None:
                self.socket.close()
        except Exception:
            pass

        self.socket = None

    def _send_request(self, waiter, request, request_id):
        self._requests[request_id] = _MessageState(self._request_lock, request_id, waiter)
        request.send(self.socket)

    def _mk_breakpoints(self):
        source_map = {}
        for bk in self.breakpoints:
            src = bk.source
            line = bk.line
            if src not in source_map:
                source_map[src] = set()
            source_map[src].add(line)

        for bk in self.removed_breakpoints:
            src = bk.source
            line = bk.line
            if src not in source_map:
                source_map[src] = set()
        self.removed_breakpoints.clear()

        breakpoint_requests = []
        for source in source_map:
            src = DAPSource.create(path=source)
            bkpts = []

            for l in source_map[source]:
                bkpts.append(DAPSourceBreakpoint.create(l))

            args = DAPSetBreakpointsArguments.create(src, bkpts)
            req = DAPSetBreakpointsRequest.create(self.rq_counter.get(), args)

            breakpoint_requests.append(req)

        return breakpoint_requests

    # internal resolve events

    def _resolve_stopped_event(self, event):
        self.state = DebuggerState.EXECUTION_PAUSED
        stop_reason = event.get_body().get_reason()
        stop_description = event.get_body().get_description_or_default("")
        res = RenpyExecutionState(self)
        self.current_states.add(res)
        self.pause_callback(stop_reason, stop_description, res)

    def _resolve_threads(self, response):
        request = self._requests[response.get_request_seq()]
        request.waiter._load_threads(response.get_body())
        request.set_ready()

    def _resolve_stack_traces(self, response):
        request = self._requests[response.get_request_seq()]
        request.waiter._load_stack_traces(response.get_body())
        request.set_ready()

    def _resolve_scopes(self, response):
        request = self._requests[response.get_request_seq()]
        request.waiter._load_scopes(response.get_body())
        request.set_ready()

    def _resolve_variables(self, response):
        request = self._requests[response.get_request_seq()]
        request.waiter._load_variables(response.get_body())
        request.set_ready()

    def _init_handshake1(self):
        self.state = DebuggerState.CONNECTING

        request_id = self.rq_counter.get()
        DAPInitializeRequest.create(request_id, DAPInitializeRequestArguments.create(0)).send(self.socket)

    def _init_handshake2(self):
        self.sync_breakpoints()

        request_id = self.rq_counter.get()
        DAPConfigurationDoneRequest.create(request_id).send(self.socket)

    def _init_handshake3(self):
        self.state = DebuggerState.CONNECTED
        request_id = self.rq_counter.get()
        DAPLaunchRequest.create(request_id, DAPLaunchRequestArguments.create()).send(self.socket)

    def _connected(self):
        self.connected_callback()

    # PUBLIC API

    def connect(self):
        if self.state != DebuggerState.NOT_CONNECTED:
            raise RuntimeError("already connected")

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self._ip, self._port))

        self._init_handshake1()

    def disconnect(self):
        if self.state == DebuggerState.NOT_CONNECTED:
            raise RuntimeError("already disconnected")

        DAPDisconnectRequest.create(self.rq_counter.get()).send(self.socket)

    def pause(self):
        if self.state != DebuggerState.CONNECTED:
            raise RuntimeError("already connected")

        # TODO?
        DAPPauseRequest.create(self.rq_counter.get(), DAPPauseArguments.create(0)).send(self.socket)

    def get_state(self):
        return self.state

    # callbacks

    def set_connected_callback(self, callback=lambda: None):
        self.connected_callback = callback

    def set_disconnected_callback(self, callback=lambda reason, exception: None):
        self.disconnected_callback = callback

    def set_client_error_callback(self, callback=lambda error_info: None):
        self.client_error_callback = callback

    def set_pause_callback(self, callback=lambda stop_reason, reason_description, renpy_thread: None):
        self.pause_callback = callback

    # breakpoints related

    def add_breakpoint(self, breakpoint, sync=False):
        self.breakpoints.add(breakpoint)

        if sync:
            self.sync_breakpoints()

    def remove_breakpoint(self, breakpoint, sync=False):
        self.breakpoints.remove(breakpoint)
        self.removed_breakpoints.add(breakpoint)

        if sync:
            self.sync_breakpoints()

    def remove_breakpoint_from_source(self, source, sync=False):
        to_remove = set()

        for b in self.breakpoints:
            if b.source == source:
                to_remove.add(b)

        for b in to_remove:
            self.remove_breakpoint(breakpoint, sync=False)

        if sync:
            self.sync_breakpoints()

    def clear_breakpoints(self, sync=False):
        self.breakpoints = set()

        if sync:
            self.sync_breakpoints()

    def sync_breakpoints(self):
        if self.state == DebuggerState.NOT_CONNECTED:
            raise RuntimeError("not connected")

        for breakpoint_request in self._mk_breakpoints():
            breakpoint_request.send(self.socket)


class _DebuggerComponent(object):
    def is_valid(self):
        return False

    def get_debugger(self):
        """
        Returns actual top level debugger instance from nested component instances
        """
        if isinstance(self.debugger, RenpyDebugger):
            return self.debugger
        else:
            return self.debugger.get_debugger()


class RenpyExecutionState(_DebuggerComponent):
    """
    Denotes paused renpy execution state.

    Is valid until next time execution is run.
    """
    # TODO: work around real multithreading debugging both in renpy and here, so far it can't be done because renpy doesn't support it
    # so w/e
    def __init__(self, debugger):
        self.debugger = debugger
        self.threads = {}

    def is_valid(self):
        return self in self.debugger.current_states

    def _get_threads(self):
        return list(self.threads.values())

    @_wait_cycle(_get_threads)
    def get_threads(self):
        request_id = self.debugger.rq_counter.get()

        request = DAPThreadsRequest.create(request_id)
        self.debugger._send_request(self, request, request_id)
        return request_id

    def _load_threads(self, rb):
        self.threads = {}
        for thread_id in rb.get_threads():
            self.threads[thread_id] = RenpyThread(self, thread_id)


class RenpyThread(_DebuggerComponent):
    """
    Denotes paused renpy thread

    Also contains thread components
    """

    def __init__(self, execution_state, thread):
        self.debugger = execution_state.get_debugger()
        self.execution_state = execution_state
        self.thread_id = thread.get_id()
        self.name = thread.get_name()

        self.stack_trace = None
        self.active_frame = None

    def get_thread_id(self):
        return self.thread_id

    def get_thread_name(self):
        return self.name

    def is_valid(self):
        return self.execution_state.is_valid() and self.debugger.get_state() == DebuggerState.EXECUTION_PAUSED

    def _get_stack_frames(self):
        return self.stack_trace

    @_wait_cycle(_get_stack_frames)
    def get_stack_frames(self):
        request_id = self.debugger.rq_counter.get()

        request = DAPStackTraceRequest.create(request_id, DAPStackTraceArguments.create(self.thread_id))
        self.debugger._send_request(self, request, request_id)
        return request_id

    def _load_stack_traces(self, rb):
        self.stack_trace = []
        for stack_frame in rb.get_stack_frames():
            self.stack_trace.append(StackFrame(self, stack_frame))

    def _set_active_frame(self, frame):
        if self.active_frame is not None:
            self.active_frame._clear()
        self.active_frame = frame

    def continue_execution(self):
        self.debugger._continue_with_the_execution()
        DAPContinueRequest.create(self.debugger.rq_counter.get(), DAPContinueArguments.create(self.thread_id)).send(self.debugger.socket)

    def step(self):
        self.debugger._continue_with_the_execution()
        DAPNextRequest.create(self.debugger.rq_counter.get(), DAPNextArguments.create(self.thread_id)).send(self.debugger.socket)

    def step_in(self):
        self.debugger._continue_with_the_execution()
        DAPStepInRequest.create(self.debugger.rq_counter.get(), DAPStepInArguments.create(self.thread_id)).send(self.debugger.socket)

    def step_out(self):
        self.debugger._continue_with_the_execution()
        DAPStepOutRequest.create(self.debugger.rq_counter.get(), DAPStepOutArguments.create(self.thread_id)).send(self.debugger.socket)


class StackFrame(_DebuggerComponent):
    """
    Denotes single stack frame of execution.

    It must be set to active to read it's content.
    """
    def __init__(self, rpy_thread, stack_frame):
        self.debugger = rpy_thread.get_debugger()
        self.rpy_thread = rpy_thread
        self.stack_frame = stack_frame
        self.scopes = None

    def _clear(self):
        self.scopes = None

    def is_valid(self):
        return self.rpy_thread.is_valid() and self.rpy_thread.active_frame == self

    def get_line_of_code(self):
        return self.stack_frame.get_name()

    def get_source(self):
        source = None

        if self.stack_frame.has_source():
            source = self.stack_frame.get_source().get_path_or_default()

        return source

    def get_line(self):
        return self.stack_frame.get_line()

    def set_active(self):
        self.rpy_thread._set_active_frame(self)

    def _get_scopes(self):
        return self.scopes

    @_wait_cycle(_get_scopes)
    def get_scopes(self):
        request_id = self.debugger.rq_counter.get()

        request = DAPScopesRequest.create(request_id,
                                          DAPScopesArguments.create(self.stack_frame.get_id()))
        self.debugger._send_request(self, request, request_id)
        return request_id

    def _load_scopes(self, rb):
        self.scopes = []
        for scope in rb.get_scopes():
            self.scopes.append(VariableContainer(self, scope.get_name(), "<Scope>",
                                                 "<Scope>", scope.get_variables_reference(),
                                                 scope.get_indexed_variables_or_default([]),
                                                 scope.get_named_variables_or_default([])))


class VariableContainer(_DebuggerComponent):
    """
    Contains either scope contents or contents of an expanded variable.
    """
    def __init__(self, parent, name, value, type, var_ref, indexed, named, eval_name=None):
        self.debugger = parent.get_debugger()
        self.parent = parent
        self.name = name
        self.value = value
        self.type = type
        self.var_ref = var_ref
        self.indexed = indexed
        self.named = named
        self.eval_name = eval_name
        self.variables = None

    def is_valid(self):
        return self.parent.is_valid()

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def get_type(self):
        return self.type

    def _get_components(self):
        return self.variables

    @_wait_cycle(_get_components)
    def get_components(self):
        request_id = self.debugger.rq_counter.get()

        request = DAPVariablesRequest.create(request_id, DAPVariablesArguments.create(self.var_ref))
        self.debugger._send_request(self, request, request_id)
        return request_id

    def _load_variables(self, rb):
        self.variables = OrderedDict()

        for vb in rb.get_variables():
            name = vb.get_name()
            self.variables[name] = VariableContainer(self, name, vb.get_value(),
                                                     vb.get_type_or_default("<unknown>"),
                                                     vb.get_variables_reference(),
                                                     vb.get_indexed_variables_or_default([]),
                                                     vb.get_named_variables_or_default([]))


class _MessageState(object):
    def __init__(self, lock, req_id, waiter):
        self._lock = lock

        self.req_id = req_id
        self.callback = None
        self.ready = False
        self.waiter = waiter

    def set_callback(self, callback):
        ready = False
        with self._lock:
            self.callback = callback
            ready = self.ready

        if ready:
            self.callback()

    def set_ready(self):
        has_callback = False
        with self._lock:
            self.ready = True
            has_callback = self.callback is not None

        if has_callback:
            self.callback()
