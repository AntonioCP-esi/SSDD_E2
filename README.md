# Servicio de Cálculo Remoto con ZeroC Ice y Apache Kafka

Este proyecto implementa un sistema distribuido de cálculo remoto que utiliza **ZeroC Ice** para invocar operaciones aritméticas 
básicas y **Apache Kafka** para recibir y enviar peticiones de cálculo serializadas en formato JSON.
-
---

## Requisitos previos

- Python 3.10
- Docker y Docker Compose
- Apache Kafka (iniciado vía Docker)
- Entorno virtual Python (`.venv`)
-
---
# Paso 1

Se inicia el docker(kafka): docker-compose up -d

# Paso 2
Se inicia el servidor Ice:
Con este comando:
ssdd-calculator --Ice.Config=config/calculator.config

# Paso 3
Crear un entorno virtual y entrar en el:
Con estos dos comandos
python3.10 -m venv .venv
source .venv/bin/activate

# Paso 4
Ejecutar el main(incluye el consumer y el producer):
(.venv) rubiocalzada@rubiocalzada-IdeaPad-3-15ITL6:~/Distribuidos/Lab/LabExtra/SSDD_E2$ python calculator/main.py

# Paso 5
Recibimos en el servidor y el consumer la respuesta, deserializada y con la operación realizada
Inicio de herramientas(por separado si hiciese falta):
---
Consumer.py:
(.venv) rubiocalzada@rubiocalzada-IdeaPad-3-15ITL6:~/Distribuidos/Lab/LabExtra/SSDD_E2/calculator$ python kafka_consumer.py
---
Producer.py:
(.venv) rubiocalzada@rubiocalzada-IdeaPad-3-15ITL6:~/Distribuidos/Lab/LabExtra/SSDD_E2/calculator$ python kafka_producer.py


La herramienta Producer es un extra, ya que realmente para enviar los mensajes se utiliza un formato JSON con la operación a realizar. Es conveniente ya que unicamente cambiamos el mensaje que queremos mandar dentro de la herramienta sin tener que escribir el comando.

Se inicia kafka, con 'docker-compose up -d', una vez iniciado el docker inciamos el servidor, con su 
comando, y ya ejecutamos el main que lanzara las herramientas, primero el consumer para deserializar 
y calcular la operacion, luego el producer que enviara el mensaje con la operacion y por ultimo el 
servidor recibira la respuesta con la operacion calculada.

# Errores en la ejecución
Al intentar hacer commit incluyendo en los archivos el entorno virtual "venv" me daba un error debido a:
GitHub me estaba dando este aviso importante:

calculator/.venv/lib/python3.10/site-packages/IcePy.cpython-310-x86_64-linux-gnu.so ocupa 80 MB, y GitHub recomienda no subir archivos mayores a 50 MB.

Una solución era no subir el entorno virtual (.venv) al repositorio ya que no es recomendable versionar .venv. Ocupa mucho espacio y puede causar errores. En su lugar, hacemos lo siguiente:

Borramos el .venv del repo (solo del control de versiones):
git rm -r --cached calculator/.venv

Añadimos .venv al archivo .gitignore:
echo ".venv/" >> .gitignore
git add .gitignore
git commit -m "Ignorar entorno virtual local (.venv)"
git push origin main

