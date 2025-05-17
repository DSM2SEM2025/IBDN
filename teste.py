from passlib.hash import bcrypt

hash = bcrypt.hash("teste")
print(bcrypt.verify("teste", hash))  # Deve retornar True
