import QtQuick 2.4
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.2

Item {

    property alias treeView: treeView
    property alias tableViewColumn: tableViewColumn

    anchors.fill: parent

    implicitHeight: parent.height
    implicitWidth: parent.width
    TreeView {

        implicitHeight: parent.height
        implicitWidth: parent.width
        id: treeView
        anchors.fill: parent

        //clip: true

        TableViewColumn {
            id: tableViewColumn
            title: "Name"
            width: parent.width
            visible: false

        }

    }


}
