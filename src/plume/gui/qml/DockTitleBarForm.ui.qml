import QtQuick 2.4
import QtQuick.Layouts 1.2
import QtQuick.Controls 1.4

Item {
    id: item3
    property alias close_toolButton: close_toolButton
    property alias add_toolButton: add_toolButton
    property alias dock_comboBox: dock_comboBox
    implicitHeight: 25

    Rectangle {
        id: rectangle1
        color: "#ffffff"
        anchors.fill: parent

        RowLayout {
            id: rowLayout2
            anchors.fill: parent
            spacing: 0


            ComboBox {
                id: dock_comboBox
                Layout.fillHeight: true
                Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                Layout.maximumHeight: 24
                Layout.minimumWidth: 90
                Layout.maximumWidth: 150
                model:    ListModel {}
            }

            Stretcher {
                id: stretcher1
                Layout.fillWidth: true
                Layout.minimumWidth: 4
                Layout.maximumWidth: 200
                Layout.preferredWidth: 300
                anchors.fill: parent
            }

            Item {
                id: item2
                Layout.minimumWidth: 1
                Layout.fillHeight: true
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter

                ToolButton {
                    id: close_toolButton
                    x: 138
                    width: 20
                    height: 20
                    anchors.top: parent.top
                    anchors.topMargin: 4
                    anchors.right: parent.right
                    anchors.rightMargin: 4
                    iconSource: "pics/32x32/window-close.png"
                    Layout.alignment: Qt.AlignRight | Qt.AlignTop
                }

                ToolButton {
                    id: add_toolButton
                    x: 104
                    width: 20
                    height: 20
                    iconSource: "pics/32x32/list-add.png"
                    anchors.right: parent.right
                    anchors.rightMargin: 38
                    anchors.top: parent.top
                    anchors.topMargin: 4
                    Layout.fillWidth: false
                    Layout.alignment: Qt.AlignRight | Qt.AlignTop
                }
            }


        }
    }
}
