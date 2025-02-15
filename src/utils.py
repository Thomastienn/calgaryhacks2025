# Reusable helper functions go here
import time

def ease_in_out(t, stretch=1, translate=0):
    return (t*t*(3-2*t) * stretch) + translate

def tk_translate(ctk_object, relx_i, relx_f, rely_i, rely_f, duration, start_time=None):
    if start_time is None:
        start_time = time.perf_counter()
    current_time = time.perf_counter()
    elapsed = (current_time-start_time)/duration
    if elapsed > 1:
        elapsed = 1
    move_amountx = ease_in_out(elapsed, relx_f-relx_i, relx_i)/duration
    move_amounty = ease_in_out(elapsed, rely_f-rely_i, rely_i)/duration
    
    
    ctk_object.place(relx=move_amountx, rely=move_amounty)
    
    if elapsed < 1:
        ctk_object.after(5, tk_translate, ctk_object, relx_i, relx_f, rely_i, rely_f, duration, start_time)
        
def tk_grow(ctk_object, duration, start_time=None, starting_width=None, starting_height=None):
    if start_time is None:
        start_time = time.perf_counter()
        starting_width = ctk_object.winfo_width()/2
        starting_height = ctk_object.winfo_height()/2
    current_time = time.perf_counter()
    elapsed = (current_time - start_time) / duration
    if elapsed > 1:
        elapsed = 1
    grow_amount = ease_in_out(elapsed)/4
    
    ctk_object.configure(width=starting_width+starting_width*grow_amount, height=starting_height+starting_height*grow_amount)
    
    if elapsed < 1:
        ctk_object.after(10, tk_grow, ctk_object, duration, start_time, starting_width, starting_height)

def tk_shrink(ctk_object, duration, start_time=None, starting_width=None, starting_height=None):
    if start_time is None:
        start_time = time.perf_counter()
        starting_width = ctk_object.winfo_width()/2
        starting_height = ctk_object.winfo_height()/2
    current_time = time.perf_counter()
    elapsed = (current_time - start_time) / duration
    if elapsed > 1.2397:
        elapsed = 1.2397
    grow_amount = -1*ease_in_out(elapsed)/4
    print(grow_amount)
    ctk_object.configure(width=starting_width+starting_width*grow_amount, height=starting_height+starting_height*grow_amount)
    if elapsed < 1.2397:
        ctk_object.after(10, tk_shrink, ctk_object, duration, start_time, starting_width, starting_height)