import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Dialogs 1.2
import QtQuick.Layouts 1.1
import QtQuick.Controls.Styles 1.4
import Qt.labs.settings 1.0
import "singletons" 1.0


ApplicationWindow {
    id: window
    visible: true
    title: "Plume Creator"
    width: 800
    height: 600

    Settings {
        property alias x: window.x
        property alias y: window.y
        property alias width: window.width
        property alias height: window.height
    }


    menuBar: MenuBar {
        Menu {
            title: qsTr("File")
            MenuItem {
                text: qsTr("&Open")
                onTriggered: console.log("Open action triggered");
            }
            MenuItem {
                text: qsTr("Exit")
                onTriggered: Qt.quit();
            }
        }
    }

    toolBar: ToolBar {
        RowLayout {
                    anchors.fill: parent
                    ToolButton {
                        text: "Open testproject"
                        iconSource: "new.png"
                    }
                    ToolButton {
                        text: "save"
                        iconSource: "open.png"
                    }
//                    Item { Layout.fillWidth: true }
//                    CheckBox {
//                        text: "Enabled"
//                        checked: true
//                        Layout.alignment: Qt.AlignRight
//                    }
        }
    }

    statusBar: StatusBar {
        RowLayout {
            anchors.fill: parent
            Label { text: "Read Only" }
        }
    }
    MainForm {

   }


    MessageDialog {
        id: messageDialog
        title: qsTr("May I have your attention, please?")

        function show(caption) {
            messageDialog.text = caption;
            messageDialog.open();
        }
    }

    Connections {
    target: SignalHub
    onOpenSheetInWritePageSignal: console.debug(sheet_id)
    }


}

