<?php
// ==========================================
// ALGORITMO DE PRUEBA - GABRIEL TUMBACO
// ==========================================

/* Este archivo contiene operadores aritméticos, relacionales, lógicos,
   palabras reservadas, delimitadores y estructuras de control
   para estresar el analizador léxico.
*/

# 1. Pruebas de Operadores Aritméticos

$a = 10;
$b = 3;
$suma = $a + $b;
$resta = $a - $b;
$producto = $a * $b;
$division = $a / $b;
$modulo = $a % $b;

# 2. Pruebas de Operadores de Asignación Compuesta

$contador = 0;
$contador += 5;
$contador -= 2;

# 3. Pruebas de Operadores Relacionales

$mayor = $a > $b;
$menor = $a < $b;
$mayor_igual = $a >= $b;
$menor_igual = $a <= $b;
$igualdad = $a == $b;
$diferencia = $a != $b;

# 4. Pruebas de Estructuras de Control y Operadores Lógicos

if ($a > $b && $a != 0) {
    echo "A es mayor y distinto de cero";
}

if ($a < $b || $b == 0) {
    echo "Condicion OR cumplida";
} else {
    echo "Condicion OR no cumplida";
}

$activo = true;
if (!$activo) {
    echo "No activo";
}

# 5. Pruebas de Bucle While con Break

$i = 0;
while ($i < 10) {
    if ($i == 5) {
        break;
    }
    $i += 1;
}

# 6. Pruebas de Funciones

function sumar($x, $y) {
    return $x + $y;
}

$resultado = sumar(4, 6);
echo $resultado;

# 7. Pruebas de Arreglos y Delimitadores

$numeros = [1, 2, 3, 4, 5];
$persona = ["nombre" => "Gabriel", "edad" => 22];

# 8. Prueba de Expresiones con Agrupación

$promedio = ($a + $b) / 2;

?>
