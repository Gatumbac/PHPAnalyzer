<?php
// ==========================================
// ALGORITMO DE PRUEBA - DARWIN DÍAZ
// ==========================================

/* Este archivo contiene todas las estructuras definidas en el subconjunto de PHP:
   variables, tipos de datos, operadores, estructuras de control, arreglos y funciones.
*/

// 1. Tipos de datos, Variables y Peticiones HTTP
$edad = 25;
$precio = 15.50;
$nombre = "Proyecto Compiladores";
$activo = true;

$peticion_web = $_POST["usuario"]; 

// 2. Estructuras de Datos
$numeros = [1, 2, 3, 4, 5]; 
$configuracion = ["modo" => "desarrollo", "version" => 1]; 

// 3. Operaciones y Asignaciones
$subtotal = 100;
$iva = 12;
$total = $subtotal + $iva; 
$promedio = ($total + 50) / 2 * 3; 

$contador = 0;
$contador += 1; 
$contador -= 1; 

// 4. Declaración de Funciones y Llamadas
function calcular_descuento($monto, $porcentaje) { 
    return ($monto * $porcentaje) / 100;
}

$descuento = calcular_descuento($total, 10); 

// 5. Estructuras de Control y Expresiones Booleanas
while ($contador < 5) { 
    if ($contador == 3 || !$activo) { 
        break; 
    } else {
        echo "Iterando bucle"; 
    }
    $contador += 1;
}

/*
// =========================================================================
// 1. SECCIÓN DE ERRORES LÉXICOS
// =========================================================================

# Error Léxico 1: Carácter inválido '@' que no pertenece al alfabeto del lenguaje.
$invalido = 10 @ 5;

# Error Léxico 2: Carácter inválido '~' no reconocido por el componente léxico.
$variable_rara = ~100;


// =========================================================================
// 2. SECCIÓN DE ERRORES SINTÁCTICOS
// =========================================================================

# Error Sintáctico 1: Omisión del delimitador de fin de instrucción (Punto y coma).
$valor = 100

# Error Sintáctico 2: Estructura condicional 'if' sin los paréntesis obligatorios.
if $edad > 18 {
    echo "Mayor";
}

# Error Sintáctico 3: Operador de asignación compuesta incompleto (falta expresión derecha).
$contador += ;

# Error Sintáctico 4: Uso de punto y coma en lugar de coma para separar elementos de un arreglo.
$diccionario = ["clave1" => 1 ; "clave2" => 2];


// =========================================================================
// 3. SECCIÓN DE ERRORES SEMÁNTICOS
// =========================================================================

# Error Semántico 1: Uso de una variable que no ha sido declarada en la Tabla de Símbolos.
$resultado_falso = $variable_fantasma + 10;

# Error Semántico 2: Sentencia de ruptura 'break' utilizada fuera de un contexto de bucle.
if ($edad >= 18) {
    break; 
}

# Error Semántico 3: Operación aritmética entre tipos de datos incompatibles (String y Entero).
$texto = "Hola";
$error_tipo = $texto * 5;

# Error Semántico 4: Duplicidad o redeclaración de una función con el mismo identificador.
function procesar_datos() {
    return 1;
}
function procesar_datos() {
    return 2;
}
*/
?>