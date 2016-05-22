import QtQuick 2.4
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.1

Item {
    id: baseItem
    property alias columnLayout: columnLayout
    property alias sizeHandle: sizeHandle
    property alias handleMouseArea: handleMouseArea
    property alias base: base
    property alias baseItem: baseItem
    Rectangle{
        id: base
        anchors.fill: parent


        ColumnLayout {
            id: columnLayout
            anchors.fill: parent

            // populate docks here

        }

        Rectangle {
            id: sizeHandle
            width: 6
            color: 'red' //"#ffffff"

            MouseArea {
                id: handleMouseArea
                hoverEnabled: true
                anchors.fill: parent
            }
        }
    }

}
