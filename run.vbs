Set WshShell = CreateObject("WScript.Shell") 
WshShell.Run chr(34) & "run-all.bat" & Chr(34), 0
Set WshShell = Nothing