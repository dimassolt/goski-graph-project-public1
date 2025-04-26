import bcrypt

password = 'abc123'
# Hash and print password
hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
print(hashed_pw.decode())
