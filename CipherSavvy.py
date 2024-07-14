from tkinter import  *
import numpy as np

def caesar_cipher(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            base = ord('a') if char.islower() else ord('A')
            shifted = (ord(char) - base + shift) % 26 + base
            encrypted_text += chr(shifted)
        else:
            encrypted_text += char
    return encrypted_text

def playfair_key(key):
    key = ''.join(dict.fromkeys(key.upper()))
    key = key.replace('J', 'I')
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    matrix = [[0] * 5 for _ in range(5)]
    row = 0
    col = 0
    for letter in key:
        matrix[row][col] = letter
        col += 1
        if col == 5:
            col = 0
            row += 1
    for letter in alphabet:
        if letter not in key and letter != 'J':
            matrix[row][col] = letter
            col += 1
            if col == 5:
                col = 0
                row += 1
    return matrix

def find_letter_positions(matrix, letter):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == letter:
                return (i, j)

def playfair_cipher(plain_text, key):
    matrix = playfair_key(key)
    encrypted_text = ""
    plain_text = plain_text.upper().replace("J", "I")
    for i in range(0, len(plain_text), 2):
        char1 = plain_text[i]
        char2 = plain_text[i + 1] if i + 1 < len(plain_text) else 'X'
        if char1 == char2:
            char2 = 'X'
        row1, col1 = find_letter_positions(matrix, char1)
        row2, col2 = find_letter_positions(matrix, char2)
        if row1 == row2:
            encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
        else:
            encrypted_text += matrix[row1][col2] + matrix[row2][col1]
    return encrypted_text

def hill_key(key):
    key = key.upper().replace(" ", "")
    key_len = len(key)
    sqrt_len = int(key_len ** 0.5)
    if sqrt_len ** 2 != key_len:
        raise ValueError("Key length must be a perfect square")
    key_matrix = np.array([ord(char) - 65 for char in key]).reshape(sqrt_len, sqrt_len)
    return key_matrix

def hill_cipher(plain_text, key):
    plain_text = plain_text.upper().replace(" ", "")
    plain_len = len(plain_text)
    sqrt_len = key.shape[0]
    if plain_len % sqrt_len != 0:
        plain_text += "X" * (sqrt_len - (plain_len % sqrt_len))
    encrypted_text = ""
    for i in range(0, len(plain_text), sqrt_len):
        plain_vector = np.array([ord(char) - 65 for char in plain_text[i:i+sqrt_len]])
        encrypted_vector = np.dot(key, plain_vector) % 26
        encrypted_text += ''.join([chr(char + 65) for char in encrypted_vector])
    return encrypted_text

def vigenere_cipher(plain_text, key):


    encrypted_text = ""
    key_length = len(key)
    for i in range(len(plain_text)):
        char = plain_text[i]
        if char.isalpha():
            shift = ord(key[i % key_length].upper()) - 65
            encrypted_text += caesar_cipher(char, shift)
        else:
            encrypted_text += char
    return encrypted_text

def encrypt_text():
    input_text = e1.get("1.0", "end-1c")
    selected_cipher = clicked.get()
    key = e2.get()
    if selected_cipher == "Caesar Cipher":
        shift = int(key)
        encrypted_text = caesar_cipher(input_text, shift)
        des="Caesar cipher is a substitution method where each letter in the plaintext is shifted a certain number of places down or up the alphabet."
    elif selected_cipher == "Playfair Cipher":
        encrypted_text = playfair_cipher(input_text, key)
        des="Playfair cipher is a polygraphic substitution technique where pairs of letters are encrypted as blocks instead of individual letters. A 5x5 grid with a keyword is used for encryption. Repeated letters in a pair are separated by a filler like 'X'. It provides stronger encryption than simple substitution."
    elif selected_cipher == "Hill Cipher":
        key_matrix = hill_key(key)
        encrypted_text = hill_cipher(input_text, key_matrix)
        des="Hill cipher is a polygraphic substitution method employing matrices. Plaintext is broken into blocks, each represented as vectors. Multiplying these vectors by a predetermined key matrix yields ciphertext."
    else:
        encrypted_text = vigenere_cipher(input_text, key)
        des="The Vigenère cipher is a polyalphabetic substitution method using a keyword. Each letter in the plaintext is shifted according to the corresponding letter in the keyword. Repeating the keyword ensures stronger encryption."
    
    result_text.delete("1.0", "end")
    result_text.insert("1.0", encrypted_text)
    para.delete("1.0", "end")
    para.insert("1.0",des)

t=Tk()
t.geometry("400x500")
l1=Label(t,text="CIPHERSAVVY",font='arial 25 bold',bg='beige',foreground="brown")
l1.pack()
l2=Label(t,text="PLAINTEXT:",bg='beige',foreground="brown")
l2.place(x=10,y=80)
e1=Text(t,height=1, width=20,fg="brown")
e1.place(x=120,y=80)
l3=Label(t,text="KEY:",bg='beige',foreground="brown")
l3.place(x=10,y=130)
e2=Entry(t,fg="brown")
e2.place(x=120,y=130)
l4=Label(t,text="METHOD:",bg='beige',foreground="brown")
l4.place(x=10,y=180)
options = ["Playfair Cipher","Hill Cipher","Caesar Cipher","Vignere Cipher"]
clicked = StringVar(t) 
clicked.set( "Caesar Cipher") 
drop = OptionMenu( t, clicked, *options ) 
drop.config(bg="brown")
drop.place(x=120,y=180)
b1 = Button( t , text = "Encrypt" , command = encrypt_text, bg='brown' )
b1.place(x=150,y=230)
l5=Label(t, text="Encrypted Text:",bg='beige',foreground="brown")
l5.place(x=10,y=280)
result_text = Text(t, height=1, width=20,fg="brown")
result_text.place(x=120,y=280)
l6=Label(t, text="Description:",bg='beige',foreground="brown")
l6.place(x=10,y=320)
para = Text(t, height=10, width=32,fg="brown")
para.place(x=120,y=320)

t.configure(bg="beige")
t.resizable(False,False)
t.mainloop()
