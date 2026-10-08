$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$source = Join-Path $projectRoot 'dashboard\Dashboard.pbix'
$output = Join-Path $projectRoot 'dashboard\Dashboard_Custom.pbix'
$work = Join-Path $projectRoot '.pbix_customize'

if (Test-Path -LiteralPath $work) {
    Remove-Item -LiteralPath $work -Recurse -Force
}
Expand-Archive -LiteralPath $source -DestinationPath $work -Force

$pageDir = Join-Path $work 'Report\definition\pages\26f15efa213e2c3971bb'
$pagePath = Join-Path $pageDir 'page.json'
$page = Get-Content -Raw -LiteralPath $pagePath
$page = $page.Replace('"displayName":"Page 1"', '"displayName":"Tổng quan • Netflix Content"')
$page = $page.Replace("'#FAFAFA'", "'#F7F9FC'")
[System.IO.File]::WriteAllText($pagePath, $page, [System.Text.UTF8Encoding]::new($false))

$shapePath = Join-Path $pageDir 'visuals\5298a3dbafbc078acf9a\visual.json'
$shape = Get-Content -Raw -LiteralPath $shapePath
$shape = $shape.Replace("'#FF0000'", "'#0F172A'")
[System.IO.File]::WriteAllText($shapePath, $shape, [System.Text.UTF8Encoding]::new($false))

$headerPath = Join-Path $pageDir 'visuals\1a1be13387a2bba7f847\visual.json'
$header = Get-Content -Raw -LiteralPath $headerPath
$header = $header.Replace('Netflix mở rộng thư viện rất mạnh từ 2016, đạt mức bổ sung cao nhất vào 2019. Movie vẫn chiếm đa số nhưng TV Show tăng nhanh trong giai đoạn cuối.', 'NETFLIX CONTENT DASHBOARD\nTổng quan thư viện nội dung, phân bổ và xu hướng bổ sung')
$header = $header.Replace('"fontSize":"28pt"', '"fontSize":"24pt"')
[System.IO.File]::WriteAllText($headerPath, $header, [System.Text.UTF8Encoding]::new($false))

$cardIds = @(
    '3dc6a7e37e65c6445f38',
    'c3a92c256c70956e3e22',
    '337ee86df5f8900e95fb',
    '5a2dd6308a6340a24108',
    '6688a432a7b01129e801'
)
foreach ($id in $cardIds) {
    $path = Join-Path $pageDir ("visuals\$id\visual.json")
    $s = Get-Content -Raw -LiteralPath $path
    $s = $s.Replace("'#120000'", "'#FFFFFF'")
    $q = [char]39
    $fontOld = '"fontColor":{"solid":{"color":{"expr":{"Literal":{"Value":"' + $q + '#FFFFFF' + $q + '"}}}}}'
    $fontNew = '"fontColor":{"solid":{"color":{"expr":{"Literal":{"Value":"' + $q + '#0F172A' + $q + '"}}}}}'
    $lineOld = '"lineColor":{"solid":{"color":{"expr":{"Literal":{"Value":"' + $q + '#FFFFFF' + $q + '"}}}}}'
    $lineNew = '"lineColor":{"solid":{"color":{"expr":{"Literal":{"Value":"' + $q + '#D8E4F2' + $q + '"}}}}}'
    $s = $s.Replace($fontOld, $fontNew)
    $s = $s.Replace($lineOld, $lineNew)
    $s = $s.Replace('"show":{"expr":{"Literal":{"Value":"false"}}}', '"show":{"expr":{"Literal":{"Value":"true"}}}')
    [System.IO.File]::WriteAllText($path, $s, [System.Text.UTF8Encoding]::new($false))
}

$titleUpdates = @{
    '85907bdce5bcd53f7d85' = 'Nội dung theo năm phát hành và loại hình'
    '5e3ca2b9b055ba080a7c' = 'Top 10 thể loại phổ biến'
    '145fcdfd633a7d51e188' = 'Xu hướng bổ sung nội dung theo năm'
}
foreach ($item in $titleUpdates.GetEnumerator()) {
    $path = Join-Path $pageDir ("visuals\$($item.Key)\visual.json")
    $s = Get-Content -Raw -LiteralPath $path
    $s = [regex]::Replace($s, '("text":\{"expr":\{"Literal":\{"Value":"\x27)[^\x27]*(\x27"\}\}\})', ('$1' + $item.Value + '$2'), 1)
    [System.IO.File]::WriteAllText($path, $s, [System.Text.UTF8Encoding]::new($false))
}

if (Test-Path -LiteralPath $output) {
    Remove-Item -LiteralPath $output -Force
}
$tempOutput = "$output.tmp"
if (Test-Path -LiteralPath $tempOutput) {
    Remove-Item -LiteralPath $tempOutput -Force
}
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
$sourceStream = [System.IO.File]::OpenRead($source)
$sourceZip = [System.IO.Compression.ZipArchive]::new($sourceStream, [System.IO.Compression.ZipArchiveMode]::Read)
$targetStream = [System.IO.File]::Open($tempOutput, [System.IO.FileMode]::CreateNew)
$targetZip = [System.IO.Compression.ZipArchive]::new($targetStream, [System.IO.Compression.ZipArchiveMode]::Create)
foreach ($entry in $sourceZip.Entries) {
    $sourceFile = Join-Path $work ($entry.FullName -replace '/', '\')
    if (-not (Test-Path -LiteralPath $sourceFile -PathType Leaf)) {
        continue
    }
    $level = if ($entry.FullName -eq 'DataModel') { [System.IO.Compression.CompressionLevel]::NoCompression } else { [System.IO.Compression.CompressionLevel]::Optimal }
    $newEntry = $targetZip.CreateEntry($entry.FullName, $level)
    $inStream = [System.IO.File]::OpenRead($sourceFile)
    $outStream = $newEntry.Open()
    $inStream.CopyTo($outStream)
    $outStream.Dispose()
    $inStream.Dispose()
}
$targetZip.Dispose()
$targetStream.Dispose()
$sourceZip.Dispose()
$sourceStream.Dispose()
Move-Item -LiteralPath $tempOutput -Destination $output -Force
Remove-Item -LiteralPath $work -Recurse -Force
Write-Output $output
