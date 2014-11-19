' This sample demonstrates how to export data from Scatt file to CSV
' Copyright (c) 2001 ZAO Scatt
' Adapted by I.Zliobaite 19.11.2014

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

' Trying to open the scatt file
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

outputFile.WriteLine "Shot number"
	& "The moment of shot"
	& "Shot result"
	& "Aiming time"
	& "Breach coordinate X (mm)"
	& "Breach coordinate Y (mm)"
	& "Average aiming point X (mm)"
	& "Average aiming point Y (mm)"
	& "Steadiness in 10.0 (%)"
	& "Steadiness in 10a0 (%)"
	& "Trace length (mm)"
	& "Distance between breach and AAP"

' Store all match shots in a variable AllShots
'
Dim AllShots
Set AllShots = doc.Aimings.Match.Shots

' Iterate through all shots in a collection.
'
Dim i
For i = 1 To AllShots.Count
	' Store next shot in a variable CurrentShot
	'
	Dim CurrentShot
	Set CurrentShot = AllShots(i)

	' Get part of the trace - one second before the shot
	dim TestRange
	Set TestRange = CurrentShot.Range(-1,0)

	' Average aiming point
	dim AverageX, AverageY
	AverageX = TestRange.AveragePointX
	AverageY = TestRange.AveragePointY

	' Steadiness in 10.0 (center of the target)
	Dim Targ
	Set Targ = CurrentShot.Attr.Event.Target(CurrentShot.Attr.SubTarget)

	Dim Radius10
	Radius10 = Targ.Ring(10) / 2 + CurrentShot.Attr.Event.Caliber / 2

	' Distance between breach and AAP
	Dim dx, dy
	dx = CurrentShot.BreachX - AverageX
	dy = CurrentShot.BreachY - AverageY


	' store data
	'
	outputFile.WriteLine i 
			& CurrentShot.ShotTime
			& CurrentShot.Result
			& CurrentShot.ShotTime - CurrentShot.Attr.EnterTime
			& CurrentShot.BreachX
			& - CurrentShot.BreachY
			& AverageX
			& - AverageY
			& TestRange.Steadiness(Radius10, CurrentShot.Attr.FCoefficient, 0, 0)
			& TestRange.Steadiness(Radius10, CurrentShot.Attr.FCoefficient, AverageX, AverageY)
			& TestRange.Length
			& Sqr(dx*dx + dy*dy)
Next