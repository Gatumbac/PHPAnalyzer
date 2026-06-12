<?php
// ==========================================
// ALGORITMO DE PRUEBA - DARWIN DÍAZ
// ==========================================

/* Este archivo contiene diferentes tipos de variables,
   tipos de datos primitivos (enteros, flotantes, strings, booleanos)
   y variaciones de comentarios para estresar el analizador léxico.
*/

# 1. Pruebas de Comentarios
// Este es un comentario de una sola línea (estilo C++)
# Este es otro comentario de una sola línea (estilo Shell/Perl)

/*
   Este es un comentario multilínea
   diseñado para verificar que el lexer ignore correctamente
   los saltos de línea y el texto dentro de los delimitadores.
*/

# 2. Pruebas de Tipos de Datos Primitivos y Variables

// Variables con números enteros (Integer)
$edad_usuario = 25;
$id_registro = 100456;
$temperatura_minima = -5; // Entero negativo

// Variables con números de punto flotante (Float)
$precio_producto = 19.99;
$pi_aproximado = 3.14159;
$puntaje_promedio = 0.5;
$saldo_negativo = -120.45; // Flotante negativo

// Variables con Cadenas de Texto (String)
$nombre_simple = 'Darwin Diaz';
$saludo_complejo = "Bienvenido al sistema de pruebas léxicas del compilador.";
$string_vacio = "";
$string_con_numeros = "ID-999_Usuario";

// Variables con Valores Booleanos (Boolean)
$estado_activo = true;
$procesar_datos = false;
$es_valido = TRUE;  // Variante en mayúsculas
$tiene_permiso = FALSE; // Variante en mayúsculas

# 3. Bloque mixto para evaluar la correcta separación de tokens en secuencia
$resultado_final = $precio_producto;
$mensaje_log = "El proceso ha terminado de forma exitosa.";
$finalizado = true;

// Fin del archivo de prueba
?>