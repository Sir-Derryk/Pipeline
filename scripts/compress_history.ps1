param (
    [switch]$PushToRemote = $false
)

$ErrorActionPreference = "Stop"

# Переходим в директорию скрипта
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  [UDE] STARTING INTEGRATED HISTORY COMPRESSION & CI/CD CLEANUP" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Root Directory: $scriptDir" -ForegroundColor DarkGray
if ($PushToRemote) {
    Write-Host "⚠️ WARNING: -PushToRemote is ENABLED. Changes will be force-pushed to GitHub!" -ForegroundColor Red
} else {
    Write-Host "ℹ️ Mode: LOCAL ONLY. No force-pushes will be performed." -ForegroundColor Green
}
Write-Host "`n⚠️ IMPORTANT: To allow force-pushing of compressed branches," -ForegroundColor Yellow
Write-Host "  you MUST temporarily deactivate Rulesets and Branch Protection Rules" -ForegroundColor Yellow
Write-Host "  on GitHub for the parent repository and all three submodules!" -ForegroundColor Yellow
Write-Host "======================================================================" -ForegroundColor Cyan

Write-Host "`nPress ENTER to proceed or Ctrl+C to abort..." -ForegroundColor DarkYellow
Read-Host | Out-Null

# Список репозиториев для обработки
$targets = @(
    [PSCustomObject]@{ Name = "engine";      Path = "..\engine";      Branch = "master"; Msg = "Initial commit (Universal Documentation Engine Core)" },
    [PSCustomObject]@{ Name = "user-docs";   Path = "..\user-docs";   Branch = "main";   Msg = "Initial commit (User and Admin Guides)" },
    [PSCustomObject]@{ Name = "design-docs"; Path = "..\design-docs"; Branch = "main";   Msg = "Initial commit (Design and SRS Documentation)" },
    [PSCustomObject]@{ Name = "Pipeline";    Path = "..";           Branch = "master"; Msg = "Initial commit (Universal Documentation Portal)" }
)

# Проверка окружения
Write-Host "🔍 [1/3] Checking prerequisites..." -ForegroundColor Yellow
$gitCheck = Get-Command git -ErrorAction SilentlyContinue
$ghCheck = Get-Command gh -ErrorAction SilentlyContinue

if (-not $gitCheck) {
    Write-Error "Git is not installed or not in system PATH."
}
if (-not $ghCheck) {
    Write-Warning "GitHub CLI (gh) is not installed. Workflow run deletion will be skipped."
}

# 1. Удаление логов запусков GitHub Actions (только если gh установлен и авторизован)
if ($ghCheck) {
    Write-Host "`n🧹 [2/3] Cleaning up GitHub Actions workflow runs..." -ForegroundColor Yellow
    foreach ($target in $targets) {
        $targetPath = Join-Path $scriptDir $target.Path
        if (Test-Path $targetPath) {
            Push-Location $targetPath
            try {
                Write-Host "👉 Checking workflow runs for '$($target.Name)'..." -ForegroundColor Cyan
                $runs = gh run list --limit 500 --json databaseId | ConvertFrom-Json
                if ($runs -and $runs.Count -gt 0) {
                    Write-Host "Found $($runs.Count) runs. Deleting..." -ForegroundColor DarkYellow
                    foreach ($run in $runs) {
                        gh run delete $run.databaseId | Out-Null
                    }
                    Write-Host "✅ Deleted workflow runs successfully." -ForegroundColor Green
                } else {
                    Write-Host "No runs found." -ForegroundColor Gray
                }
            } catch {
                Write-Warning "Failed to clear workflow runs for $($target.Name): $_"
            } finally {
                Pop-Location
            }
        }
    }
}

# 2. Локальное сжатие истории
Write-Host "`n📦 [3/3] Compressing repository histories to 1 commit..." -ForegroundColor Yellow

for ($i = 0; $i -lt $targets.Count; $i++) {
    $target = $targets[$i]
    $targetPath = Join-Path $scriptDir $target.Path
    
    if (-not (Test-Path $targetPath)) {
        Write-Warning "Path not found: $targetPath. Skipping."
        continue
    }

    Write-Host "`n--- Processing '$($target.Name)' (Branch: $($target.Branch)) ---" -ForegroundColor Cyan
    Push-Location $targetPath
    try {
        # Имя временной сиротской ветки
        $tempBranch = "temp_compress_" + (Get-Random)
        
        Write-Host "Creating orphan branch '$tempBranch'..." -ForegroundColor DarkGray
        git checkout --orphan $tempBranch | Out-Null

        Write-Host "Staging all files..." -ForegroundColor DarkGray
        git add -A | Out-Null
        
        Write-Host "Creating initial commit..." -ForegroundColor DarkGray
        git commit -m "$($target.Msg)" | Out-Null

        Write-Host "Updating local branch layout..." -ForegroundColor DarkGray
        $branches = git branch --list $target.Branch
        if ($branches) {
            git branch -D $target.Branch | Out-Null
        }
        git branch -m $target.Branch | Out-Null

        Write-Host "✅ '$($target.Name)' compressed successfully!" -ForegroundColor Green

        # Force push если передан флаг -PushToRemote
        if ($PushToRemote) {
            Write-Host "Pushing changes to remote..." -ForegroundColor Yellow
            git push -f origin $target.Branch
            Write-Host "🚀 Remote successfully updated!" -ForegroundColor Green
        } else {
            Write-Host "💡 To push changes manually, run: git push -f origin $($target.Branch)" -ForegroundColor DarkYellow
        }
    } catch {
        Write-Error "Failed to process $($target.Name): $_"
    } finally {
        Pop-Location
    }
}

Write-Host "`n======================================================================" -ForegroundColor Green
Write-Host "  SUCCESS: Compression process complete!" -ForegroundColor Green
if (-not $PushToRemote) {
    Write-Host "  To push all changes to GitHub, run the script with: -PushToRemote" -ForegroundColor Green
}
Write-Host "======================================================================" -ForegroundColor Green
