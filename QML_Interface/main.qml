import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.5
import QtQuick.Dialogs 1.0

Page {
    id: window
    visible: true
    width: 640
    height: 300
    title: qsTr("Hello World")


    signal upbutton_pressed;
    signal downbutton_pressed;
    signal leftbutton_pressed;
    signal rightbutton_pressed;
    signal stopbutton_pressed;
    signal sendtoolpathbutton_pressed(string path);
    signal portChanged(string name);
    signal connectbutton_pressed;

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

            FileDialog{
                id: filedialog
                title: "Chose A Toolpath File"
                onAccepted: {

                    sendtoolpathbutton_pressed(this.fileUrl)
                }
            }

            RowLayout {
                id: rowLayout
                width: 100
                height: 100

                Button {
                    id: spindelbutton
                    text: qsTr("Spindel")
                }

                TextEdit {
                    id: spindeltext

                    Layout.fillWidth: true
                    text: qsTr("0")
                    horizontalAlignment: Text.AlignRight
                    font.pixelSize: 12
                }
            }



        } // End Left Layout

        Column{
            spacing: 2
            Layout.column: 1
            anchors.right: window.right

            RowLayout{

                spacing: 5
                ComboBox{
                    id: portsspinbox
                    model: Interface.pList

                    onCurrentTextChanged: portChanged(portsspinbox.currentText)
                }

                Button{
                    id: connectbutton
                    text: "Connect"
                    onClicked: connectbutton_pressed()
                }

            }

            TextEdit {
                id: textEdit

                text: qsTr("- - -")
                font.pixelSize: 12

                anchors.left: portsspinbox.left
                anchors.right: window.right

            }
        }

    }

    // End MainLayout (Row)

}
