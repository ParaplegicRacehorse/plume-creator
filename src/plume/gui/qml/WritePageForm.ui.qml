import QtQuick 2.4
import QtQuick.Layouts 1.2
import QtQuick.Controls 1.4

Item {
    property alias leftBase: leftBase
    property alias rightBase: rightBase
    property alias rectangle3: rectangle3
    anchors.fill: parent



    RowLayout {
        id: leftRowLayout
        anchors.fill: parent

        WriteLeftBase {
            id: leftBase
            implicitWidth: 200
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.minimumHeight: 100
            Layout.minimumWidth: 130
            Layout.rowSpan: 2
        }

        ColumnLayout {
            id: bottomColumnLayout
            width: 100
            height: 100


            RowLayout {
                id: rightRowLayout
                width: 100
                height: 100

                Item {
                    id: item1
                    width: 200
                    height: 200
                    Layout.fillHeight: true
                    Layout.fillWidth: true

                    Rectangle {
                        id: rectangle3
                        color: "#ffffff"
                        anchors.fill: parent
                    }
                }

                WriteRightBase {
                    id: rightBase
                    implicitWidth: 200
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                    Layout.minimumHeight: 100
                    Layout.minimumWidth: 130
                    Layout.rowSpan: 2
                }

            }

            Rectangle {
                id: rectangle2
                width: 200
                height: 200
                color: "#ffffff"
                Layout.fillHeight: true
                Layout.fillWidth: true
            }
        }

    }
}
