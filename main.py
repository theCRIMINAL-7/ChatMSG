import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pyrebase
from datetime import datetime
import threading
import json
from firebase_config import FIREBASE_CONFIG, initialize_firebase

class ChatMSG:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ChatMSG")
        self.root.geometry("1000x700")
        
        # Color scheme
        self.colors = {
            'primary': '#6C63FF',      # Main theme color
            'secondary': '#4CAF50',    # Accent color
            'background': '#F5F6FA',   # Background color
            'text': '#6C63FF',         # Text color
            'light_text': '#636E72',   # Secondary text color
            'white': '#FFFFFF',        # White
            'error': '#FF6B6B',        # Error color
            'success': '#00B894',      # Success color
            'chat_bg': '#E8EAF6',      # Chat background
            'sent_msg': '#6C63FF',     # Sent message color
            'received_msg': '#FFFFFF', # Received message color
            'button_text': '#6C63FF'   # Button text color
        }
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TFrame', background=self.colors['background'])
        self.style.configure('TLabel', background=self.colors['background'], foreground=self.colors['text'])
        
        # Configure button styles
        self.style.configure('TButton', 
                           background=self.colors['primary'],
                           foreground=self.colors['button_text'],
                           font=('Helvetica', 12, 'bold'),
                           padding=10)
        self.style.map('TButton',
                      background=[('active', self.colors['secondary'])],
                      foreground=[('active', self.colors['button_text'])])
        
        # Configure link button style
        self.style.configure('Link.TButton',
                           background=self.colors['background'],
                           foreground=self.colors['primary'],
                           font=('Helvetica', 12, 'bold'),
                           padding=5)
        self.style.map('Link.TButton',
                      background=[('active', self.colors['background'])],
                      foreground=[('active', self.colors['secondary'])])
        
        # Initialize Firebase
        self.firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()
        
        # Initialize Firebase Admin SDK
        initialize_firebase()
        
        # Current user data
        self.current_user = None
        self.current_username = None
        
        # Start with login screen
        self.show_login_screen()
        
    def show_login_screen(self):
        """Display the login screen"""
        self.clear_window()
        
        # Create main container
        main_container = ttk.Frame(self.root, padding="40")
        main_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # App title
        title_label = ttk.Label(main_container, 
                              text="ChatMSG",
                              font=('Helvetica', 24, 'bold'),
                              foreground=self.colors['primary'])
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # Login frame
        login_frame = ttk.Frame(main_container, padding="20", style='Card.TFrame')
        login_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10)
        
        # Email
        ttk.Label(login_frame, 
                 text="Email",
                 font=('Helvetica', 12)).grid(row=0, column=0, pady=(0, 5), sticky='w')
        self.email_entry = ttk.Entry(login_frame, width=30, font=('Helvetica', 12))
        self.email_entry.grid(row=1, column=0, pady=(0, 15))
        
        # Password
        ttk.Label(login_frame,
                 text="Password",
                 font=('Helvetica', 12)).grid(row=2, column=0, pady=(0, 5), sticky='w')
        self.password_entry = ttk.Entry(login_frame, width=30, show="*", font=('Helvetica', 12))
        self.password_entry.grid(row=3, column=0, pady=(0, 20))
        
        # Login button
        login_btn = ttk.Button(login_frame,
                             text="Login",
                             command=self.login,
                             style='TButton',
                             width=20)
        login_btn.grid(row=4, column=0, pady=(0, 10))
        
        # Signup link
        signup_btn = ttk.Button(login_frame,
                              text="Create Account",
                              command=self.show_signup_screen,
                              style='Link.TButton',
                              width=20)
        signup_btn.grid(row=5, column=0)
        
    def show_signup_screen(self):
        """Display the signup screen"""
        self.clear_window()
        
        # Create main container
        main_container = ttk.Frame(self.root, padding="40")
        main_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # App title
        title_label = ttk.Label(main_container,
                              text="Create Account",
                              font=('Helvetica', 24, 'bold'),
                              foreground=self.colors['primary'])
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # Signup frame
        signup_frame = ttk.Frame(main_container, padding="20", style='Card.TFrame')
        signup_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10)
        
        # Username
        ttk.Label(signup_frame,
                 text="Username",
                 font=('Helvetica', 12)).grid(row=0, column=0, pady=(0, 5), sticky='w')
        self.username_entry = ttk.Entry(signup_frame, width=30, font=('Helvetica', 12))
        self.username_entry.grid(row=1, column=0, pady=(0, 15))
        
        # Email
        ttk.Label(signup_frame,
                 text="Email",
                 font=('Helvetica', 12)).grid(row=2, column=0, pady=(0, 5), sticky='w')
        self.signup_email_entry = ttk.Entry(signup_frame, width=30, font=('Helvetica', 12))
        self.signup_email_entry.grid(row=3, column=0, pady=(0, 15))
        
        # Password
        ttk.Label(signup_frame,
                 text="Password",
                 font=('Helvetica', 12)).grid(row=4, column=0, pady=(0, 5), sticky='w')
        self.signup_password_entry = ttk.Entry(signup_frame, width=30, show="*", font=('Helvetica', 12))
        self.signup_password_entry.grid(row=5, column=0, pady=(0, 20))
        
        # Signup button
        signup_btn = ttk.Button(signup_frame,
                              text="Sign Up",
                              command=self.signup,
                              style='TButton',
                              width=20)
        signup_btn.grid(row=6, column=0, pady=(0, 10))
        
        # Back to login
        back_btn = ttk.Button(signup_frame,
                            text="Back to Login",
                            command=self.show_login_screen,
                            style='Link.TButton',
                            width=20)
        back_btn.grid(row=7, column=0)
        
    def show_contacts_screen(self):
        """Display the contacts screen"""
        self.clear_window()
        
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame, style='Header.TFrame')
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        # User info
        user_frame = ttk.Frame(header_frame)
        user_frame.pack(side=tk.LEFT, padx=20, pady=10)
        
        ttk.Label(user_frame,
                 text=f"Welcome, {self.current_username}",
                 font=('Helvetica', 14, 'bold'),
                 foreground=self.colors['primary']).pack(side=tk.LEFT)
        
        # Logout button
        logout_btn = ttk.Button(header_frame,
                              text="Logout",
                              command=self.logout,
                              style='TButton')
        logout_btn.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Contacts list frame
        contacts_frame = ttk.Frame(main_frame, width=300, style='Contacts.TFrame')
        contacts_frame.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        
        # Add contact button
        add_contact_btn = ttk.Button(contacts_frame,
                                   text="➕ Add Contact",
                                   command=self.show_add_contact_dialog,
                                   style='TButton')
        add_contact_btn.pack(fill=tk.X, padx=10, pady=10)
        
        # Contacts list
        self.contacts_listbox = tk.Listbox(contacts_frame,
                                         font=('Helvetica', 12),
                                         bg=self.colors['white'],
                                         fg=self.colors['text'],
                                         selectbackground=self.colors['primary'],
                                         selectforeground=self.colors['white'],
                                         borderwidth=0,
                                         highlightthickness=0)
        self.contacts_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.contacts_listbox.bind('<<ListboxSelect>>', self.on_contact_select)
        
        # Chat frame
        self.chat_frame = ttk.Frame(main_frame, style='Chat.TFrame')
        self.chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Load contacts
        self.load_contacts()
        
    def show_chat_window(self, contact_username):
        """Display chat window for selected contact"""
        # Clear chat frame
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
            
        # Chat header
        header_frame = ttk.Frame(self.chat_frame, style='ChatHeader.TFrame')
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(header_frame,
                 text=contact_username,
                 font=('Helvetica', 14, 'bold'),
                 foreground=self.colors['primary']).pack(side=tk.LEFT)
        
        # Chat messages area
        self.messages_area = scrolledtext.ScrolledText(self.chat_frame,
                                                     wrap=tk.WORD,
                                                     font=('Helvetica', 12),
                                                     bg=self.colors['chat_bg'],
                                                     fg=self.colors['text'],
                                                     borderwidth=0,
                                                     highlightthickness=0)
        self.messages_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        # Message input area
        input_frame = ttk.Frame(self.chat_frame, style='Input.TFrame')
        input_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.message_entry = ttk.Entry(input_frame,
                                     font=('Helvetica', 12),
                                     width=50)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        send_button = ttk.Button(input_frame,
                               text="Send",
                               command=lambda: self.send_message(contact_username),
                               style='TButton')
        send_button.pack(side=tk.RIGHT)
        
        # Load chat history
        self.load_chat_history(contact_username)
        
        # Start listening for new messages
        self.start_message_listener(contact_username)
        
    def login(self):
        """Handle user login"""
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        try:
            # Authenticate with Firebase
            user = self.auth.sign_in_with_email_and_password(email, password)
            
            # Get user data from database
            user_data = self.db.child("users").child(user['localId']).get().val()
            
            if user_data:
                self.current_user = user
                self.current_username = user_data['username']
                messagebox.showinfo("Success", "Login successful!")
                self.show_contacts_screen()
            else:
                messagebox.showerror("Error", "User data not found")
                
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {str(e)}")
            
    def signup(self):
        """Handle user signup"""
        username = self.username_entry.get()
        email = self.signup_email_entry.get()
        password = self.signup_password_entry.get()
        
        try:
            # Check if username exists
            users = self.db.child("users").get().val()
            if users:
                for user_id, user_data in users.items():
                    if user_data.get('username') == username:
                        messagebox.showerror("Error", "Username already taken")
                        return
            
            # Create user in Firebase Auth
            user = self.auth.create_user_with_email_and_password(email, password)
            
            # Store user data in database
            user_data = {
                "username": username,
                "email": email,
                "contacts": []
            }
            self.db.child("users").child(user['localId']).set(user_data)
            
            messagebox.showinfo("Success", "Signup successful!")
            self.show_login_screen()
            
        except Exception as e:
            messagebox.showerror("Error", f"Signup failed: {str(e)}")
            
    def load_contacts(self):
        """Load user's contacts from database"""
        try:
            user_data = self.db.child("users").child(self.current_user['localId']).get().val()
            if user_data and 'contacts' in user_data:
                self.contacts_listbox.delete(0, tk.END)
                for contact in user_data['contacts']:
                    self.contacts_listbox.insert(tk.END, contact)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load contacts: {str(e)}")
            
    def show_add_contact_dialog(self):
        """Show dialog to add a new contact"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Contact")
        dialog.geometry("400x200")
        dialog.configure(bg=self.colors['background'])
        
        # Center the dialog
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Content frame
        content_frame = ttk.Frame(dialog, padding="20", style='Card.TFrame')
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(content_frame,
                 text="Enter username:",
                 font=('Helvetica', 12)).pack(pady=(0, 10))
        
        username_entry = ttk.Entry(content_frame,
                                 font=('Helvetica', 12),
                                 width=30)
        username_entry.pack(pady=(0, 20))
        
        def add_contact():
            username = username_entry.get()
            try:
                # Check if user exists
                users = self.db.child("users").get().val()
                user_found = False
                for user_id, user_data in users.items():
                    if user_data.get('username') == username:
                        user_found = True
                        # Add to contacts
                        current_contacts = self.db.child("users").child(self.current_user['localId']).child("contacts").get().val() or []
                        if username not in current_contacts:
                            current_contacts.append(username)
                            self.db.child("users").child(self.current_user['localId']).child("contacts").set(current_contacts)
                            messagebox.showinfo("Success", f"Added {username} to contacts")
                            self.load_contacts()
                        else:
                            messagebox.showinfo("Info", "Contact already added")
                        break
                
                if not user_found:
                    messagebox.showerror("Error", "User not found")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add contact: {str(e)}")
            
            dialog.destroy()
            
        ttk.Button(content_frame,
                  text="Add",
                  command=add_contact,
                  style='TButton',
                  width=20).pack(pady=10)
        
    def on_contact_select(self, event):
        """Handle contact selection"""
        selection = self.contacts_listbox.curselection()
        if selection:
            contact_username = self.contacts_listbox.get(selection[0])
            self.show_chat_window(contact_username)
            
    def send_message(self, receiver_username):
        """Send message to selected contact"""
        message = self.message_entry.get()
        if not message.strip():
            return
            
        try:
            # Get receiver's user ID
            users = self.db.child("users").get().val()
            receiver_id = None
            for user_id, user_data in users.items():
                if user_data.get('username') == receiver_username:
                    receiver_id = user_id
                    break
                    
            if receiver_id:
                # Create message data
                message_data = {
                    "sender": self.current_username,
                    "receiver": receiver_username,
                    "message": message,
                    "timestamp": datetime.now().isoformat()
                }
                
                # Store message in database
                self.db.child("messages").push(message_data)
                
                # Clear message entry
                self.message_entry.delete(0, tk.END)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {str(e)}")
            
    def load_chat_history(self, contact_username):
        """Load chat history with selected contact"""
        try:
            messages = self.db.child("messages").get().val()
            if messages:
                self.messages_area.delete(1.0, tk.END)
                for message_id, message in messages.items():
                    if (message['sender'] == self.current_username and message['receiver'] == contact_username) or \
                       (message['sender'] == contact_username and message['receiver'] == self.current_username):
                        if message['sender'] == self.current_username:
                            self.messages_area.insert(tk.END, f"{message['message']}\n", "sent")
                        else:
                            self.messages_area.insert(tk.END, f"{message['message']}\n", "received")
                            
                # Configure tags for message alignment and colors
                self.messages_area.tag_configure("sent", 
                                               justify="right",
                                               background=self.colors['sent_msg'],
                                               foreground=self.colors['white'],
                                               spacing1=10,
                                               spacing3=10,
                                               lmargin1=100,
                                               lmargin2=100,
                                               rmargin=20,
                                               relief="flat",
                                               borderwidth=0)
                self.messages_area.tag_configure("received",
                                               justify="left",
                                               background=self.colors['received_msg'],
                                               foreground=self.colors['text'],
                                               spacing1=10,
                                               spacing3=10,
                                               lmargin1=20,
                                               lmargin2=20,
                                               rmargin=100,
                                               relief="flat",
                                               borderwidth=0)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load chat history: {str(e)}")
            
    def start_message_listener(self, contact_username):
        """Start listening for new messages"""
        def message_stream_handler(message):
            if message["event"] == "put":
                message_data = message["data"]
                if message_data:
                    # Handle both single message and multiple messages
                    if isinstance(message_data, dict):
                        messages = [message_data]
                    else:
                        messages = message_data.values()
                        
                    for msg in messages:
                        if isinstance(msg, dict) and 'sender' in msg and 'receiver' in msg:
                            if (msg['sender'] == self.current_username and msg['receiver'] == contact_username) or \
                               (msg['sender'] == contact_username and msg['receiver'] == self.current_username):
                                if msg['sender'] == self.current_username:
                                    self.messages_area.insert(tk.END, f"{msg['message']}\n", "sent")
                                else:
                                    self.messages_area.insert(tk.END, f"{msg['message']}\n", "received")
                                self.messages_area.see(tk.END)
        
        # Start streaming messages
        self.db.child("messages").stream(message_stream_handler)
        
    def logout(self):
        """Handle user logout"""
        try:
            # Clear current user data
            self.current_user = None
            self.current_username = None
            
            # Show login screen
            self.show_login_screen()
            
            messagebox.showinfo("Success", "Logged out successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Logout failed: {str(e)}")
            
    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ChatMSG()
    app.run() 