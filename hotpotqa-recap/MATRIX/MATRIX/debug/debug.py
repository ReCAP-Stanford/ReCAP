import functools
import threading
import rich

 
_debug_context = threading.local()
_debug_context.indent_level = 0   

from rich.console import Console

from typing import Any, Union, Set, Callable



 
 
 

 
 

def debug(args_set: Union[Set, None]=None, kwargs_set: Union[Set, None]=None, return_op: Callable=None, param_log: bool=True):
    def _debug(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not hasattr(_debug_context, "indent_level"):
                _debug_context.indent_level = 0
            
            console = Console()
            if args_set is None:
                printed_args = args
            else:
                printed_args = [args_set[idx](val) for idx, val in enumerate(args) if idx in args_set]
            if kwargs_set is None:
                printed_kwargs = kwargs
            else:
                printed_kwargs = {key: kwargs_set[key](val) for key, val in kwargs.items() if key in kwargs_set}
            
            indent = "    " * _debug_context.indent_level
            func_name = func.__name__
            if param_log:
                args_repr = ", ".join(repr(a) for a in printed_args)
                kwargs_repr = ", ".join(f"{k}={v!r}" for k, v in printed_kwargs.items())
                params = ", ".join(filter(None, [args_repr, kwargs_repr]))

                log_entry = f"\n{indent}▶ Enter {func_name}({params})"
                # print(log_entry)
                console.print(f"[bold][green]\n{indent}▶ Enter[/green][/bold] {func_name}({params})")
            else:
                log_entry = f"\n{indent}▶ Enter {func_name}"
                console.print(f"[bold][green]\n{indent}▶ Enter[/green][/bold] [yellow]{func_name}[/yellow]")
                
            _write_log(log_entry)
            
            _debug_context.indent_level += 1

            try:
                result = func(*args, **kwargs)
            finally:
                if return_op is None:
                    printed_result = result
                else:
                    printed_result = return_op(result)
                _debug_context.indent_level -= 1
                indent = "    " * _debug_context.indent_level

                log_exit = f"{indent}◀ Exit {func_name} -> {printed_result!r}\n"
                console.print(f"[bold][red]{indent}◀ Exit[/red][/bold] [yellow]{func_name}[/yellow] -> [blue]{printed_result!r}[/blue]\n")
                _write_log(log_exit)

            return result

        return wrapper
    return _debug

def _write_log(message):
    with open("debug.txt", "a", encoding="utf-8") as f:
        f.write(message + "\n")

