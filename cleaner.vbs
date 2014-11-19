' Copyright (c) 2002 ZAO Scatt

on error resume next

Sub QuitWithError(msg, retval)
	WScript.Echo msg
	WScript.Quit retval
End Sub

Function ValidShot(shot)
        ValidShot = False

	dim TestRange
	Set TestRange = shot.Range(0, 0)

	If Abs(TestRange.Index2Sec(TestRange.First)) <= 0.2 Then
		' trace too short
		Exit Function
	End If

	Dim r
	r = (shot.Attr.Event.Target(shot.Attr.SubTarget).FormWidth / 2) ^ 2

	Dim i
	For i = TestRange.First to 0
		Dim tr
		tr = TestRange.x(i) ^ 2 + TestRange.y(i) ^ 2

		If tr <= r Then
			' at least one point inside target
			ValidShot = True
			Exit Function
		End If
	Next

	' not inside target - invalid shot
End Function
    
Sub ValidateDocument(filename)
	Dim doc
	Set doc = CreateObject("ScattDoc.ScattDocument")
	if doc Is Nothing then QuitWithError "Error: Scatt Professional was not installed properly.", 1

	doc.FileName = filename
	doc.Load
	If Not doc.Valid Then
		WScript.Echo filename & ": FAILED"
		Exit Sub
	End If

	Dim Modified
	Modified = 0

	Dim AllShots
	Set AllShots = doc.Aimings.Shots

	Dim i
	For i = 1 To AllShots.Count
	        Dim CurrentShot
        	Set CurrentShot = AllShots(i)

		If Not ValidShot(CurrentShot) Then
			CurrentShot.Hidden = True
			Modified = Modified + 1
		End If
	Next

	If Modified > 0 Then 
		doc.Save
		WScript.Echo filename & ": " & CStr(Modified) & " shots removed"
	Else
		WScript.Echo filename & ": ok"
	End If
End Sub


Set objArgs = WScript.Arguments
If objArgs.Count > 0 Then
        Dim i
	For i = 0 to objArgs.Count - 1
		ValidateDocument(objArgs(i))
	Next	
Else
	dim fso
	set fso = CreateObject("Scripting.FileSystemObject")

	set folder = fso.GetFolder(".")

	for each file in folder.files
	        ValidateDocument(file)
	next
End If
