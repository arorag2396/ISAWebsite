VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "Sheet3"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Sub Send_Row()
'For Tips see: http://www.rondebruin.nl/win/winmail/Outlook/tips.htm
'Don't forget to copy the function RangetoHTML in the module.
'Working in Excel 2000-2016
    Dim OutApp As Object
    Dim OutMail As Object
    Dim cell As Range
    Dim rng As Range
    Dim Ash As Worksheet

    Set Ash = ActiveSheet
    On Error GoTo cleanup
    Set OutApp = CreateObject("Outlook.Application")

    With Application
        .EnableEvents = False
        .ScreenUpdating = False
    End With

    For Each cell In Ash.Columns("B").Cells.SpecialCells(xlCellTypeConstants)
        If cell.Value Like "?*@?*.?*" Then
           'And LCase(cell.Offset(0, 1).Value) = "yes" Then

            'Change the filter range and filter Field if needed
            'It will filter on Column B now (mail addresses)
            Ash.Range("A1:J100").AutoFilter Field:=2, Criteria1:=cell.Value

            With Ash.AutoFilter.Range
                On Error Resume Next
                Set rng = .SpecialCells(xlCellTypeVisible)
                On Error GoTo 0
            End With

            Set OutMail = OutApp.CreateItem(0)

            On Error Resume Next
            With OutMail
                .To = cell.Value
                .Subject = "Grades Aug"
                .HTMLBody = cell.Offset(0, 2).Value
                .Display  'Or use .Send
            End With
            On Error GoTo 0

            Set OutMail = Nothing
            Ash.AutoFilterMode = False
        End If
    Next cell

cleanup:
    Set OutApp = Nothing
    With Application
        .EnableEvents = True
        .ScreenUpdating = True
    End With
End Sub

