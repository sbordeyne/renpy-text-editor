# py23 compatible
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import

from .base import __all__ as base_all
from .gen import __all__ as gen_all

from .base import *
from .gen import *
from ..utils import _fix_all

__all__ = _fix_all(["features"] + base_all + gen_all)

# enabled features
features = {
    "supports_exception_info_request": False,
    "support_terminate_debuggee": False,
    "supports_terminate_threads_request": False,
    "supports_data_breakpoints": False,
    "supports_step_in_targets_request": False,
    "supports_set_expression": False,
    "supports_goto_targets_request": False,
    "supports_function_breakpoints": False,

    # TODO
    "supports_conditional_breakpoints": False,
    "supports_hit_conditional_breakpoints": False,
}
