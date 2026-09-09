# AGENTS.md — Biblioteca Quiñones

## 1. Fuente oficial de verdad
El archivo `docs/Documento_Maestro_Biblioteca_v1.0.docx` es la especificación oficial del proyecto.

Antes de desarrollar o modificar cualquier funcionalidad:
1. Leer este archivo `AGENTS.md`.
2. Revisar el Documento Maestro v1.0.
3. Leer `docs/ESTADO_PROYECTO.md`.
4. Inspeccionar el código y el estado de Git.

No modificar por iniciativa propia reglas de negocio, arquitectura, tecnologías principales, roles, modelo de datos, criterios de aceptación o alcance definido en el Documento Maestro.

Si durante el desarrollo aparece una necesidad estructural no prevista:
- detener esa modificación;
- explicar el problema de forma breve;
- proponer una solución;
- esperar aprobación del usuario antes de cambiar la especificación;
- si se aprueba, registrar el cambio en `docs/REGISTRO_CAMBIOS.md` y actualizar el Documento Maestro si corresponde.

## 2. Alcance de trabajo por semana
Trabajar únicamente en la semana solicitada por el usuario.

No avanzar a funcionalidades de semanas posteriores salvo que sean un requisito técnico mínimo para completar o probar correctamente la semana actual.

Cada semana se considera terminada únicamente cuando:
- las actividades previstas han sido implementadas;
- las pruebas correspondientes han sido ejecutadas;
- los criterios de aceptación aplicables han sido verificados;
- las evidencias han sido guardadas;
- `docs/ESTADO_PROYECTO.md` ha sido actualizado;
- el usuario ha podido revisar el resultado.

## 3. Estilo de desarrollo
- Mantener el código sencillo, legible y apropiado para un proyecto académico de Prácticas Pre-Profesionales II.
- Evitar introducir frameworks, patrones, dependencias o abstracciones innecesarias.
- Usar las tecnologías congeladas en el Documento Maestro.
- Priorizar claridad y mantenibilidad sobre complejidad.
- Añadir comentarios solo cuando aporten comprensión real.
- Mantener nombres coherentes con el dominio del proyecto y preferentemente en español cuando formen parte del negocio.

## 4. Seguridad y secretos
Nunca:
- imprimir credenciales completas en respuestas o evidencias;
- subir `.env` a Git;
- incluir `DATABASE_URL`, contraseñas, tokens o `SECRET_KEY` en archivos versionados;
- copiar secretos a documentación.

Los secretos pueden utilizarse desde variables de entorno cuando sean necesarios para ejecutar o probar el proyecto.

## 5. Base de datos
La base de datos oficial será PostgreSQL alojada en Neon.

- No asumir que PostgreSQL está instalado localmente.
- Usar Psycopg 3 para las conexiones.
- Mantener scripts SQL versionados cuando correspondan.
- Preservar historial: los registros con historial asociado deben desactivarse en lugar de eliminarse físicamente desde la interfaz, según el Documento Maestro.
- Las modificaciones estructurales de BD deben respetar el modelo definido y quedar documentadas.

## 6. Git y GitHub
Antes de modificar archivos, revisar `git status`.

Durante el trabajo:
- hacer cambios pequeños y coherentes;
- no reescribir historia Git sin autorización;
- no ejecutar operaciones destructivas innecesarias;
- no hacer `push` de código no probado.

Al finalizar una tarea o semana aprobada:
- preparar un commit descriptivo;
- informar al usuario qué se incluirá;
- realizar `push` únicamente cuando corresponda y exista autenticación/configuración disponible.

## 7. Evidencias
Cada semana tiene su carpeta:
`docs/evidencias/semana_XX/`

Guardar, cuando corresponda:
- `SEMANA_XX_EVIDENCIA.md` con resumen de lo realizado;
- capturas de pantalla relevantes;
- resultados de pruebas;
- scripts SQL utilizados;
- PDFs generados;
- referencias a commits;
- enlaces de deployment cuando existan;
- cualquier otra evidencia académica útil.

No fabricar evidencias: toda evidencia debe corresponder a una ejecución o resultado real.

## 8. Pruebas
No considerar una funcionalidad terminada sin probarla.

Las pruebas deben incluir:
- camino principal;
- restricciones importantes;
- casos límite relevantes;
- criterios de aceptación aplicables.

Si una prueba falla:
- corregir la causa;
- volver a ejecutar;
- registrar el resultado final.

## 9. Resumen obligatorio al finalizar cada tarea
Al terminar, explicar al usuario de forma breve:
1. Qué se realizó.
2. Qué archivos principales se crearon o modificaron.
3. Qué pruebas se ejecutaron y sus resultados.
4. Qué criterios de aceptación se comprobaron.
5. Dónde quedaron las evidencias.
6. Qué acción manual debe realizar el usuario, si existe.
7. Qué problema, decisión o pendiente quedó abierto, si existe.

## 10. Regla de continuidad entre chats
No depender de conversaciones anteriores para conocer el estado real del proyecto.

La continuidad debe reconstruirse siempre desde:
- `AGENTS.md`;
- Documento Maestro v1.0;
- `docs/ESTADO_PROYECTO.md`;
- `docs/REGISTRO_CAMBIOS.md`;
- código actual;
- historial Git.
