import pyzipper
from itertools import product
import string
import concurrent.futures

# Caminho para o arquivo ZIP
zip_file_path = 'file.zip'

# Função para tentar abrir o arquivo com a senha fornecida
def try_password(password):
    try:
        with pyzipper.AESZipFile(zip_file_path) as zip_file:
            # Tenta extrair o conteúdo com a senha fornecida
            zip_file.extractall(pwd=password.encode('utf-8'))
            print(f'Senha encontrada: {password}')
            return True
    except (RuntimeError, pyzipper.BadZipFile, pyzipper.LargeZipFile):
        # Captura exceções específicas que indicam falha na senha ou arquivo ZIP grande
        return False
    except Exception as e:
        # Captura outras exceções e exibe para depuração
        print(f'Erro ao tentar senha {password}: {e}')
        return False

# Função para gerar combinações de senhas
def generate_passwords(characters, length):
    return (''.join(password_tuple) for password_tuple in product(characters, repeat=length))

# Tenta as senhas usando programação paralela
def brute_force_zip(zip_file_path, max_simultaneous=10000):
    # Definindo diferentes conjuntos de caracteres para as senhas
    numeric_characters = string.digits
    alpha_characters = string.ascii_letters
    alphanumeric_characters = string.ascii_letters + string.digits

    # Tentando senhas numéricas
    for length in range(1, 20):  # Tentando senhas de 1 até 5 caracteres
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_simultaneous) as executor:
            password_combinations = generate_passwords(numeric_characters, length)
            future_to_password = {executor.submit(try_password, pw): pw for pw in password_combinations}
            for future in concurrent.futures.as_completed(future_to_password):
                if future.result():
                    return

    # Tentando senhas alfabéticas
    for length in range(1, 20):
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_simultaneous) as executor:
            password_combinations = generate_passwords(alpha_characters, length)
            future_to_password = {executor.submit(try_password, pw): pw for pw in password_combinations}
            for future in concurrent.futures.as_completed(future_to_password):
                if future.result():
                    return

    # Tentando senhas alfanuméricas
    for length in range(1, 20):
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_simultaneous) as executor:
            password_combinations = generate_passwords(alphanumeric_characters, length)
            future_to_password = {executor.submit(try_password, pw): pw for pw in password_combinations}
            for future in concurrent.futures.as_completed(future_to_password):
                if future.result():
                    return

    print("Senha não encontrada ou o arquivo pode estar corrompido.")

# Executa a função de força bruta
brute_force_zip(zip_file_path)
