from time import sleep

def fill_progress_bar(widget, total_iterations):
    widget.lock_buttons()
    percentage_total = 100 // total_iterations
    percentage_total_rest = 100 % total_iterations
    current_progress = 0
    for i in range(total_iterations):
        current_progress += percentage_total
        sleep(0.02)
        widget.progressBar.setValue(current_progress)
    
    current_progress += percentage_total_rest
    widget.progressBar.setValue(current_progress)

    if current_progress == 100:
        # Here we should call a success dialog box function;
        # A function that receives the operation and the message would 
        # work fine;
        pass