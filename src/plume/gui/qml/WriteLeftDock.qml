import QtQuick 2.4
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.1
import QtQuick.Controls.Styles 1.4

WriteLeftDockForm {


    //    TabView {
    //        id: tabView
    //        width: baseRectangle1.width
    //        anchors.fill: parent
    //        style: TabViewStyle {
    //            tab: Item {}
    //        }
    //        Tab {
    //            id: tab1
    //            title: "Sheets"
    //            SheetTreePanel {
    //                Layout.fillHeight: true
    //                Layout.fillWidth: true
    //                implicitHeight: parent.height
    //                implicitWidth: parent.width
    //                id: sheetTreePanel
    //                anchors.fill: parent
    //                visible: true
    //            }
    //        }
    //        Tab {
    //            id: tab2
    //            title: "Wastebin"
    //            WastebinPanel {
    //                Layout.fillHeight: true
    //                Layout.fillWidth: true
    //                implicitHeight: parent.height
    //                implicitWidth: parent.width
    //                id: wastebinPanel
    //                anchors.fill: parent
    //                visible: true
    //            }
    //        }
    //    }
    Component{
        id: sheetTreePanelComponent
        SheetTreePanel {
            Layout.fillHeight: true
            Layout.fillWidth: true
            implicitHeight: parent.height
            implicitWidth: parent.width
            id: sheetTreePanel
            anchors.fill: parent
            visible: true
        }
    }

    Component{
        id: wastebinPanelComponent
        WastebinPanel {
            Layout.fillHeight: true
            Layout.fillWidth: true
            implicitHeight: parent.height
            implicitWidth: parent.width
            id: wastebinPanel
            anchors.fill: parent
            visible: true
        }
    }

    function init(){
        tabView.addTab("Sheets", sheetTreePanelComponent)
        tabView.addTab("Wastebin", wastebinPanelComponent)
    }

    Component.onCompleted: init()



}
