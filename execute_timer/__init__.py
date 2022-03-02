import time as timer

class execute_for():
    def __init__(self, duration=1):
        if (isinstance(duration, (int, float))):
            self.duration = duration
        else:
            self.duration = 1
        
    def __enter__(self):
        self.expiry = timer.perf_counter() + self.duration
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        _sleep_for = self.expiry - timer.perf_counter()
        if (_sleep_for>0):
            timer.sleep(_sleep_for)

class execute_timer():
    def __init__(self,
                 report="Operation completed in {:.6f}s.",
                 echo=False,
                ):
        self.report = report
        self.echo = echo
        
    @classmethod
    def start(cls,
              report="Operation completed in {:.6f}s.",
              echo=False,
             ):
        _obj =  cls(report=report,
                    echo=echo,
                   )
        _obj.reset()
        return _obj
        
    def reset(self):
        self.start_time = timer.perf_counter()
        self.end_time = None
        
    def lapsed(self):
        if (self.end_time is not None):
            return self.end_time - self.start_time
        else:
            return timer.perf_counter() - self.start_time
        
    def __enter__(self):
        self.reset()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = timer.perf_counter()
        if (self.echo):
            print (self.report.format(self.lapsed()))


def function_timer(
    report="Operation completed in {:.6f}s with arguments: ",
):
    def decorator(func):
        def wrapper(*args, **kwargs):
            appended_report = report
            with execute_timer(report=appended_report, echo=True):
                _return = func(*args, **kwargs)

            return _return

        return wrapper
    
    return decorator
