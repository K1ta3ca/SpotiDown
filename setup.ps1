# setup.ps1 - Скрипт за настройка на средата и зависимостите

# --- Конфигурация ---
$venvDir = ".\.venv"
$requirementsFile = ".\requirements.txt"
$ffmpegDir = ".\ffmpeg"
$ffmpegExe = Join-Path -Path $ffmpegDir -ChildPath "bin\ffmpeg.exe"

# --- Функции за съобщения ---
function Write-Success($message) { Write-Host $message -ForegroundColor Green }
function Write-Warning($message) { Write-Host $message -ForegroundColor Yellow }
function Write-Error($message) { Write-Host $message -ForegroundColor Red }

# --- Основна логика ---
try {
    # 1. Проверка за Python
    Write-Host "1. Checking for Python..."
    $pythonExists = (Get-Command python -ErrorAction SilentlyContinue)
    if (-not $pythonExists) {
        Write-Error "ERROR: Python is not installed or not found in your PATH."
        throw "Python not found."
    }
    Write-Success "   Python found."

    # 2. Настройка на виртуална среда
    Write-Host "2. Setting up virtual environment..."
    if (-not (Test-Path -Path $venvDir)) {
        Write-Warning "   Virtual environment not found. Creating..."
        python -m venv $venvDir
        Write-Success "   Virtual environment created."
    } else {
        Write-Success "   Virtual environment already exists."
    }
    $pip = Join-Path -Path $venvDir -ChildPath "Scripts\pip.exe"

    # 3. Инсталиране на Python библиотеки
    Write-Host "3. Installing Python libraries..."
    if (Test-Path -Path $requirementsFile) {
        & $pip install -r $requirementsFile | Out-Null
        Write-Success "   Libraries are up to date."
    } else {
        Write-Warning "   requirements.txt not found. Skipping."
    }

    # 4. Инсталиране на FFmpeg
    Write-Host "4. Checking for FFmpeg..."
    if (-not (Test-Path -Path $ffmpegExe)) {
        Write-Warning "   FFmpeg not found. Attempting to download..."
        $zipFile = "ffmpeg.zip"
        $ffmpegUrl = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        
        Write-Host "   Downloading from $ffmpegUrl (this may take a moment)..."
        Invoke-WebRequest -Uri $ffmpegUrl -OutFile $zipFile -UseBasicParsing
        
        Write-Host "   Extracting archive..."
        Expand-Archive -Path $zipFile -DestinationPath $ffmpegDir -Force
        
        # Преместване на файловете от подпапката
        $subDir = Get-ChildItem -Path $ffmpegDir -Directory | Select-Object -First 1
        if ($subDir) {
            Move-Item -Path ($subDir.FullName + '\*') -Destination $ffmpegDir -Force
            Remove-Item -Path $subDir.FullName -Recurse -Force
        }
        
        Remove-Item -Path $zipFile
        Write-Success "   FFmpeg installed successfully!"
    } else {
        Write-Success "   FFmpeg is already installed."
    }

    Write-Success "`nSetup complete! Launching application..."
    Start-Sleep -Seconds 1

} catch {
    Write-Error "`nSetup failed. Please check the error messages above."
    Write-Error "Common issues: No internet connection, firewall/antivirus blocking downloads, or insufficient permissions."
    # Хвърляме грешката отново, за да може .bat файлът да я хване
    throw
}