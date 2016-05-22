import QtQuick 2.4
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.1
import Qt.labs.settings 1.0

WriteRightBaseForm {
    orientation: Qt.RightEdge
    dockList: [writeRightDock1, writeRightDock2, writeRightDock3]

    ColumnLayout {
        id: columnLayout
        anchors.fill: parent

        WriteRightDock {
            id: writeRightDock1
            Layout.fillHeight: true
            Layout.fillWidth: true
            onAddDockClicked: setOneDockVisible()
            onCloseDockClicked: closeDock(writeRightDock1)
        }
        WriteRightDock {
            id: writeRightDock2
            Layout.fillHeight: true
            Layout.fillWidth: true
            onAddDockClicked: setOneDockVisible()
            onCloseDockClicked: closeDock(writeRightDock2)
        }
        WriteRightDock {
            id: writeRightDock3
            Layout.fillHeight: true
            Layout.fillWidth: true
            onAddDockClicked: setOneDockVisible()
            onCloseDockClicked: closeDock(writeRightDock3)
        }
    }



    Settings {
        id: settings
        property int write_right_base_width: baseItem.implicitWidth
    }

    function readSettings(){
        baseWidthChanged(settings.write_right_base_width)
    }
    function saveSettings(){
        settings.write_right_base_width = baseItem.implicitWidth
    }

    Component.onDestruction: saveSettings()

    Component.onCompleted: readSettings()


}
