Get-ChildItem -Filter *.mp4 # mp4 files as example
$filesWithPattern = Get-ChildItem -Filter *.mp4 | Where-Object { $_.Name -match ' \[Optimum quality and size\]' } # pattern in original filename that must be removed: " [Optimum quality and size]"
#
$filesWithPattern | ForEach-Object {
    $newName = $_.Name -replace ' \[Optimum quality and size\]', ''
    $newFullPath = Join-Path $_.DirectoryName $newName
    Rename-Item -LiteralPath $_.FullName -NewName $newFullPath
    Write-Host "Renamed: $($_.FullName) to $newFullPath"
}
# End of File 
