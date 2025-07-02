def clear_main_frame(main_frame):
    """Clear the main frame"""
    if main_frame is None:
        return

    for widget in main_frame.winfo_children():
        widget.destroy()
