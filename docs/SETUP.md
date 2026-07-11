# Levantamiento local de PHPAnalyzer

Guía paso a paso para ejecutar PHPAnalyzer en tu ordenador. El proyecto es un monorepo con tres piezas:

- **Core del analizador** (`packages/analyzer`): lógica de análisis léxico/sintáctico/semántico de PHP, en Python.
- **API** (`apps/api`): servicio HTTP con FastAPI que expone el core.
- **Web** (`apps/web`): interfaz React + Vite + TypeScript que consume la API.

> Convención de puertos: API en `http://localhost:8000` y Web en `http://localhost:5173`.

---

## 1. Requisitos previos

Antes de empezar, verifica que tienes instalado lo siguiente:

| Herramienta | Versión mínima | Cómo verificar |
|-------------|----------------|----------------|
| Python | 3.10 | `python --version` |
| Node.js | 18 | `node --version` |
| pnpm | 9.x | `pnpm --version` |
| Git | cualquiera reciente | `git --version` |

Si no tienes `pnpm`, instálalo con:

```bash
npm install -g pnpm@9
```

---

## 2. Clonar el repositorio

```bash
git clone https://github.com/Gatumbac/PHPAnalyzer.git
cd PHPAnalyzer
```

---

## 3. Configurar el backend (Python)

El backend necesita un entorno virtual con las dependencias del core **y** de la API.

### 3.1 Crear y activar el entorno virtual

```bash
python -m venv .venv
```

Activa el entorno según tu sistema operativo:

- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
  > Si PowerShell bloquea la ejecución de scripts, habilita temporalmente con:
  > `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

- **Windows (CMD):**
  ```cmd
  .venv\Scripts\activate.bat
  ```

- **Linux / macOS:**
  ```bash
  source .venv/bin/activate
  ```

Sabrás que está activo cuando el prompt muestre `(.venv)` al inicio.

### 3.2 Instalar las dependencias de Python

Desde la raíz del repositorio (con el entorno activo):

```bash
pip install -r requirements.txt
pip install -r apps/api/requirements.txt
```

- `requirements.txt` (raíz) instala `ply` (motor del analizador).
- `apps/api/requirements.txt` instala `fastapi`, `uvicorn`, `pytest` y `httpx`.

Verifica que todo quedó bien:

```bash
python -c "import fastapi, uvicorn, ply; print('OK')"
```

---

## 4. Configurar el frontend (Web)

### 4.1 Instalar dependencias de Node

Desde la raíz del repositorio:

```bash
pnpm install
```

Esto instala las dependencias del workspace, incluyendo las de `apps/web`.

### 4.2 Configurar la variable de entorno

Crea el archivo `.env` dentro de `apps/web`. Puedes copiar el ejemplo:

- **Windows (PowerShell):**
  ```powershell
  Copy-Item apps\web\.env.example apps\web\.env
  ```

- **Linux / macOS:**
  ```bash
  cp apps/web/.env.example apps/web/.env
  ```

El contenido debe ser:

```env
VITE_API_URL=http://localhost:8000
```

> Si tu API corre en otro host/puerto, ajusta este valor para que apunte a ella.

---

## 5. Levantar los servicios

Necesitas **dos terminales**: una para la API y otra para la Web. Mantén ambas abiertas mientras uses la aplicación.

### 5.1 Levantar la API (terminal 1)

Asegúrate de que el entorno virtual esté activado y de estar en la **raíz del repositorio** (el comando usa `apps.api.main`, que requiere esa ubicación).

```bash
uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000
```

Verás algo como:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

> `--reload` reinicia el servidor automáticamente cuando cambias archivos Python. Quítalo si prefiere estabilidad.

### 5.2 Levantar la Web (terminal 2)

Desde la raíz del repositorio:

```bash
pnpm web:dev
```

Verás algo como:

```
  VITE v5.x  ready in xxx ms
  ➜  Local:   http://localhost:5173/
```

---

## 6. Verificar que todo funciona

### 6.1 Probar la API

Abre en el navegador (o con `curl`):

- `http://localhost:8000/health` → debe responder `{"status":"ok"}`
- `http://localhost:8000/docs` → documentación interactiva de FastAPI (Swagger UI).

Ejemplo con `curl`:

```bash
curl http://localhost:8000/health
# {"status":"ok"}

curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d "{\"source_code\":\"<?php $x = 10 + 5; echo $x; ?>\",\"include_tokens\":true}"
```

### 6.2 Probar la Web

Abre `http://localhost:5173/` en el navegador. Deberías ver:

- El editor de código con un ejemplo PHP precargado.
- El indicador de estado de la API (debe decir **API disponible**).
- Al pulsar **Ejecutar Analisis**, el inspector muestra la tabla de tokens y el estado del análisis.

---

## 7. Detener los servicios

En cada terminal, pulsa `Ctrl + C` para detener el proceso correspondiente.

---

## 8. Solución de problemas comunes

### El navegador muestra "API no disponible"

- Confirma que la API está corriendo en el puerto 8000 (`http://localhost:8000/health`).
- Revisa que `apps/web/.env` exista y `VITE_API_URL` apunte a `http://localhost:8000`.
- Reinicia la Web después de cambiar `.env` (Vite no recarga variables de entorno en caliente).

### Error: `uvicorn: command not found` / `ModuleNotFoundError: No module named 'fastapi'`

El entorno virtual no está activo o faltan dependencias. Repite los pasos 3.1 y 3.2.

### Error: `Failed to resolve import "./lib/api"`

Faltan archivos del frontend. Asegúrate de haber ejecutado `pnpm install` y de que `apps/web/src/lib/` contenga `api.ts` y `exportLogs.ts`.

### El puerto ya está en uso

Si `8000` o `5173` están ocupados por otro proceso:

- Cambia el puerto de la API: `uvicorn apps.api.main:app --reload --port 8001` y actualiza `VITE_API_URL` en `apps/web/.env`.
- Cambia el puerto de la Web: edita `apps/web/vite.config.ts` y añade `server: { port: 5174 }`, o ejecuta `pnpm --filter web dev -- --port 5174`.

### PowerShell bloquea `Activate.ps1`

Ejecuta una vez por sesión:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

---

## 9. Resumen rápido (para quienes ya conocen el proyecto)

```bash
# Backend
python -m venv .venv
.venv\Scripts\Activate.ps1            # Windows  |  source .venv/bin/activate  (Linux/macOS)
pip install -r requirements.txt -r apps/api/requirements.txt
uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (otra terminal)
pnpm install
cp apps/web/.env.example apps/web/.env   # solo la primera vez
pnpm web:dev
```

Abre `http://localhost:5173` y pulsa **Ejecutar Analisis**.