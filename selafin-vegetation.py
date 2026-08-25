from data_manip.extraction.telemac_file import TelemacFile
import numpy as np
# ---------------------------------------------------------
# 1. Archivos
# ---------------------------------------------------------
archivo_entrada = "geo_dragforce.slf"
archivo_salida = "geo_porosity.slf"

# ---------------------------------------------------------
# 2. Leer malla existente
# ---------------------------------------------------------
geo = TelemacFile(archivo_entrada)

x = geo.meshx
y = geo.meshy
tri = geo.tri.triangles

print("Numero de nodos:", len(x))
print("Variables existentes:", geo.varnames)

# ---------------------------------------------------------
# 3. Crear nueva variable POROSITY
# ---------------------------------------------------------
# Por defecto todo el dominio tiene porosidad = 1
porosity = np.ones(len(x), dtype=float)

# ---------------------------------------------------------
# 4. ZONA CUADRADA
#
# Aquí ponemos porosidad = 0.6 en una zona rectangular
# ---------------------------------------------------------
xmin = 0.0
xmax = 40.0

ymin = 0.0
ymax = 15.0
zona = (
    (x >= xmin) &
    (x <= xmax) &
    (y >= ymin) &
    (y <= ymax)
)
porosity[zona] = 0.6
print("Nodos con vegetacion:", np.sum(zona))

# ---------------------------------------------------------
# 5. Crear nuevo archivo SLF
# ---------------------------------------------------------
nuevo = TelemacFile(
    archivo_salida,
    access="w",
    overwrite=True
)
nuevo.add_header(
    "POROSITY",
    date=geo.get_mesh_date()
)
# Misma malla
nuevo.add_mesh(
    x,
    y,
    tri
)

# ---------------------------------------------------------
# 6. Copiar las variables existentes
# ---------------------------------------------------------
for nombre, unidad in zip(geo.varnames, geo.varunits):

    nuevo.add_variable(
        nombre,
        unidad
    )

# ---------------------------------------------------------
# 7. Añadir POROSITY
# ---------------------------------------------------------
nuevo.add_variable(
    "POROSITY",
    "-"
)

# ---------------------------------------------------------
# 8. Copiar los valores existentes
#
# Para una geometry.slf normalmente tenemos un único
# registro temporal: record = 0
# ---------------------------------------------------------
for ivar, nombre in enumerate(geo.varnames):

    valores = geo.get_data_value(
        nombre,
        0
    )

    nuevo._values[0, ivar, :] = valores

# ---------------------------------------------------------
# 9. Introducir POROSITY
# ---------------------------------------------------------
indice_porosity = len(geo.varnames)

nuevo._values[
    0,
    indice_porosity,
    :
] = porosity

# ---------------------------------------------------------
# 10. Escribir archivo
# ---------------------------------------------------------
nuevo.write()

nuevo.close()
geo.close()

print("Archivo creado:", archivo_salida)
