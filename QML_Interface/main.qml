import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.5
import QtQuick.Dialogs 1.0

Page {
    id: window
    visible: true
    width: 640
    height: 400
    title: qsTr("Hello World")


    signal upbutton_pressed;
    signal downbutton_pressed;
    signal leftbutton_pressed;
    signal rightbutton_pressed;
    signal stopbutton_pressed;
    signal sendtoolpathbutton_pressed(string path);
    signal portChanged(string name);
    signal connectbutton_pressed;
    signal spindelbutton_pressed(string rpm);
    signal zbuttonactivated;
    signal zbuttoncanceld;

    Row{
        id: mainlayout
        //anchors.fill: parent
        spacing: 2

        /*Linkes Layout*/
        ColumnLayout{
            id: leftlayout
            Layout.row: 0
            spacing: 2

            /*Steuerkreuz*/
            GridLayout{
                id: steuerkreuz
                columns: 3
                rows: 3


                Button{
                    id: upbutton
                    Layout.column: 1
                    Layout.row: 0
                    text: "Up"


                    onClicked: upbutton_pressed()
                }

                Button{
                    id: leftbutton
                    Layout.column: 0
                    Layout.row: 1
                    text: "Left"

                    onClicked: leftbutton_pressed()
                }

                Button{
                    id: stopbutton
                    Layout.column: 1
                    Layout.row: 1
                    text: "Stop"

                    onClicked: stopbutton_pressed()
                }

                Button{
                    id: rightbutton
                    Layout.column: 2
                    Layout.row: 1
                    text: "Right"

                    onClicked: rightbutton_pressed()
                }

                Button{
                    id: downbutton
                    Layout.column: 1
                    Layout.row: 2
                    text: "Down"

                    onClicked: downbutton_pressed()
                }
            }

            /*Excel Button*/

            Button{
                id: toolpathbutton
                anchors.left: steuerkreuz.left
                anchors.right: steuerkreuz.right


                Layout.row: 1
                text: "Send Toolpath"

                onClicked:{


                    filedialog.open()

                }
            }

            ProgressBar {
                id: progressBar
                width: toolpathbutton.width
                height: 16
                value: ProgressInterface.pValue


            }

            FileDialog{
                id: filedialog
                title: "Chose A Toolpath File"
                onAccepted: {

                    sendtoolpathbutton_pressed(this.fileUrl)
                }
            }


            RowLayout {
                id: rowLayout
                //anchors.top: progressBar.bottom
                width: 100
                height: 100

                Button {
                    id: spindelbutton
                    text: qsTr("Spindel")
                    onClicked: {
                        spindelbutton_pressed(spindeltext.text)
                    }
                }

                TextEdit {
                    id: spindeltext

                    Layout.fillWidth: true
                    text: qsTr("0")
                    horizontalAlignment: Text.AlignRight
                    font.pixelSize: 12
                }
            }

            RowLayout {
                id: rowLayout2
                //anchors.top: rowLayout.bottom
                width: 100
                height: 100


                DelayButton {
                     id: zdelaybutton
                     checked: false
                     text: qsTr("Z")

                     onActivated: zbuttonactivated()
                     onActionChanged: zbuttoncanceld()


                     contentItem: Text {
                         text: zdelaybutton.text
                         font: zdelaybutton.font
                         opacity: enabled ? 1.0 : 0.3
                         color: "white"
                         horizontalAlignment: Text.AlignHCenter
                         verticalAlignment: Text.AlignVCenter
                         elide: Text.ElideRight
                     }

                     background: Rectangle {
                         implicitWidth: 50
                         implicitHeight: 50
                         opacity: enabled ? 1 : 0.3
                         color: zdelaybutton.down ? "#17a81a" : "#21be2b"
                         radius: size / 2

                         readonly property real size: Math.min(zdelaybutton.width, zdelaybutton.height)
                         width: size
                         height: size
                         anchors.centerIn: parent


                         Canvas {
                             id: canvas
                             anchors.fill: parent

                             Connections {
                                 target: zdelaybutton
                                 onProgressChanged: canvas.requestPaint()

                             }

                             onPaint: {
                                 var ctx = getContext("2d")
                                 ctx.clearRect(0, 0, width, height)
                                 ctx.strokeStyle = "white"
                                 ctx.lineWidth = parent.size / 20
                                 ctx.beginPath()
                                 var startAngle = Math.PI / 5 * 3
                                 var endAngle = startAngle + zdelaybutton.progress * Math.PI / 5 * 9
                                 ctx.arc(width / 2, height / 2, width / 2 - ctx.lineWidth / 2 - 2, startAngle, endAngle)
                                 ctx.stroke()
                             }
                         }
                     }
                 }


            }





        } // End Left Layout

        Column{
            id: rightlayout
            spacing: 2
            Layout.column: 1
            Layout.fillWidth: parent

            RowLayout{
                spacing: 5

                ComboBox{
                    id: portsspinbox
                    model: PortInterface.pList

                    onCurrentTextChanged: portChanged(portsspinbox.currentText)
                }

                Button{
                    id: connectbutton
                    text: "Connect"
                    onClicked: connectbutton_pressed()
                }

            }

            Frame {
                id: frame
                height: 160
                width: 320

                ScrollView{
                    x: -5
                    y: -6
                    height: 148
                    width: 306
                    anchors.right: window.right
                    TextArea {
                        id: logtext
                        x: -10
                        y: -6
                        width: 306
                        height: 128

                        wrapMode: TextEdit.Wrap
                        text: this.append(LogInterface.lastElement)

                        font.pixelSize: 9
                        Layout.fillWidth: rightlayout
                    }
                }
            }



        }


    }

    Connections {
        target: zdelaybutton
        onActionChanged: print("clicked")
    }

    // End MainLayout (Row)

}




















