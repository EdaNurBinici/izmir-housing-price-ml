# Train model script for Windows

Write-Host "Training model..." -ForegroundColor Green
python model_egitim.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nModel training completed successfully!" -ForegroundColor Green
} else {
    Write-Host "`nModel training failed!" -ForegroundColor Red
    exit 1
}
