' This sample demonstrates how to extract x and y coordinates
' from Scatt file
' Copyright (c) 2002 ZAO Scatt

on error resume next

Sub QuitWithError(msg, retval)
	WScript.Echo msg
	WScript.Quit retval
End Sub

' Did user specified file name?
'
Set objArgs = WScript.Arguments
if objArgs.Count < 1 then QuitWithError "Usage: SAMPLES filename.scatt output.txt", 1

' Creating instance of the ScattDoc object, through which we will access
' data. Scatt Professional application has to be installed.
'
Dim doc
Set doc = CreateObject("ScattDoc.ScattDocument")
if doc Is Nothing then QuitWithError "Error: Scatt Professional was not installed properly.", 1

' Specify the name of the Scatt file
'
doc.FileName = objArgs(0)

' Trying to open the file
'
doc.Load
if Not doc.Valid then QuitWithError "Error: File not found or invalid file format.", 1

' Open file for output
'
Dim outputFileName
if objArgs.Count = 1 then outputFileName = objArgs(0) & ".txt" else outputFileName = objArgs(1)

Dim fso, outputFile
Set fso = CreateObject("Scripting.FileSystemObject")
Set outputFile = fso.CreateTextFile(outputFileName, True)
if Err.Number <> 0 then QuitWithError "Error: Can't create output file " & objArgs(1)

' Store all match shots in a variable AllShots
'
Dim AllShots
Set AllShots = doc.Aimings.Match.Shots
if AllShots.Count = 0 then QuitWithError "Error: No match shots"

' Writing information about file
'
outputFile.WriteLine doc.Event.Name & " (" & doc.Event.ShortName & ")"
outputFile.WriteLine AllShots(1).ShotTime
outputFile.WriteLine doc.ShooterName
outputFile.WriteLine doc("_comments")
outputFile.WriteLine

' Iterate through all shots in a collection.
'
Dim i
For i = 1 To AllShots.Count
	outputFile.WriteLine "Shot #" & CStr(i)

	' Store next shot in a variable CurrentShot
	'
	Dim CurrentShot
	Set CurrentShot = AllShots(i)

	' Get part of the trace - one second before the shot, 0.5 after
	dim TestRange
	Set TestRange = CurrentShot.Range(-1, 0.5)

	Dim j
	For j = TestRange.First to TestRange.Last
		outputFile.WriteLine FormatNumber(TestRange.Index2Sec(j), 3) _
			& " x=" & FormatNumber(TestRange.X(j), 2) _
                        & " y=" & FormatNumber(TestRange.Y(j), 2)
	Next

	outputFile.WriteLine
Next
