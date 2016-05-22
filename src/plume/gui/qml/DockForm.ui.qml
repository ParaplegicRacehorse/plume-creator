import QtQuick 2.4
import QtQuick.Layouts 1.2
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4

Item {
    id: item
    property alias dockTitleBar: dockTitleBar
    property alias tabView: tabView
    property alias baseRectangle1: baseRectangle1
    property alias baseItem: item
    property alias item2: item2

    Rectangle {
        id: baseRectangle1
        color: "#ffffff"
        anchors.fill: parent
        implicitHeight: parent.height
        implicitWidth: parent.width

        ColumnLayout {
            id: columnLayout1
            anchors.fill: parent
            implicitHeight: parent.height
            implicitWidth: parent.width
            spacing: 0




            DockTitleBar {
                id: dockTitleBar
                Layout.minimumHeight: 25
                Layout.maximumHeight: 25
                Layout.minimumWidth: 10
                Layout.fillHeight: true
                Layout.fillWidth: true
            }
            Item {
                id: item2
                Layout.fillHeight: true
                Layout.fillWidth: true
                implicitHeight: parent.height
                implicitWidth: parent.width


                TabView {
                    id: tabView
                    width: baseRectangle1.width
                    anchors.fill: parent
                    style: TabViewStyle {
                        tab: Item {}
                    }

                }


            }
        }

    }
}
