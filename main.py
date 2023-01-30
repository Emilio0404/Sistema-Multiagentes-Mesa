from flask import Flask
from ambiente import Ambiente


app = Flask(__name__)
modelo = Ambiente(100, 100)

@app.route('/', methods=["GET"])
def get_model():
    modelo.step()
    return modelo.mandar_json_a_unity()


def main():
    from ambiente import Ambiente
    modelo = Ambiente(100, 100)

    # Para representar intervalos de 15 minutos se multiplica las 24 horas por 4
    for i in range(0, 24 * 4):
        hora = i // 4 if i // 4 >= 10 else "0" + str(i // 4)
        minutos = i * 15  % 60 if i * 15  % 60 > 10 else "0" + str(i * 15  % 60)
        print(hora, ":", minutos, " ", "Iteración:", i, sep="")
        modelo.step()

if __name__ == "__main__":
    main()