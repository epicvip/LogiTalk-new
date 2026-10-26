from customtkinter import *
from socket import *
import threading


HOST = "7.tcp.eu.ngrok.io"
PORT = 22318

client_socket = socket(AF_INET, SOCK_STREAM)
is_connected = False

try:
    client_socket.connect((HOST, PORT))
    print("Успішно приєднався до сервера!")
    is_connected = True
except:
    print("Не змогли приєднатися")

my_username = "Гість"

def add_message (message_text, align="right"):
    msg_label = CTkLabel(chat, 
                        text=message_text, 
                        corner_radius=8, 
                        fg_color="blue" if align == "right" else "#333333"
)

    anchor = "e" if align == "right" else "w"
    msg_label.pack(anchor=anchor, pady=5, padx=10)
    chat._parent_canvas.yview_moveto(1.0)


def send_message(event=None):
    if is_connected == False:
        return

    message = message_input.get()
        
    if message.strip():
        add_message(f"Ви: {message}", align="right")

        full_message = f"{my_username}: {message}"

        client_socket.sendall(full_message.encode())
        message_input.delete(0, "end")

def receive_messages ():
    while is_connected:
        try:
            message = client_socket.recv(4096)
            if not message:
                break
            message = message.decode()

            window.after(0, lambda m=message: add_message(m, align="left"))
        except:
            print("З'єднання з сервером розірвано")   
            break 

window = CTk()
window.geometry("400x350")
window.title("LogiTalk")

window.menu_visible = False

def showLeftSideMenu():
    if window.menu_visible == True:
        sidebar_frame.pack_forget()
        window.menu_visible = False
        btn_menu.configure(text="▶")
    else:
        sidebar_frame.pack(side="left", fill="y", before=main_frame)
        window.menu_visible = True
        btn_menu.configure(text="◀")

sidebar_frame = CTkFrame(window, width=150, corner_radius=0)
sidebar_frame.pack_propagate(False)

# menu_title = CTkLabel(sidebar_frame, text="Меню", font=("Arial", 20))
# menu_title.pack(pady=20)

name_label = CTkLabel(sidebar_frame, text=my_username, font=("Arial", 16))
name_label.pack(pady=5)

new_name_entry = CTkEntry(sidebar_frame, placeholder_text="Введіть ім'я...")
new_name_entry.pack(pady=5)

def change_username ():
    global my_username
    new_name = new_name_entry.get()
    if new_name.strip():
        my_username = new_name
        name_label.configure(text=new_name)
        new_name_entry.delete(0, "end")


btn_saveName = CTkButton(sidebar_frame, text="Зберегти ім'я", command=change_username)
btn_saveName.pack(pady=(0, 40), padx=20)

def changeTheme():
    theme = get_appearance_mode()
    if theme == "Dark":
        set_appearance_mode("Light")
    else:
        set_appearance_mode("Dark")

btn_changeTheme = CTkButton(sidebar_frame, text="Змінити тему", command=changeTheme)
btn_changeTheme.pack(pady=10, padx=10)

main_frame = CTkFrame(window, fg_color="transparent")
main_frame.pack(side="left", fill="both", expand=True)

top_frame= CTkFrame(main_frame, fg_color="transparent")
top_frame.pack(side="top", fill="x", padx=10, pady=10)

btn_menu = CTkButton(top_frame, width=30, text="▶", command=showLeftSideMenu)
btn_menu.pack(side="left")

chat = CTkScrollableFrame(main_frame)
chat.pack(fill="both", expand=True, padx=10, pady=10)


bottom_frame = CTkFrame(main_frame, fg_color="transparent", )
bottom_frame.pack(side="bottom", fill="x",  padx=5, pady=10)


message_input = CTkEntry(bottom_frame, placeholder_text="Введіть повідомлення..." )
message_input.pack(side="left", fill="x", expand=True, padx=5)

message_input.bind("<Return>", send_message)

sendmessage = CTkButton(bottom_frame, text="Надіслати", width=80, command=send_message)
sendmessage.pack(side="right")


if is_connected:
    receive_thread = threading.Thread(target=receive_messages, daemon = True)
    receive_thread.start()


window.mainloop()

