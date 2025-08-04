import Convergent


# Encrypt data
plaintext = b"Hello, World!"
encrypted_data = Convergent.encrypt(plaintext)

# Decrypt data
decrypted_data = Convergent.decrypt(encrypted_data)

print("Plaintext:", plaintext)
print("Encrypted:", encrypted_data)
print("Decrypted:", decrypted_data)
