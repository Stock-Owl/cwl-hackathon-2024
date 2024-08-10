import tkinter as tk
from PIL import ImageTk, Image
import os

# creates window and canvas
root = tk.Tk().
root.title("Peter Alert")
canvas = tk.Canvas(root, width=200, height=193)

# puts text above peter
label = tk.Label(root, text="Peter Alert", font=("Arial", 12), width=20)
label.pack()

#puts image on canvas
peter = ImageTk.PhotoImage(Image.open("./p_alert/peter_smol.jpg"))
canvas.create_image(0, 0, anchor="nw", image=peter)
canvas.pack()

# puts 'OK' button in the window
button = tk.Button(root, 
                   text="OK",
                   command=root.destroy,
                   activebackground="gray", 
                   activeforeground="white",
                   anchor="center",
                   bg="lightgray",
                   cursor="hand2",
                   font=("Arial", 12),
                   width=20,
                   justify="center")
button.pack()

# root.mainloop()
input()
