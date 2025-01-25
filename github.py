import tkinter as tk
from tkinter import ttk
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="YOUR API KEY")
model = genai.GenerativeModel("YOUR SELECTED GEMININI MODEL")


def fetch_ai_response(prompt):
    """Send the prompt to Gemini and get a concise response."""
    try:
        prompt = f"Provide a concise and clear response to the following:\n\n{prompt}\n\nAnswer concisely."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error fetching response: {e}"


def fetch_ai_response_for_clipboard():
    """Fetch AI response for clipboard content directly."""
    global last_clipboard_content
    try:
        clipboard_content = root.clipboard_get()
    except tk.TclError:
        clipboard_content = ""  # Handle empty or inaccessible clipboard

    if clipboard_content and clipboard_content != last_clipboard_content:
        last_clipboard_content = clipboard_content
        ai_response = fetch_ai_response(clipboard_content.strip())
        ai_response_text.delete(1.0, tk.END)
        ai_response_text.insert(tk.END, ai_response)


def fetch_ai_response_for_custom_message(event=None):
    """Fetch AI response when Enter key is pressed for a custom message."""
    try:
        clipboard_content = root.clipboard_get()
    except tk.TclError:
        clipboard_content = ""

    custom_message = custom_message_entry.get().strip()
    combined_prompt = clipboard_content.strip()
    if custom_message:
        combined_prompt += f"\n\n{custom_message}"

    if combined_prompt:
        ai_response = fetch_ai_response(combined_prompt)
        ai_response_text.delete(1.0, tk.END)
        ai_response_text.insert(tk.END, ai_response)


def update_clipboard_monitoring():
    """Monitor clipboard content and fetch AI response if needed."""
    fetch_ai_response_for_clipboard()
    root.after(1500, update_clipboard_monitoring)


def copy_ai_response_to_clipboard():
    """Copy the AI response to the clipboard."""
    response = ai_response_text.get("1.0", tk.END).strip()
    if response:
        root.clipboard_clear()
        root.clipboard_append(response)
        root.update()
        copy_label.config(text="Response copied to clipboard!", foreground="green")
    else:
        copy_label.config(text="No response to copy!", foreground="red")


# Initialize the last clipboard content variable
last_clipboard_content = ""

# Create the main Tkinter window
root = tk.Tk()
root.title("Screen Solver")
root.geometry("900x600")
root.resizable(True, True)

# Style Configuration
style = ttk.Style()
style.configure("TFrame", background="#1e1e1e")
style.configure("TLabel", font=("Arial", 12), background="#1e1e1e", foreground="#FFFFFF")
style.configure("TButton", font=("Arial", 12), background="#4CAF50", foreground="#FFFFFF")
style.configure("TLabelFrame", background="#1e1e1e", foreground="#FFD700")

# Root Configuration
root.configure(bg="#1e1e1e")

# Title Section
title_label = ttk.Label(root, text="ScreenAI", font=("Arial", 20, "bold"), foreground="#FFD700", background="#1e1e1e")
title_label.pack(pady=15)

# Custom Message Section
custom_message_frame = ttk.Frame(root, padding=10)
custom_message_frame.pack(pady=10)

custom_message_label = ttk.Label(custom_message_frame, text="Custom Message:")
custom_message_label.grid(row=0, column=0, padx=5, pady=5, sticky="W")

custom_message_entry = tk.Entry(custom_message_frame, width=60, font=("Arial", 12), bg="#333333", fg="#00FF00", insertbackground="#FFD700", relief="solid")
custom_message_entry.grid(row=0, column=1, padx=5, pady=5)

# AI Response Section
ai_response_frame = ttk.LabelFrame(root, text="AI Response", padding=(10, 5))
ai_response_frame.pack(pady=20, fill="both", expand=True)

ai_response_text = tk.Text(ai_response_frame, wrap=tk.WORD, height=12, font=("Arial", 12), bg="#333333", fg="#39FF14", insertbackground="#FFD700", padx=10, pady=10, relief="solid")
ai_response_text.pack(fill="both", expand=True)

# Copy Button
copy_button = ttk.Button(root, text="Copy AI Response", command=copy_ai_response_to_clipboard, style="TButton")
copy_button.pack(pady=10)

copy_label = ttk.Label(root, text="", font=("Arial", 10), background="#1e1e1e", foreground="#FFD700")
copy_label.pack()

# Bind Enter Key
custom_message_entry.bind('<Return>', fetch_ai_response_for_custom_message)

# Start Clipboard Monitoring
update_clipboard_monitoring()

# Run Tkinter Main Loop
root.mainloop()
