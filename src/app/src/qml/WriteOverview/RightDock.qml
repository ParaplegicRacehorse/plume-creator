import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import Qt.labs.settings 1.1
import eu.skribisto.writedocumentlistmodel 1.0
import eu.skribisto.usersettings 1.0
import eu.skribisto.searchtaglistproxymodel 1.0
import eu.skribisto.taghub 1.0
import ".."
import "../Items"

RightDockForm {

    property int projectId : -2
    property int paperId : -2

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
        id: toolMenuShortcut
        enabled: root.enabled

    }


    //-----------------------------------------------------------


    //Menu :
    property list<Component> menuComponents:  [
        Component{
        id:  toolDockMenuComponent
        SkrMenu {
            id: toolDockMenu
            objectName: "toolDockMenu"
            title: qsTr("&Tools dock")


            Component.onCompleted: {

                toolMenuShortcut.sequence = skrQMLTools.mnemonic(title)
                toolMenuShortcut.activated.connect(function() {
                    Globals.openSubMenuCalled(toolDockMenu)
                })
            }


            SkrMenuItem {
                text: qsTr( "&Overview")
                onTriggered: {

                    if(Globals.compactMode){
                        rightDrawer.open()
                    }
                    sheetOverviewFrame.folded = false
                    sheetOverviewTool.forceActiveFocus()
                }
            }

            SkrMenuItem {
                text: qsTr( "&Edit")
                onTriggered: {

                    if(Globals.compactMode){
                        rightDrawer.open()
                    }
                    editFrame.folded = false
                    editView.forceActiveFocus()
                }
            }


            SkrMenuItem {
                text: qsTr( "&Tags")
                onTriggered: {

                    if(Globals.compactMode){
                        rightDrawer.open()
                    }
                    tagPadFrame.folded = false
                    tagPadView.forceActiveFocus()
                }
            }
        }
    }
]



    //-----------------------------------------------------------

    //-----------------------------------------------------------
    //---------------Overview---------------------------------------
    //-----------------------------------------------------------
    sheetOverviewFrame.onContentHeightChanged: {
        if(sheetOverviewFrame.SplitView.preferredHeight < sheetOverviewFrame.SplitView.minimumHeight){
            sheetOverviewFrame.SplitView.preferredHeight = sheetOverviewFrame.SplitView.minimumHeight
        }

        if(sheetOverviewFrame.SplitView.preferredHeight > sheetOverviewFrame.SplitView.maximumHeight){
            sheetOverviewFrame.SplitView.preferredHeight = sheetOverviewFrame.SplitView.maximumHeight
        }
    }


    //-----------------------------------------------------------
    //---------------Edit---------------------------------------------
    //-----------------------------------------------------------



    editView.skrSettingsGroup: SkrSettings.overviewTreeNoteSettings
    editView.textWidthSliderVisible: false



    //-----------------------------------------------------------
    //---------------Tags :---------------------------------------------
    //-----------------------------------------------------------


    //proxy model for tag list :

    SKRSearchTagListProxyModel {
        id: tagProxyModel
        projectIdFilter: projectId
        noteIdFilter: paperId
    }
    tagPadView.tagListModel: tagProxyModel

    Connections{
        target: tagPadView
        function onCallRemoveTagRelationship(projectId, itemId, tagId){
            plmData.tagHub().removeTagRelationship(projectId, SKRTagHub.Note , itemId, tagId)
        }
    }

    Connections{
        target: tagPadView
        function onCallAddTagRelationship(projectId, itemId, tagName){
            var result;
            // verify if name doesn't already exist :
            var tagId = plmData.tagHub().getTagIdWithName(projectId, tagName)

            if(tagId === -2){
                //if not, create tag
                result = plmData.tagHub().addTag(projectId, tagName)
                tagId = plmData.tagHub().getLastAddedId()
            }

            // set relationship
            result = plmData.tagHub().setTagRelationship(projectId, SKRTagHub.Note, itemId, tagId)
            if (!result){
                console.log("result onCallAddTagRelationship")
                //TODO: add notification
                return
            }
        }
    }

    onProjectIdChanged: {
        tagPadView.projectId = projectId
        tagPadView.itemId = -2
    }
    onPaperIdChanged: {
        tagPadView.itemId = paperId
    }

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
        category: "writeOverviewRightDock"
        property var dockSplitView
        property bool sheetOverviewFrameFolded: sheetOverviewFrame.folded
        property bool editFrameFolded: editFrame.folded
        property bool tagPadFrameFolded: tagPadFrame.folded
    }



    PropertyAnimation {
        target: sheetOverviewFrame
        property: "SplitView.preferredHeight"
        duration: 500
        easing.type: Easing.InOutQuad
    }
    PropertyAnimation {
        target: editFrame
        property: "SplitView.preferredHeight"
        duration: 500
        easing.type: Easing.InOutQuad
    }
    PropertyAnimation {
        target: tagPadFrame
        property: "SplitView.preferredHeight"
        duration: 500
        easing.type: Easing.InOutQuad
    }

    function loadConf(){

        sheetOverviewFrame.folded = settings.sheetOverviewFrameFolded
        editFrame.folded = settings.editFrameFolded
        tagPadFrame.folded = settings.tagPadFrameFolded

        splitView.restoreState(settings.dockSplitView)

    }

    function resetConf(){
        sheetOverviewFrame.folded = false
        editFrame.folded = false
        tagPadFrame.folded = false
        splitView.restoreState("")

    }

    Component.onCompleted: {
        loadConf()
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
