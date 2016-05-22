import QtQuick 2.4

DockTitleBarForm {
    anchors.fill: parent

    property alias listModel: listModel

    ListModel {
        id: listModel
        ListElement{
            text: "Text"
            index: 0}
    }

    function init(){
    dock_comboBox.textRole = "text"
    dock_comboBox.model = listModel
    //dock_comboBox.onCurrentIndexChanged: console.debug(listModel.get(dock_comboBox.currentIndex).index)
}

    Component.onCompleted: init()
}
