import re
print('------------------------')
print('Bem vindo ao programa que calcula os dois últimos números do seu CPF!')
print('------------------------')
# cpf_enviado = "506.746.398-80" \
#     .replace('.', '')\
#     .replace(' ', '')\
#     .replace('-', '')

cpf_enviado = input('Digite seu CPF: ')
cpf_enviado = re.sub(
    r'[^0-9]', '',
    cpf_enviado
)

nove_digitos = cpf_enviado[:9]
contador = 10
resultado = 0

for digito in nove_digitos:
    resultado += int(digito) * contador
    contador -= 1
    print(resultado)

# Multiplicar o resultado anterior por 10
print('------------------------')
print('Abaixo irei multiplicar o resultado anterior por 10:')
multiplicar_10 = resultado * 10
print(multiplicar_10)

# Obter o resto da divisão da conta anterior por 11
print('------------------------')
print('Esse é o primeiro número do seu CPF: ')
digito_1 = multiplicar_10 % 11

# Última condição para encontrar o primeiro dígito
if digito_1 > 9:
    digito_1 = 0
elif digito_1 <= 9:
    digito_1 = digito_1

    print(digito_1)

"""
Cálculo segundo digito: inserção do primeiro dígito na hora da multiplicação
"""

print('-----------------------------')
print('AGORA IREI CALCULAR O SEGUNDO NÚMERO DO CPF:')
print('-----------------------------')
dez_digitos = cpf_enviado[:10]
contador_2 = 11
resultado_2 = 0

for digito in dez_digitos:
    resultado_2 += int(digito) * contador_2
    contador_2 -= 1
    print(resultado_2)

# Multiplicar o resultado anterior por 10
print('------------------------')
print('Abaixo irei multiplicar o resultado anterior por 10:')
multiplicar_10 = resultado_2 * 10
print(multiplicar_10)

# Obter o resto da divisão da conta anterior por 11
print('------------------------')
print('Esse é o segundo número do seu CPF: ')
digito_2 = multiplicar_10 % 11
# Última condição para encontrar o segundo dígito
if digito_2 > 9:
    digito_2 = 0
elif digito_2 <= 9:
    digito_2 = digito_2

print(digito_2)
print('------------------------')

cpf_calculado = f'{nove_digitos}{digito_1}{digito_2}'
print(cpf_calculado)

if cpf_enviado == cpf_calculado:
    print(f'Seu CPF é válido.')
else:
    print('Seu CPF é inválido.')
