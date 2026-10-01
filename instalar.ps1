<#
.SYNOPSIS
    Prepara todo el entorno local del Sistema de Trámites Municipales.

.DESCRIPTION
    Ejecuta la instalación completa en un solo comando:
      1. Verifica las herramientas (Python, PostgreSQL, Redis, Ollama, Node).
      2. Crea el archivo .env a partir de .env.example.
      3. Crea el rol y la base de datos, aplica migraciones y carga los seeds.
      4. Crea el entorno virtual e instala las dependencias Python.
      5. Instala las dependencias del front-end.
      6. Asegura Redis y Ollama levantados y descarga el modelo del SLM.
      7. Genera los embeddings (BGE-M3) de los documentos para el RAG.

    Es idempotente: se puede volver a ejecutar sin romper nada.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\instalar.ps1

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\instalar.ps1 -OllamaModel gemma4 -SinIndexar
#>

[CmdletBinding()]
param(
    [string]$PostgresUser = 'postgres',
    [string]$PostgresPassword = $(if ($env:PGPASSWORD) { $env:PGPASSWORD } else { 'postgres' }),
    [string]$AppUser = 'tramites',
    [string]$AppPassword = 'tramites',
    [string]$AppDatabase = 'tramites_municipales',
    [string]$OllamaModel = 'qwen2.5:3b',
    [switch]$SinIndexar
)

$ErrorActionPreference = 'Stop'
$raiz = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $raiz

$fallos = New-Object System.Collections.Generic.List[string]

function Paso([string]$mensaje) { Write-Host "`n==> $mensaje" -ForegroundColor Cyan }
function Ok([string]$mensaje)  { Write-Host "    [ok] $mensaje" -ForegroundColor Green }
function Info([string]$mensaje) { Write-Host "    $mensaje" }
function Omitido([string]$m)   { Write-Host "    [--] $m" -ForegroundColor DarkGray }
function Falla([string]$m) {
    Write-Host "    [!!] $m" -ForegroundColor Red
    $fallos.Add($m)
}

function Test-Herramienta([string]$comando, [string]$paquete) {
    if (Get-Command $comando -ErrorAction SilentlyContinue) { return $true }
    Falla "Falta '$comando' ($paquete)"
    return $false
}

function Invoke-Nativo([string]$archivo, [string[]]$argumentos, [string]$descripcion) {
    & $archivo @argumentos
    if ($LASTEXITCODE -ne 0) { throw "$descripcion falló (código $LASTEXITCODE)" }
}

# ---------------------------------------------------------------- 1. Herramientas
Paso '1/7 · Verificando herramientas'

$faltan = @()
foreach ($c in @(
    @{ cmd = 'python';  paquete = 'Python 3.11+ (https://python.org)' },
    @{ cmd = 'psql';    paquete = 'PostgreSQL (https://postgresql.org)' },
    @{ cmd = 'node';    paquete = 'Node.js 18+ (https://nodejs.org)' },
    @{ cmd = 'npm';     paquete = 'npm (incluido con Node.js)' },
    @{ cmd = 'ollama';  paquete = 'Ollama (https://ollama.com/download)' }
)) {
    if (Test-Herramienta $c.cmd $c.paquete) { Ok $c.cmd }
}

$redis = Get-Command redis-server -ErrorAction SilentlyContinue
if ($redis) { Ok 'redis-server' } else { Info 'redis-server no está en el PATH (opcional: puede instalarse como servicio)' }

if ($fallos.Count -gt 0) {
    Write-Host "`nFaltan herramientas necesarias. Instálalas y vuelve a ejecutar:" -ForegroundColor Red
    $fallos | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
    exit 1
}

# ---------------------------------------------------------------- 2. .env
Paso '2/7 · Archivo de configuración'
if (Test-Path '.env') {
    Omitido '.env ya existe'
} else {
    Copy-Item '.env.example' '.env'
    Ok '.env creado desde .env.example'
}

# ---------------------------------------------------------------- 3. Base de datos
Paso '3/7 · Base de datos (rol, migraciones y datos)'

$env:PGPASSWORD = $PostgresPassword
$existeRol = psql -h localhost -U $PostgresUser -t -c "SELECT 1 FROM pg_roles WHERE rolname='$AppUser';" 2>$null
if ($LASTEXITCODE -ne 0) {
    Falla "No se pudo conectar a PostgreSQL como '$PostgresUser'. Revisa el usuario/contraseña (-PostgresPassword)."
} else {
    if ($existeRol -match '1') {
        Omitido "rol '$AppUser' ya existe"
    } else {
        try {
            Invoke-Nativo 'psql' @('-h','localhost','-U',$PostgresUser,'-c',
                "CREATE ROLE $AppUser LOGIN PASSWORD '$AppPassword' CREATEDB;") "crear rol"
            Ok "rol '$AppUser' creado"
        } catch { Falla $_.Exception.Message }
    }

    $existeDb = psql -h localhost -U $PostgresUser -t -c "SELECT 1 FROM pg_database WHERE datname='$AppDatabase';" 2>$null
    if ($existeDb -match '1') {
        Omitido "base '$AppDatabase' ya existe"
    } else {
        try {
            Invoke-Nativo 'psql' @('-h','localhost','-U',$PostgresUser,'-c',
                "CREATE DATABASE $AppDatabase OWNER $AppUser;") "crear base de datos"
            Ok "base '$AppDatabase' creada"
        } catch { Falla $_.Exception.Message }
    }

    $env:PGPASSWORD = $AppPassword
    $archivos = @(
        'database/migrations/002_create_tables.sql',
        'database/migrations/003_create_vectors.sql',
        'database/seeds/municipios.sql',
        'database/seeds/tramites.sql',
        'database/seeds/documentos.sql'
    )
    foreach ($archivo in $archivos) {
        try {
            Invoke-Nativo 'psql' @('-h','localhost','-U',$AppUser,'-d',$AppDatabase,
                '-v','ON_ERROR_STOP=1','-q','-f',$archivo) $archivo
            Ok $archivo
        } catch { Falla $_.Exception.Message }
    }
}

# ---------------------------------------------------------------- 4. Python
Paso '4/7 · Dependencias Python'
$pythonVenv = if ($IsWindows -or $env:OS -eq 'Windows_NT') { '.venv\Scripts\python.exe' } else { '.venv/bin/python' }
if (Test-Path $pythonVenv) {
    Omitido 'entorno virtual .venv ya existe'
} else {
    Invoke-Nativo 'python' @('-m','venv','.venv') 'crear entorno virtual'
    Ok '.venv creado'
}
& $pythonVenv -m pip install --quiet --disable-pip-version-check -r requirements.txt
if ($LASTEXITCODE -eq 0) { Ok 'requirements.txt instalado' } else { Falla 'falló la instalación de requirements.txt' }

# ---------------------------------------------------------------- 5. Front-end
Paso '5/7 · Dependencias del front-end'
if (Test-Path 'frontend-tramites/package.json') {
    Push-Location 'frontend-tramites'
    npm install --silent
    if ($LASTEXITCODE -eq 0) { Ok 'node_modules listo' } else { Falla 'falló npm install' }
    Pop-Location
} else {
    Falla 'no se encontró frontend-tramites/package.json'
}

# ---------------------------------------------------------------- 6. Redis y Ollama
Paso '6/7 · Servicios locales y modelo del SLM'

$puerto = { param($n) (Test-NetConnection -ComputerName localhost -Port $n -WarningAction SilentlyContinue).TcpTestSucceeded }

if (& $puerto 6379) {
    Ok 'Redis escuchando en 6379'
} elseif ($redis) {
    Start-Process -FilePath $redis.Source -ArgumentList '--port','6379' -WindowStyle Hidden
    Start-Sleep -Seconds 2
    if (& $puerto 6379) { Ok 'Redis iniciado' } else { Falla 'Redis no respondió en el puerto 6379' }
} else {
    Info 'Redis no está instalado: la caché quedará deshabilitada'
}

if (-not (& $puerto 11434)) {
    $ollamaExe = (Get-Command ollama).Source
    Start-Process -FilePath $ollamaExe -ArgumentList 'serve' -WindowStyle Hidden
    Start-Sleep -Seconds 4
}
if (& $puerto 11434) { Ok 'Ollama escuchando en 11434' } else { Falla 'Ollama no respondió en el puerto 11434' }

if ((ollama list | Select-String -SimpleMatch $OllamaModel)) {
    Omitido "modelo '$OllamaModel' ya descargado"
} else {
    Info "descargando modelo '$OllamaModel' (puede tardar unos minutos)..."
    ollama pull $OllamaModel
    if ($LASTEXITCODE -eq 0) { Ok "modelo '$OllamaModel' descargado" } else { Falla "fallo al descargar '$OllamaModel'" }
}

# ---------------------------------------------------------------- 7. Embeddings
Paso '7/7 · Embeddings de los documentos (BGE-M3)'
if ($SinIndexar) {
    Omitido 'omitido por -SinIndexar (el RAG no tendrá documentos que recuperar)'
} else {
    Info 'la primera vez descarga el modelo BGE-M3 (~2.3 GB) y tarda unos minutos'
    & $pythonVenv -m backend.scripts.indexar_documentos
    if ($LASTEXITCODE -eq 0) { Ok 'documentos indexados' } else { Falla 'falló la indexación de documentos' }
}

# ---------------------------------------------------------------- Resumen
Write-Host ''
if ($fallos.Count -eq 0) {
    Write-Host 'Instalación completada.' -ForegroundColor Green
} else {
    Write-Host "Instalación terminada con $($fallos.Count) problema(s):" -ForegroundColor Yellow
    $fallos | ForEach-Object { Write-Host "  - $_" -ForegroundColor Yellow }
}

Write-Host @'

Para arrancar el sistema:

  .venv\Scripts\Activate.ps1
  cd backend; uvicorn main:app --reload --port 8000
  cd ..\frontend-tramites; npm run dev      (en otra terminal)

  API .............. http://localhost:8000
  Swagger ........... http://localhost:8000/docs
  App .............. http://localhost:3000

'@ -ForegroundColor Cyan

if ($fallos.Count -gt 0) { exit 1 }