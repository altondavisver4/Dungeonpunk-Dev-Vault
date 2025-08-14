Param(
  [string]$Category = "MECHANIC",
  [string]$Slug = "Short-Slug",
  [int]$Version = 1,
  [string]$Folder = "."
)

$Date = Get-Date -Format "yyyy-MM-dd"
$Name = "{0}_{1}_{2}_v{3}.md" -f $Date, $Category, $Slug, $Version
$Path = Join-Path $Folder $Name

$Content = @"
---
tags: []
status: working
hot: false
summary: ""
---

# $Category — $Slug (v$Version)

(Write here)
"@

Set-Content -Path $Path -Value $Content -Encoding UTF8
Write-Host "Created $Path"
