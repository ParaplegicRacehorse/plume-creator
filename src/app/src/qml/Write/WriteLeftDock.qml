import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import Qt.labs.settings 1.1
import eu.skribisto.searchsheetlistproxymodel 1.0
import eu.skribisto.writedocumentlistmodel 1.0
import eu.skribisto.usersettings 1.0
import ".."
import "../Items"

WriteLeftDockForm {
    id: root


    SKRUserSettings {
        id: skrUserSettings
    }

    splitView.handle: Item {
        id: handle
        implicitHeight: 8
        property bool hovered: SplitHandle.hovered

        RowLayout {
            anchors.fill: parent
            Rectangle {
                Layout.preferredWidth: 20
                Layout.preferredHeight: 5
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                color: hoverHandler.hovered ? SkrTheme.accent : SkrTheme.divider

                HoverHandler {
                    id: hoverHandler
                    cursorShape: Qt.SplitVCursor
                }
            }
        }
    }


    //-----------------------------------------------------------

    Shortcut {
        id: navigationMenuShortcut
        enabled: root.enabled

    }


    //-----------------------------------------------------------


    //Menu :
    property list<Component> menuComponents:  [
        Component{
            id:  navigationDockMenuComponent
            SkrMenu {
                id: navigationDockMenu
                objectName: "navigationDockMenu"
                title: qsTr("&Navigation dock")

                Component.onCompleted: {

                    navigationMenuShortcut.sequence = skrQMLTools.mnemonic(title)
                    navigationMenuShortcut.activated.connect(function() {
                        Globals.openSubMenuCalled(navigationDockMenu)
                    })
                }


                SkrMenuItem {
                    text: qsTr("&Navigation")
                    onTriggered: {
                        if(Globals.compactMode){
                            leftDrawer.open()
                        }
                        navigationFrame.folded = false
                        navigation.forceActiveFocus()
                    }
                }

                SkrMenuItem {
                    text: qsTr("&Documents")
                    onTriggered: {
                        if(Globals.compactMode){
                            leftDrawer.open()
                        }
                        documentFrame.folded = false
                        documentView.forceActiveFocus()
                    }
                }
            }
        }
    ]

    //Navigation List :
    //-----------------------------------------------------------

    SKRSearchSheetListProxyModel {
        id: navigationProxyModel
        showTrashedFilter: false
        showNotTrashedFilter: true
        navigateByBranchesEnabled: true
    }

    navigation.treeListViewProxyModel: navigationProxyModel

    SKRSearchSheetListProxyModel {
        id: trashedSheetProxyModel
        showTrashedFilter: true
        showNotTrashedFilter: false
    }
    navigation.trashedListViewProxyModel: trashedSheetProxyModel


    SKRSearchSheetListProxyModel {
        id: restoreSheetProxyModel
        showTrashedFilter: true
        showNotTrashedFilter: false
    }
    navigation.restoreListViewProxyModel: restoreSheetProxyModel






    function restoreSheetList(projectId, sheetIdList){
        // restore is difficult to explain : a restored parent will restore its children, even those trashed years before. To avoid that,
        // children trashed at the same minute will be checked to allow restore. The older ones will stay unchecked by default.
        // All that is done in RestoreView.qml

        var i
        for(i = 0 ; i < sheetIdList.length ; i++){
            plmData.sheetHub().untrashOnlyOnePaper(projectId, sheetIdList[i])
        }


       //console.log("restored: sheet:", sheetIdList)
    }











    //-----------------------------------------------------------

    //Document List :
    //-----------------------------------------------------------
    documentView.model: plmModels.writeDocumentListModel()
    documentView.documentModel: plmModels.writeDocumentListModel()

    //-----------------------------------------------------------


    //-----------------------------------------------------------

    //-----------------------------------------------------------
    transitions: [
        Transition {

            PropertyAnimation {
                properties: "implicitWidth"
                easing.type: Easing.InOutQuad
                duration: 500
            }
        }
    ]

    property alias settings: settings

    Settings {
        id: settings
        category: "writeLeftDock"
        property var dockSplitView
        property bool navigationFrameFolded: navigationFrame.folded
        property bool documentFrameFolded: documentFrame.folded
    }

    function setCurrentPaperId(projectId, paperId) {
        navigationProxyModel.setCurrentPaperId(projectId, paperId)
    }
    function setOpenedPaperId(projectId, paperId) {
        navigation.openedProjectId = projectId
        navigation.openedPaperId = paperId
    }


    PropertyAnimation {
        target: navigationFrame
        property: "SplitView.preferredHeight"
        duration: 500
        easing.type: Easing.InOutQuad
    }


    function loadConf(){

        navigationFrame.folded = settings.navigationFrameFolded
        documentFrame.folded = settings.documentFrameFolded
        splitView.restoreState(settings.dockSplitView)


    }

    function resetConf(){
        navigationFrame.folded = false
        documentFrame.folded = false
        splitView.restoreState("")

    }

    Component.onCompleted: {


        loadConf()
        navigation.openDocument.connect(Globals.openSheetCalled)
        navigation.openDocumentInNewTab.connect(Globals.openSheetInNewTabCalled)
        navigation.openDocumentInNewWindow.connect(Globals.openSheetInNewWindowCalled)
        navigation.restoreDocumentList.connect(root.restoreSheetList)
        Globals.resetDockConfCalled.connect(resetConf)


    }
    Component.onDestruction: {

        settings.dockSplitView = splitView.saveState()

    }

    onEnabledChanged: {
        if(enabled){

        }
    }
}
