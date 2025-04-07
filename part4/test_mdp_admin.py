from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
new_hash = bcrypt.generate_password_hash("admin1234").decode("utf-8")
print(new_hash)
