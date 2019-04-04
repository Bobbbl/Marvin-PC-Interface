import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.5

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

    RowLayout{
        id: mainlayout
        anchors.fill: parent
        spacing: 2

        /*Linkes Layout*/
        ColumnLayout{
            id: leftlayout
            spacing: 2
            anchors.top: parent.top
            anchors.bottom: parent.bottom

            /*Steuerkreuz*/
            GridLayout{
                id: steuerkreuz
                anchors.top: parent.top
                //anchors.fill: parent
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
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                text: "Send Toolpath"
            }


        }

        /*Rechtes Layout*/

    }

}
