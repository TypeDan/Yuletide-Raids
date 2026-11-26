param([Parameter(Mandatory=$true)][string]$ArchivePath,[Parameter(Mandatory=$true)][string]$EssenceLibrary)
$ErrorActionPreference='Stop'
Add-Type -Path $EssenceLibrary
$sourceRoot=Split-Path -Parent $PSScriptRoot
$stream=[IO.File]::OpenRead((Resolve-Path -LiteralPath $ArchivePath).Path)
try {
 $archive=[AOEMods.Essence.SGA.Graph.Archive]::FromStream($stream)
 $entries=@{}
 function ReadEntries($node,[string]$prefix) {
  $relative=if($prefix){"$prefix/$($node.Name)"}else{$node.Name}
  if($node -is [AOEMods.Essence.SGA.Graph.ArchiveFolderNode]){foreach($child in $node.Children){ReadEntries $child $relative}}
  else{$entries[$relative]=[byte[]]@($node.GetData())}
 }
 foreach($toc in $archive.Tocs){ReadEntries $toc.RootFolder ''}
 if(-not $entries.ContainsKey('mod.bin')){throw 'Missing mod metadata'}
 foreach($key in $entries.Keys){
  if($key -match '\.scar$'){
   if([Text.Encoding]::UTF8.GetString($entries[$key]) -match 'YULE_NOV25_PROBE|SANTA_DELIVERY_PROBE|YULE_DELIVERY_PROBE|YuleDeliveryProbe'){throw "Diagnostic code in $key"}
   $source=Join-Path $sourceRoot "assets/$key"
   if(-not(Test-Path -LiteralPath $source)){throw "Missing source for $key"}
   $expected=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData([IO.File]::ReadAllBytes($source)))
   $actual=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($entries[$key]))
   if($expected -ne $actual){throw "Source/archive mismatch: $key"}
  }
 }
 if(-not $entries.ContainsKey('scar/christmas/yuletide_settings.scar')){throw 'Missing lobby settings script'}
 Write-Output "PASS: $($entries.Count) archive entries; metadata and lobby script present; all Lua scripts match source; diagnostic markers absent."
 Get-FileHash -LiteralPath $ArchivePath
}finally{$stream.Dispose()}
