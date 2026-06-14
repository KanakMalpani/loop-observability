"""Loop Trace Format (LTF) instrumentation for loop runs."""

from loopotel.tracer import LoopTracer, current_tracer, emit_iteration, trace_loop

__version__ = "0.1.0"
__all__ = ["LoopTracer", "current_tracer", "emit_iteration", "trace_loop", "__version__"]
