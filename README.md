Se inicia el docker:
docker-compose up -d
-
Se inicia el servidor Ice:
(.venv) rubiocalzada@rubiocalzada-IdeaPad-3-15ITL6:~/Distribuidos/Lab/LabExtra/SSDD_E2$ ssdd-calculator --Ice.Config=config/calculator.config
-
ssdd-calculator --Ice.Config=config/calculator.config
-
-
-
Crear un entorno virtual y entrar en el:
python3.10 -m venv .venv
source .venv/bin/activate
-
-
Ejecutar el main(incluye el consumer y el producer):
(.venv) rubiocalzada@rubiocalzada-IdeaPad-3-15ITL6:~/Distribuidos/Lab/LabExtra/SSDD_E2$ python calculator/main.py
-
-
Inicio de herramientas:
(.venv) rubiocalzada@rubiocalzada-IdeaPad-3-15ITL6:~/Distribuidos/Lab/LabExtra/SSDD_E2/calculator$ python kafka_consumer.py

(.venv) rubiocalzada@rubiocalzada-IdeaPad-3-15ITL6:~/Distribuidos/Lab/LabExtra/SSDD_E2/calculator$ python kafka_producer.py
-
-
Producer para enviar los mensajes JSON, es un extra ya que se pueden escribir con comandos
-
Se inicia kafka, con 'docker-compose up -d', una vez iniciado el docker inciamos el servidor, con su 
comando, y ya ejecutamos el main que lanzara las herramientas, primero el consumer para deserializar 
y calcular la operacion, luego el producer que enviara el mensaje con la operacion y por ultimo el 
servidor recibira la respuesta con la operacion calculada.
-
Al intentar hacer commit incluyendo en los archivos el entorno virtual "venv" me daba un error debido a:
GitHub me estaba dando este aviso importante:
-
calculator/.venv/lib/python3.10/site-packages/IcePy.cpython-310-x86_64-linux-gnu.so ocupa 80 MB, y GitHub recomienda no subir archivos mayores a 50 MB.
-
Una solución era no subir el entorno virtual (.venv) al repositorio ya que no es recomendable versionar .venv. Ocupa mucho espacio y puede causar errores. En su lugar, hacemos lo siguiente:
-
Borramos el .venv del repo (solo del control de versiones):
git rm -r --cached calculator/.venv
-
Añadimos .venv al archivo .gitignore:
echo ".venv/" >> .gitignore
git add .gitignore
git commit -m "Ignorar entorno virtual local (.venv)"
git push origin main
-
