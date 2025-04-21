from tkinter import *
from tkinter import messagebox
import base64

def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

def save_and_encrypt_notes():
    title = title_entry.get()
    message = input_text.get("1.0",END)
    master_secret = master_secret_input.get()

    if len(title.strip()) == 0 or len(message.strip()) == 0 or len(master_secret.strip()) == 0:
            messagebox.showinfo(title="Error!", message="Please enter all information.")
    else:
        message_encrypted = encode(master_secret, message)

        try:
            with open("mysecret.txt", "a") as data_file:
                data_file.write(f'\n{title}\n{message_encrypted}')
        except FileNotFoundError:
            with open("mysecret.txt", "w") as data_file:
                data_file.write(f'\n{title}\n{message_encrypted}')
        finally:
            title_entry.delete(0, END)
            master_secret_input.delete(0, END)
            input_text.delete("1.0",END)

def decrypt_notes():
    message_encrypted = input_text.get("1.0", END)
    master_secret = master_secret_input.get()

    if len(message_encrypted.strip()) == 0 or len(master_secret.strip()) == 0:
        messagebox.showinfo(title="Error!", message="Please enter all information.")
    else:
        try:
            decrypted_message = decode(master_secret,message_encrypted)
            input_text.delete("1.0", END)
            input_text.insert("1.0", decrypted_message)
        except:
            messagebox.showinfo(title="Error!", message="Please make sure of encrypted info.")

window = Tk()
window.title("Secret Notes")
window.config(padx=30, pady=30)

image = PhotoImage(file="top_secret.png")
image = image.subsample(4,4)

image_label = Label(window, image=image)
image_label.pack(pady=15)

title_info_label = Label(text="Enter your title",font=("Verdena",12,"bold"))
title_info_label.pack(pady=1)

title_entry = Entry(width=54)
title_entry.pack(pady=1)

input_info_label = Label(text="Enter your secret",font=("Verdena",12,"bold"))
input_info_label.pack(pady=1)

input_text = Text(width=40, height=15)
input_text.pack(pady=1)

master_secret_label = Label(text="Enter master key",font=("Verdena",12,"bold"))
master_secret_label.pack(pady=1)

master_secret_input = Entry(width=54)
master_secret_input.pack(pady=1)

save_button = Button(text="Save & Encrypt", font=("Verdena",8,"bold"),command=save_and_encrypt_notes)
save_button.pack(pady=1)

decrypt_button = Button(text="Decrypt", font=("Verdena",8,"bold"),command=decrypt_notes)
decrypt_button.pack()
window.mainloop()