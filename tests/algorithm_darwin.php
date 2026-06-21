<?php
// =========================================================================
// ALGORITMO DE PRUEBA - DARWIN DÍAZ
// =========================================================================

/* Este archivo contiene operadores aritméticos, relacionales, lógicos,
   palabras reservadas, delimitadores y estructuras de control
   para estresar a los analizadores léxico y sintáctico.
*/

# 1. Inicialización de Variables y Estructuras de Datos

$nombre_curso = "Programacion de Compiladores 2026";
$calificaciones = [8.5, 9.2, 6.4, 4.5, 7.0];
$limite_aprobacion = 7.0;
$total_estudiantes = 5;

# 2. Solicitud de datos por teclado

$registro_activo = readline();

# 3. Definición de Función con Retorno y Parámetros

function evaluar_estado($nota, $minimo) {
    // Expresión aritmética con múltiples operadores
    $porcentaje_score = ($nota * 10) / 1;
    return $porcentaje_score;
}

# 4. Estructura de Control Compleja

$indice = 0;
while ($indice < $total_estudiantes) {

    $nota_actual = $calificaciones; // Simulación de acceso/asignación simple
    $score = evaluar_estado($nota_actual, $limite_aprobacion);

    // Condición con operadores relacionales y conectores lógicos compuestos
    if (($nota_actual >= $limite_aprobacion) && ($registro_activa == true)) {
        echo "Estudiante aprobado con excelente puntaje.";
    } else {
        echo "Estudiante requiere examen de recuperacion.";
    }

    // Condición de control para salida forzada con Break
    if ($nota_actual == 0.0) {
        break;
    }

    $indice = $indice + 1;
}

# 5. Impresión de Cierre de Bloque

echo "Procesamiento de actas finalizado para el curso:";
echo $nombre_curso;

?>
