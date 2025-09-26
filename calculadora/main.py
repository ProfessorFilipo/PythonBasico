#######################################################
####              C A L C U L A D O R A            ####
#######################################################
#### Prof. Filipo Mor - github.com/ProfessorFilipo ####
#######################################################

from calc import somar, subtrair, multiplicar, dividir

def menu():
    print("=== Calculadora Simples ===")
    print("1 - Somar")
    print("2 - Subtrair")
    print("3 - Multiplicar")
    print("4 - Dividir")
    print("0 - Sair")

while True:
    menu()
    opcao = input("Escolha uma opção: ")

    if opcao == "0":
        print("Saindo...")
        break

    a = float(input("Digite o primeiro número: "))
    b = float(input("Digite o segundo número: "))

    if opcao == "1":
        print("Resultado:", somar(a, b))
    elif opcao == "2":
        print("Resultado:", subtrair(a, b))
    elif opcao == "3":
        print("Resultado:", multiplicar(a, b))
    elif opcao == "4":
        print("Resultado:", dividir(a, b))
    else:
        print("Opção inválida!")

