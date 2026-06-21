<?php
// ==========================================
// ALGORITMO DE PRUEBA - GABRIEL TUMBACO
// ==========================================

/* Este archivo contiene operadores aritméticos, relacionales, lógicos,
   palabras reservadas, delimitadores y estructuras de control
   para estresar a los analizadores léxico y sintáctico.
*/

# 1. Configuración Inicial y Arreglos Asociativos (Sección 4.2.5)
$sistema = [
    "ambiente" => "produccion",
    "version" => 2026,
    "intentos_maximos" => 3
];

$contador_accesos = 0;
$puntos_usuario = 10;

# 2. Captura de Datos por Consola (CLI)
echo "Iniciando sesion administrativa...";
$usuario_cli = readline("Ingrese el identificador del administrador: ");

# 3. Captura de Datos Web (Superglobal $_POST)
$token_web = $_POST["token_seguridad"];
$accion_web = $_POST["accion"];

# 4. Operadores de Asignación Compuesta (Sección 4.2.1)
$contador_accesos += 1;
$puntos_usuario -= 2;

# 5. Estructura de Control Condicional Anidada (Sección 4.2.4)
if ($usuario_cli == "admin" && $token_web == "XYZ123") {

    echo "Acceso CLI verificado.";

    // Condicional If-Else secundario dentro del bloque
    if ($accion_web == "actualizar" || $accion_web == "guardar") {

        // Llamada a función como instrucción independiente (Sección 4.2.6)
        ejecutar_respaldo($usuario_cli);

        $contador_accesos += 5;
        echo "Operacion web procesada con exito.";

    } else {
        echo "Accion web no reconocida o denegada.";
    }

} else {
    echo "Fallo de autenticacion en el sistema.";
    $contador_accesos += 1;
}

# 6. Verificación de Cierre
echo "Log de accesos registrados:";
echo $contador_accesos;

?>
