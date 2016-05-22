import QtQuick 2.4
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.1
import Qt.labs.settings 1.0

WriteLeftBaseForm {
    orientation: Qt.LeftEdge
    dockList: [writeLeftDock1, writeLeftDock2, writeLeftDock3]

    ColumnLayout {
        id: columnLayout
        anchors.fill: parent

        WriteLeftDock {
            id: writeLeftDock1
            Layout.fillHeight: true
            Layout.fillWidth: true
            onAddDockClicked: setOneDockVisible()
            onCloseDockClicked: closeDock(writeLeftDock1)
        }
        WriteLeftDock {
            id: writeLeftDock2
            Layout.fillHeight: true
            Layout.fillWidth: true
            onAddDockClicked: setOneDockVisible()
            onCloseDockClicked: closeDock(writeLeftDock2)
        }
        WriteLeftDock {
            id: writeLeftDock3
            Layout.fillHeight: true
            Layout.fillWidth: true
            onAddDockClicked: setOneDockVisible()
            onCloseDockClicked: closeDock(writeLeftDock3)
        }
    }




    Settings {
        id: settings
        property int write_left_base_width: baseItem.implicitWidth
//        property alias writeLeftDock1_combobox: writeLeftDock1.dockTitleBar.dock_comboBox.currentIndex
//        property alias writeLeftDock2_combobox: writeLeftDock2.dockTitleBar.dock_comboBox.currentIndex
//        property alias writeLeftDock3_combobox: writeLeftDock3.dockTitleBar.dock_comboBox.currentIndex
    }

    function readSettings(){
        baseWidthChanged(settings.write_left_base_width)

    }
    function saveSettings(){
        settings.write_left_base_width = baseItem.implicitWidth
    }

    Component.onDestruction: saveSettings()

    Component.onCompleted: readSettings()


}
