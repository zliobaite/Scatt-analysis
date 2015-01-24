' This sample demonstrates how to export data from Scatt file to Microsoft
' Excel application.
' Copyright (c) 2001 ZAO Scatt

on error resume next

Sub QuitWithError(msg, retval)
	WScript.Echo msg
	WScript.Quit retval
End Sub

' Did user specified file name?
'
Set objArgs = WScript.Arguments
if objArgs.Count <> 1 then QuitWithError "Usage: SCATTEXP filename.scatt", 1

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

' Creating instance of the Excel application.
'
Dim xlApp
Set xlApp = CreateObject("Excel.Application")
if xlApp Is Nothing then QuitWithError "Error: Unable to create instance of Excel Application.", 1

' Add new blank workbook
'
Dim Sheet
xlApp.Workbooks.Add
Set Sheet = xlApp.ActiveSheet

' fill the titles of rows
'
With Sheet
	.Cells(1, 1).Value = "Shot number"
	.Cells(2, 1).Value = "The moment of shot"
	.Cells(3, 1).Value = "Shot result"
	.Cells(4, 1).Value = "Aiming time"
	.Cells(5, 1).Value = "Breach coordinate X (mm)"
	.Cells(6, 1).Value = "Breach coordinate Y (mm)"
	.Cells(7, 1).Value = "Average aiming point X (mm)"
	.Cells(8, 1).Value = "Average aiming point Y (mm)"
	.Cells(9, 1).Value = "Steadiness in 10.0 (%)"
	.Cells(10, 1).Value = "Steadiness in 10a0 (%)"
	.Cells(11, 1).Value = "Trace length (mm)"
	.Cells(12, 1).Value = "Distance between breach and AAP"
	.Cells(13, 1).Value = "Pulse rate"

	.Columns("A:A").EntireColumn.AutoFit
End With

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

	' store data of shot in corresponding cell of active sheet.
	'
	' Shot number
	Sheet.Cells(1, i + 1).Value = i

	' The moment of shot
	Sheet.Cells(2, i + 1).Value = CurrentShot.ShotTime
	if i = 1 then
		Sheet.Cells(2, i + 1).NumberFormat = "dd/mm/yy h:mm;@"
	Else
		Sheet.Cells(2, i + 1).NumberFormat = "h:mm:ss;@"
	End If

	' Shot result
	Sheet.Cells(3, i + 1).Value = CurrentShot.Result
        Sheet.Cells(3, i + 1).NumberFormat = "0.0"

	' Aiming time
	Sheet.Cells(4, i + 1).Value = CurrentShot.ShotTime - CurrentShot.Attr.EnterTime
        Sheet.Cells(4, i + 1).NumberFormat = "[h]:mm:ss.0;@"
                 
	' Breach coordinates
	Sheet.Cells(5, i + 1).Value = CurrentShot.BreachX
        Sheet.Cells(5, i + 1).NumberFormat = "0.00"
	Sheet.Cells(6, i + 1).Value = - CurrentShot.BreachY
        Sheet.Cells(6, i + 1).NumberFormat = "0.00"

	' Get part of the trace - one second before the shot
	dim TestRange
	Set TestRange = CurrentShot.Range(-1,0)

	' Average aiming point
	dim AverageX, AverageY
	AverageX = TestRange.AveragePointX
	AverageY = TestRange.AveragePointY
	Sheet.Cells(7, i + 1).Value = AverageX
        Sheet.Cells(7, i + 1).NumberFormat = "0.00"
	Sheet.Cells(8, i + 1).Value = - AverageY
        Sheet.Cells(8, i + 1).NumberFormat = "0.00"

	' Steadiness in 10.0 (center of the target)
	Dim Targ
	Set Targ = CurrentShot.Attr.Event.Target(CurrentShot.Attr.SubTarget)

	Dim Radius10
	Radius10 = Targ.Ring(10) / 2 + CurrentShot.Attr.Event.Caliber / 2
	Sheet.Cells(9, i + 1).Value = TestRange.Steadiness(Radius10, CurrentShot.Attr.FCoefficient, 0, 0)

	' Steadiness in 10.0
	Sheet.Cells(10, i + 1).Value = TestRange.Steadiness(Radius10, CurrentShot.Attr.FCoefficient, AverageX, AverageY)
        Sheet.Cells(3, i + 1).NumberFormat = "0.0"

	' Trace length
	Sheet.Cells(11, i + 1).Value = TestRange.Length
        Sheet.Cells(11, i + 1).NumberFormat = "0.0"

        ' Distance between breach and AAP
        Dim dx, dy
        dx = CurrentShot.BreachX - AverageX
        dy = CurrentShot.BreachY - AverageY
	Sheet.Cells(12, i + 1).Value = Sqr(dx*dx + dy*dy)
        Sheet.Cells(12, i + 1).NumberFormat = "0.0"

        ' Pulse rate
	Sheet.Cells(13, i + 1).Value = CurrentShot("_pulse")
        Sheet.Cells(13, i + 1).NumberFormat = "0.0"
Next

' Make Excel visible
'
xlApp.Visible = True


Set xlApp = Nothing
