# Sistema de reserva de turnos médicos

## Cómo iniciar

Se necesita Python 3.10 o posterior (el programa utiliza `match`). Abra una
terminal en esta carpeta y ejecute:

python Home.py


El programa es de consola. Los archivos de datos se leen y escriben en la
carpeta de trabajo desde la que se ejecuta `Home.py`.

## Módulos

- Home.py: menú principal
- Pacientes.py: alta, consulta, listado y modificación de pacientes.
- Profesionales.py: alta, baja, consulta, edición y horarios de profesionales.
- Especialidades.py: gestión de especialidades.
- Turnero.py: asignación, consulta, reprogramación y cancelación de turnos.

## Archivos de datos


- especialidades.json: lista JSON de nombres de especialidades. En la primera
  ejecución se crea con Cardiología, Clínica Médica y Traumatología.
- pacientes.txt: un paciente por línea, con campos separados por `;`:
  DNI;nombre;apellido;cobertura. Si falta, se crea con tres pacientes de
  ejemplo (DNI 10000001 a 10000003).
- profesionales.txt: un profesional por línea. El formato actual tiene 33
  campos: legajo, nombre, especialidad, duración del turno, cantidad de
  sobreturnos y cuatro campos de horario por cada día de la semana (dos
  intervalos posibles). Un intervalo no usado se representa con `-;-`. Si falta,
  se crea con tres profesionales de ejemplo (legajos 1 a 3). Las altas asignan
  automáticamente el siguiente legajo numérico disponible.
- `turnos.txt: un turno por línea: `DNI;legajo;DD/MM/AAAA;HH:MM`.
- `pacientes_aux.txt`, `profesionales_aux.txt` y `turnos_aux.txt`: archivos
  temporales que se usan al reescribir registros para modificar o quitar datos.


## Manejo de archivos en el programa

Las operaciones de consulta abren el archivo en modo lectura (`rt`) y procesan
sus líneas una por una. Las altas abren en modo agregado (`at`) y añaden una
nueva línea al final, sin reemplazar los datos existentes. La codificación
UTF-8 permite guardar nombres con tildes.

Para modificar o quitar registros, los módulos leen el archivo original y
escriben en el archivo auxiliar. Al terminar, cierran ambos y reemplazan el
original renombrando el auxiliar. La misma estrategia se usa al cambiar una
especialidad en los profesionales. Si no existe el original, las consultas
informan que todavía no hay registros. `especialidades.json`, `pacientes.txt`
y `profesionales.txt` tienen una carga inicial automática cuando cada archivo
no existe. Las cargas de pacientes y profesionales contienen datos de ejemplo;
si el archivo ya existe, no se agregan ni reemplazan registros.

Los auxiliares deben permanecer en la misma carpeta que sus archivos
originales, ya que allí se realiza el reemplazo. Si una ejecución se interrumpe
durante una actualización, puede quedar un auxiliar pendiente; el programa no
lo recupera automáticamente.
