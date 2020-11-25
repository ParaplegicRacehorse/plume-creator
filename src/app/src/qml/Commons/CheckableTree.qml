import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQml.Models 2.15
import QtQml 2.15
import QtQuick.Controls.Material 2.15
import eu.skribisto.projecthub 1.0
import "../Items"
import ".."

ListView {
    id: root




    signal openDocument(int openedProjectId, int openedPaperId, int projectId, int paperId)
    signal openDocumentInNewTab(int projectId, int paperId)
    signal openDocumentInNewWindow(int projectId, int paperId)


    signal copyCalled(int projectId, int paperId)
    signal deleteDefinitivelyCalled(int projectId, int paperId)
    //signal sendToTrashCalled(int projectId, int paperId)
    signal escapeKeyPressed()

    property int currentPaperId: -2
    property int currentProjectId: -2
    property int openedProjectId: -2
    property int openedPaperId: -2
    property bool hoveringChangingTheCurrentItemAllowed: true

    property alias visualModel: visualModel
    property var proxyModel


    DelegateModel {
        id: visualModel

        delegate: dragDelegate
    }
    model: visualModel

    property int contextMenuItemIndex: -2
    onCurrentIndexChanged: {
        contextMenuItemIndex = root.currentIndex
    }


    // options :
    property bool treelikeIndentsVisible: false
    property bool checkButtonsVisible: false
    property bool openActionsEnabled: false
    property bool renameActionEnabled: false
    property bool sendToTrashActionEnabled: false
    property bool deleteActionEnabled: false
    property bool cutActionEnabled: false
    property bool copyActionEnabled: false
    property bool pasteActionEnabled: false
    property bool elevationEnabled: false

    //tree-like onTreelikeIndents
    property int treeIndentOffset: 0
    property int treeIndentMultiplier: 10

    spacing: elevationEnabled ? 5 : 0
    leftMargin: elevationEnabled ? 5 : 0

    // checkButtons :
    function getCheckedPaperIdList(){
        return proxyModel.getCheckedIdsList()
    }

    function setCheckedPaperIdList(checkedPaperIdList){
        proxyModel.setCheckedIdsList(checkedPaperIdList)
    }



    // TreeView item :
    delegate:     Component {
        id: dragDelegate

        Item {
            id: delegateRoot

            Accessible.name: {

                var levelText
                if(treelikeIndentsVisible){
                    levelText = qsTr("Level %1").arg(model.indent)
                }

                var titleText = titleLabel.text

                var checkedText
                if(checkButtonsVisible){
                    checkedText = model.checkState === Qt.PartiallyChecked ? qsTr("partially checked") :
                                                                             model.checkState === Qt.Checked ? qsTr("checked") :
                                                                                                               model.checkState === Qt.Unchecked ? qsTr("unchecked") : ""
                }

                var labelText = ""
                if(labelLabel.text.length > 0){
                    labelText = qsTr("label: %1").arg(labelLabel.text)
                }

                var hasChildrenText = ""
                if(model.hasChildren){
                    hasChildrenText = qsTr("has children")
                }

                return levelText + " " + titleText + " " + checkedText + " " + labelText + " " + hasChildrenText

            }
            Accessible.role: Accessible.ListItem
            Accessible.description: qsTr("navigation item")


            property int visualIndex: {
                return DelegateModel.itemsIndex
            }

            Binding {
                target: content
                property: "visualIndex"
                value: visualIndex
            }

            anchors {
                left: Qt.isQtObject(parent) ? parent.left : undefined
                right: Qt.isQtObject(parent) ? parent.right : undefined
                rightMargin: 5
                leftMargin: treelikeIndentsVisible ? model.indent * root.treeIndentMultiplier - root.treeIndentOffset * root.treeIndentMultiplier : undefined
            }



            height: content.height


            onActiveFocusChanged: {
                if(root.currentIndex === model.index && model.index !== -1 && activeFocus){
                    root.currentPaperId = model.paperId
                }
            }

            //            drag.target: held ? content : undefined
            //            drag.axis: Drag.YAxis

            //            onPressAndHold: held = true
            //            onReleased: held = false
            //            Shortcut {
            //                sequence: "Ctrl+Up"
            //                onActivated: moveUpAction.trigger(delegateRoot)
            //            }
            //            Keys.onShortcutOverride: {
            //                if (event.key === Qt.Key_Backspace) {
            //                    console.log("onShortcutOverride")
            //                    event.accepted = true
            //                }
            //            }
            //            Keys.onBackPressed: {
            //                console.log("eee")
            //            }
            function editName() {
                state = "edit_name"
                titleTextFieldForceActiveFocusTimer.start()
                titleTextField.selectAll()
            }

            Timer{
                id: titleTextFieldForceActiveFocusTimer
                repeat: false
                interval: 100
                onTriggered: {
                    titleTextField.forceActiveFocus()
                }
            }

            function editLabel() {
                state = "edit_label"
                labelTextFieldForceActiveFocusTimer.start()
                labelTextField.selectAll()
            }

            Timer{
                id: labelTextFieldForceActiveFocusTimer
                repeat: false
                interval: 100
                onTriggered: {
                    labelTextField.forceActiveFocus()
                }
            }

            Keys.priority: Keys.AfterItem

            Keys.onShortcutOverride: {
                if((event.modifiers & Qt.ControlModifier) && event.key === Qt.Key_N){
                    event.accepted = true
                }
                if((event.modifiers & Qt.ControlModifier) && (event.modifiers & Qt.ShiftModifier) && event.key === Qt.Key_N){
                    event.accepted = true
                }
                if(copyActionEnabled && (event.modifiers & Qt.ControlModifier) && event.key === Qt.Key_C){
                    event.accepted = true
                }
                if(cutActionEnabled && (event.modifiers & Qt.ControlModifier) && event.key === Qt.Key_X){
                    event.accepted = true
                }
                if(pasteActionEnabled && (event.modifiers & Qt.ControlModifier) && event.key === Qt.Key_V){
                    event.accepted = true
                }
                if(renameActionEnabled && event.key === Qt.Key_Escape && (delegateRoot.state == "edit_name" || delegateRoot.state == "edit_label")){
                    event.accepted = true
                }
                if( event.key === Qt.Key_Escape){
                    event.accepted = true
                }
            }

            Keys.onPressed: {
                if (model.isOpenable && openActionsEnabled && event.key === Qt.Key_Return){
                    console.log("Return key pressed")
                    openDocumentAction.trigger()
                    event.accepted = true
                }
                if (model.isOpenable && openActionsEnabled && (event.modifiers & Qt.AltModifier) && event.key === Qt.Key_Return){
                    console.log("Alt Return key pressed")
                    openDocumentInNewTabAction.trigger()
                    event.accepted = true
                }

                // checked :
                if(checkButtonsVisible){
                    if (event.key === Qt.Key_Space){
                        console.log("Space pressed")
                        selectionCheckBox.toggle()
                        event.accepted = true
                    }
                }



                // rename

                if (model.isRenamable && renameActionEnabled && event.key === Qt.Key_F2 && delegateRoot.state !== "edit_name" && delegateRoot.state !== "edit_label"){
                    renameAction.trigger()
                    event.accepted = true
                }

                // cut
                if (model.isMovable && cutActionEnabled && (event.modifiers & Qt.ControlModifier) && event.key === Qt.Key_X && delegateRoot.state !== "edit_name" && delegateRoot.state !== "edit_label"){
                    cutAction.trigger()
                    event.accepted = true
                }

                // copy
                if (copyActionEnabled && (event.modifiers & Qt.ControlModifier) && event.key === Qt.Key_C && delegateRoot.state !== "edit_name" && delegateRoot.state !== "edit_label"){
                    copyAction.trigger()
                    event.accepted = true
                }

                if (event.key === Qt.Key_Escape){
                    console.log("Escape key pressed")
                    root.escapeKeyPressed()
                    event.accepted = true
                }

            }

            property bool editBugWorkaround: false

            SkrPane {
                id: content
                property int visualIndex: 0
                property int sourceIndex: -2

                property bool isCurrent: model.index === root.currentIndex ? true : false

                anchors {
                    horizontalCenter: parent.horizontalCenter
                    verticalCenter: parent.verticalCenter
                }
                width: delegateRoot.width
                height: 50

                padding: 1

                elevation: root.elevationEnabled ? 4 : 0


                HoverHandler {
                    id: hoverHandler
                    //                    onHoveredChanged: {
                    //                        if (hoverHandler.hovered & hoveringChangingTheCurrentItemAllowed) {
                    //                            root.currentIndex = model.index
                    //                        }
                    //                    }
                }

                TapHandler {
                    id: tapHandler



                    onSingleTapped: {
                        root.currentIndex = model.index
                        delegateRoot.forceActiveFocus()
                        eventPoint.accepted = true
                    }

                    onDoubleTapped: {
                        console.log("double tapped")
                        root.currentIndex = model.index
                        openDocumentAction.trigger()
                        eventPoint.accepted = true
                    }

                    onGrabChanged: {
                        point.accepted = false

                    }
                }

                TapHandler {
                    acceptedDevices: PointerDevice.Mouse | PointerDevice.Stylus
                    acceptedButtons: Qt.RightButton
                    onTapped: {

                        root.currentIndex = model.index

                        if(menu.visible){
                            menu.close()
                            return
                        }

                        menu.open()
                        eventPoint.accepted = true
                    }
                }
                TapHandler {
                    acceptedDevices: PointerDevice.Mouse | PointerDevice.Stylus
                    acceptedButtons: Qt.MiddleButton
                    onTapped: {
                        root.currentIndex = model.index
                        openDocumentInNewTabAction.trigger()
                        eventPoint.accepted = true

                    }
                }


                Action {
                    id: openDocumentAction
                    //shortcut: "Return"
                    enabled: {
                        if (root.focus === true && titleTextField.visible === false
                                && root.currentIndex === model.index) {
                            return true
                        } else
                            return false
                    }

                    text: "Open document"
                    onTriggered: {
                        //console.log("model.openedProjectId", openedProjectId)
                        //console.log("model.projectId", model.projectId)
                        root.openDocument(openedProjectId, openedPaperId, model.projectId,
                                          model.paperId)
                    }
                }

                Action {
                    id: openDocumentInNewTabAction
                    //shortcut: "Alt+Return"
                    enabled: {
                        if (root.focus === true && titleTextField.visible === false
                                && root.currentIndex === model.index) {
                            return true
                        } else
                            return false
                    }

                    text: "Open document in a new tab"
                    onTriggered: {
                        console.log("model.projectId", model.projectId)
                        root.openDocumentInNewTab(model.projectId,
                                                  model.paperId)

                    }
                }


                Action {
                    id: openDocumentInNewWindowAction
                    //shortcut: "Alt+Return"
                    enabled: {
                        if (root.enabled && titleTextField.visible === false
                                && root.currentIndex === model.index) {
                            return true
                        } else
                            return false
                    }

                    text: qsTr("Open document in a window")
                    onTriggered: {
                        root.openDocumentInNewWindow(model.projectId,
                                                     model.paperId)

                    }
                }

                ColumnLayout{
                    id: columnLayout3
                    anchors.fill: parent


                    RowLayout {
                        id: rowLayout
                        spacing: 2
                        Layout.fillHeight: true
                        Layout.fillWidth: true


                        CheckBox{
                            id: selectionCheckBox
                            //Layout.fillHeight: true
                            //Layout.preferredWidth: 5
                            visible: checkButtonsVisible
                            tristate: true
                            focusPolicy: Qt.NoFocus

                            onPressed: {
                                root.currentIndex = model.index
                            }

                            onCheckStateChanged: {

                                if(root.currentIndex === model.index){
                                    //console.log("model.hasChildren", model.hasChildren)
                                    if(checkState === Qt.PartiallyChecked && !proxyModel.hasChildren(model.projectId, model.paperId)){
                                        model.checkState = Qt.Checked
                                    }
                                    else if(checkState === Qt.PartiallyChecked && proxyModel.hasChildren(model.projectId, model.paperId)){
                                        model.checkState = Qt.PartiallyChecked
                                    }
                                    else if(checkState === Qt.Checked){
                                        model.checkState = Qt.Checked
                                    }
                                    else if(checkState === Qt.Unchecked){
                                        model.checkState = Qt.Unchecked
                                    }

                                }
                            }

                            Binding on checkState {
                                value: model.checkState
                                delayed: true
                                restoreMode: Binding.RestoreBindingOrValue
                            }

                        }

                        Rectangle {
                            id: trashedIndicator
                            color: "#b50003"
                            Layout.fillHeight: true
                            Layout.preferredWidth: 5
                            visible: model.trashed
                        }
                        Rectangle {
                            id: currentItemIndicator
                            color: "lightsteelblue"
                            Layout.fillHeight: true
                            Layout.preferredWidth: 5
                            visible: root.currentIndex === model.index
                        }
                        Rectangle {
                            id: openedItemIndicator
                            color: SkrTheme.accent
                            Layout.fillHeight: true
                            Layout.preferredWidth: 5
                            visible: model.projectId === openedProjectId && model.paperId === openedPaperId
                        }

                        SkrButton {
                            id: projectIsBackupIndicator
                            visible: model.projectIsBackup && model.paperId === -1
                            enabled: true
                            focusPolicy: Qt.NoFocus
                            implicitHeight: 32
                            implicitWidth: 32
                            Layout.maximumHeight: 30
                            padding: 0
                            rightPadding: 0
                            bottomPadding: 0
                            leftPadding: 2
                            topPadding: 0
                            flat: true
                            onDownChanged: down = false

                            icon {
                                source: "qrc:///icons/backup/tools-media-optical-burn-image.svg"
                                height: 32
                                width: 32
                            }


                            hoverEnabled: true
                            ToolTip.delay: 1000
                            ToolTip.timeout: 5000
                            ToolTip.visible: hovered
                            ToolTip.text: qsTr("This project is a backup")
                        }


                        Rectangle {
                            color: "transparent"
                            //border.width: 1
                            Layout.fillWidth: true
                            Layout.fillHeight: true

                            ColumnLayout {
                                id: columnLayout2
                                spacing: 1
                                anchors.fill: parent

                                SkrLabel {
                                    id: titleLabel

                                    Layout.fillWidth: true
                                    Layout.topMargin: 2
                                    Layout.leftMargin: 4
                                    Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter

                                    text: model.indent === -1 ? model.projectName : model.name
                                    elide: Text.ElideRight
                                }

                                SkrTextField {
                                    id: labelTextField
                                    visible: false


                                    Layout.fillWidth: true
                                    Layout.fillHeight: true
                                    text: labelLabel.text
                                    maximumLength: 50

                                    placeholderText: qsTr("Enter label")

                                    onEditingFinished: {
                                        //if (!activeFocus) {
                                        //accepted()
                                        //}
                                        //console.log("editing label finished")
                                        model.label = text
                                        delegateRoot.state = ""
                                    }

                                    //Keys.priority: Keys.AfterItem
                                    Keys.onShortcutOverride: event.accepted = (event.key === Qt.Key_Escape)
                                    Keys.onPressed: {
                                        if (event.key === Qt.Key_Return){
                                            console.log("Return key pressed title")
                                            editingFinished()
                                            event.accepted = true
                                        }
                                        if ((event.modifiers & Qt.CtrlModifier) && event.key === Qt.Key_Return){
                                            console.log("Ctrl Return key pressed title")
                                            editingFinished()
                                            event.accepted = true
                                        }
                                        if (event.key === Qt.Key_Escape){
                                            console.log("Escape key pressed title")
                                            delegateRoot.state = ""
                                            event.accepted = true
                                        }
                                    }

                                }

                                SkrTextField {
                                    id: titleTextField
                                    visible: false


                                    Layout.fillWidth: true
                                    Layout.fillHeight: true
                                    text: titleLabel.text
                                    maximumLength: 50

                                    placeholderText: qsTr("Enter name")

                                    onEditingFinished: {
                                        //if (!activeFocus) {
                                        //accepted()
                                        //}
                                        console.log("editing finished")
                                        model.name = text
                                        delegateRoot.state = ""
                                    }

                                    //Keys.priority: Keys.AfterItem
                                    Keys.onShortcutOverride: event.accepted = (event.key === Qt.Key_Escape)
                                    Keys.onPressed: {
                                        if (event.key === Qt.Key_Return){
                                            console.log("Return key pressed title")
                                            editingFinished()
                                            event.accepted = true
                                        }
                                        if ((event.modifiers & Qt.CtrlModifier) && event.key === Qt.Key_Return){
                                            console.log("Ctrl Return key pressed title")
                                            editingFinished()
                                            event.accepted = true
                                        }
                                        if (event.key === Qt.Key_Escape){
                                            console.log("Escape key pressed title")
                                            delegateRoot.state = ""
                                            event.accepted = true
                                        }
                                    }

                                }
                                RowLayout{
                                    id: labelLayout
                                    Layout.fillWidth: true
                                    Layout.leftMargin: 5

                                    ListItemAttributes{
                                        id: attributes
                                        attributes: model.attributes
                                        Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter
                                        Layout.leftMargin: 4
                                        Layout.bottomMargin: 2

                                    }


                                    SkrLabel {
                                        id: labelLabel
                                        text:  model.label === undefined ? "" : model.label
                                        Layout.bottomMargin: 2
                                        Layout.rightMargin: 4
                                        Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                                        elide: Text.ElideRight
                                        horizontalAlignment: Qt.AlignRight
                                        Layout.fillWidth: true


                                    }
                                }
                            }
                            //                        MouseArea {
                            //                            anchors.fill: parent
                            //                        }
                        }

                        SkrToolButton {
                            id: menuButton
                            Layout.fillHeight: true
                            Layout.preferredWidth: 30

                            text: "..."
                            flat: true
                            focusPolicy: Qt.NoFocus

                            onClicked: {

                                root.currentIndex = model.index
                                delegateRoot.forceActiveFocus()

                                if(menu.visible){
                                    menu.close()
                                    return
                                }

                                menu.open()
                            }

                            visible: hoverHandler.hovered | content.isCurrent
                        }

                        Rectangle {
                            Layout.fillHeight: true
                            Layout.preferredWidth: 2

                            color: model.indent === 0 ? Material.color(Material.Indigo) :
                                                        (model.indent === 1 ? Material.color(Material.LightBlue) :
                                                                              (model.indent === 2 ? Material.color(Material.LightGreen) :
                                                                                                    (model.indent === 3 ? Material.color(Material.Amber) :
                                                                                                                          (model.indent === 4 ? Material.color(Material.DeepOrange) :
                                                                                                                                                Material.color(Material.Teal)
                                                                                                                           ))))
                        }
                    }
                    Rectangle {
                        id: separator
                        Layout.preferredHeight: 1
                        Layout.preferredWidth: content.width / 2
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom
                        gradient: Gradient {
                            orientation: Qt.Horizontal
                            GradientStop {
                                position: 0.00;
                                color: "#ffffff";
                            }
                            GradientStop {
                                position: 0.30;
                                color: "#9e9e9e";
                            }
                            GradientStop {
                                position: 0.70;
                                color: "#9e9e9e";
                            }
                            GradientStop {
                                position: 1.00;
                                color: "#ffffff";
                            }
                        }

                    }

                }
            }
            //            DropArea {
            //                id: dropArea
            //                anchors {
            //                    fill: parent
            //                    margins: 10
            //                }
            //                property int sourceIndex: -1
            //                property int targetIndex: -1
            //                onEntered: {
            //                    sourceIndex = drag.source.DelegateModel.itemsIndex
            //                    targetIndex = dragArea.DelegateModel.itemsIndex
            //                    //                    var sourceIndex = drag.source.DelegateModel.itemsIndex
            //                    //                    var targetIndex = dragArea.DelegateModel.itemsIndex
            //                    visualModel.items.move(sourceIndex, targetIndex)

            //                    //                    var sourceModelIndex = drag.source.DelegateModel.modelIndex(
            //                    //                                sourceIndex)
            //                    //                    var targetModelIndex = dragArea.DelegateModel.modelIndex(
            //                    //                                targetIndex)

            //                    //                    console.log("targetIndex : ", sourceModelIndex.name)
            //                }

            //                onDropped: {
            //                    console.log("onDropped")
            //                }
            //            }
            states: [
                State {
                    name: "drag_active"
                    when: content.Drag.active

                    ParentChange {
                        target: content
                        parent: base
                    }
                    AnchorChanges {
                        target: content
                        anchors {
                            horizontalCenter: undefined
                            verticalCenter: undefined
                        }
                    }
                },
                State {
                    name: "edit_name"
                    PropertyChanges {
                        target: menuButton
                        visible: false
                    }
                    PropertyChanges {
                        target: titleLabel
                        visible: false
                    }
                    PropertyChanges {
                        target: labelLayout
                        visible: false
                    }
                    PropertyChanges {
                        target: titleTextField
                        visible: true
                    }
                    PropertyChanges {
                        target: labelTextField
                        visible: false
                    }
                },
                State {
                    name: "edit_label"
                    PropertyChanges {
                        target: menuButton
                        visible: false
                    }
                    PropertyChanges {
                        target: titleLabel
                        visible: false
                    }
                    PropertyChanges {
                        target: labelLayout
                        visible: false
                    }
                    PropertyChanges {
                        target: titleTextField
                        visible: false
                    }
                    PropertyChanges {
                        target: labelTextField
                        visible: true
                    }
                },

                State {
                    name: "unset_anchors"
                    AnchorChanges {
                        target: delegateRoot
                        anchors.left: undefined
                        anchors.right: undefined

                    }
                }
            ]

            //            Shortcut {
            //                sequences: ["Ctrl+Shift+N"]
            //                onActivated: addBeforeAction.trigger()
            //                enabled: root.visible
            //            }
            SkrMenu {
                id: menu
                y: menuButton.height

                onOpened: {
                    hoveringChangingTheCurrentItemAllowed = false
                    // necessary to differenciate between all items
                    contextMenuItemIndex = model.index
                }

                onClosed: {
                    hoveringChangingTheCurrentItemAllowed = true

                }


                SkrMenuItem {
                    height: model.isOpenable && openActionsEnabled ? undefined : 0
                    visible: model.isOpenable && openActionsEnabled
                    action: Action {
                        id: openPaperAction
                        text: qsTr("Open")
                        //shortcut: "Return"
                        icon {
                            source: "qrc:///icons/backup/document-edit.svg"
                        }
                        enabled: openActionsEnabled && contextMenuItemIndex === model.index && titleTextField.visible === false  && root.enabled &&  model.paperId !== -1
                        onTriggered: {
                            console.log("open paper action", model.projectId,
                                        model.paperId)
                            openDocumentAction.trigger()
                        }
                    }
                }

                SkrMenuItem {
                    height: model.isOpenable && openActionsEnabled ? undefined : 0
                    visible: model.isOpenable && openActionsEnabled
                    action: Action {
                        id: openPaperInNewTabAction
                        text: qsTr("Open in new tab")
                        //shortcut: "Alt+Return"
                        icon {
                            source: "qrc:///icons/backup/tab-new.svg"
                        }
                        enabled: openActionsEnabled && contextMenuItemIndex === model.index && titleTextField.visible === false  && root.enabled &&  model.paperId !== -1
                        onTriggered: {
                            console.log("open paper in new tab action", model.projectId,
                                        model.paperId)
                            openDocumentInNewTabAction.trigger()
                        }
                    }
                }

                SkrMenuItem {
                    height: model.isOpenable && openActionsEnabled ? undefined : 0
                    visible: model.isOpenable && openActionsEnabled
                    action: Action {
                        id: openPaperInNewWindowAction
                        text: qsTr("Open in new window")
                        //shortcut: "Alt+Return"
                        icon {
                            source: "qrc:///icons/backup/window-new.svg"
                        }
                        enabled: openActionsEnabled && contextMenuItemIndex === model.index && titleTextField.visible === false && root.enabled &&  model.paperId !== -1
                        onTriggered: {
                            console.log("open paper in new window action", model.projectId,
                                        model.paperId)
                            openDocumentInNewWindowAction.trigger()
                        }
                    }
                }

                MenuSeparator {
                    height: model.isRenamable && renameActionEnabled  ? undefined : 0
                    visible: model.isRenamable && renameActionEnabled
                }

                SkrMenuItem {
                    height: model.isRenamable && renameActionEnabled ? undefined : 0
                    visible: model.isRenamable && renameActionEnabled
                    action :Action {
                        id: renameAction
                        text: qsTr("Rename")
                        //shortcut: "F2"
                        icon {
                            source: "qrc:///icons/backup/edit-rename.svg"
                        }
                        enabled: renameActionEnabled && contextMenuItemIndex === model.index  && root.enabled
                        onTriggered: {
                            console.log("rename action", model.projectId,
                                        model.paperId)
                            delegateRoot.editName()
                        }
                    }
                }


                SkrMenuItem {
                    height: model.isRenamable && renameActionEnabled ? undefined : 0
                    visible: model.isRenamable && renameActionEnabled
                    action :  Action {
                        id: setLabelAction
                        text: qsTr("Set label")

                        icon {
                            source: "qrc:///icons/backup/label.svg"
                        }
                        enabled: renameActionEnabled && contextMenuItemIndex === model.index  && root.enabled
                        onTriggered: {
                            console.log("sel label", model.projectId,
                                        model.paperId)
                            delegateRoot.editLabel()
                        }
                    }
                }

                MenuSeparator {
                    height: model.isCopyable && copyActionEnabled  ? undefined : 0
                    visible: model.isCopyable && copyActionEnabled
                }

                SkrMenuItem {
                    height: model.isCopyable && copyActionEnabled ? undefined : 0
                    visible: model.isCopyable && copyActionEnabled
                    action :Action {

                        text: qsTr("Copy")
                        //shortcut: StandardKey.Copy
                        icon {
                            source: "qrc:///icons/backup/edit-copy.svg"
                        }
                        enabled: copyActionEnabled && contextMenuItemIndex === model.index  && root.enabled

                        onTriggered: {
                            console.log("copy action", model.projectId,
                                        model.paperId)
                            copyCalled(model.projectId, model.paperId)
                        }
                    }
                }

                MenuSeparator {
                    height: model.isTrashable && (sendToTrashActionEnabled || deleteActionEnabled) ? undefined : 0
                    visible: model.isTrashable && (sendToTrashActionEnabled || deleteActionEnabled)
                }

                SkrMenuItem {
                    height: model.isTrashable && sendToTrashActionEnabled ? undefined : 0
                    visible: model.isTrashable && sendToTrashActionEnabled
                    action: Action {
                        text: qsTr("Send to trash")
                        //shortcut: "Del"
                        icon {
                            source: "qrc:///icons/backup/edit-delete.svg"
                        }
                        enabled: sendToTrashActionEnabled && contextMenuItemIndex === model.index  && root.enabled && model.indent !== -1
                        onTriggered: {
                            console.log("sent to trash action", model.projectId,
                                        model.paperId)
                            //sendToTrashCalled(model.projectId, model.paperId)
                            proxyModel.trashItemWithChildren(model.projectId, model.paperId)
                        }
                    }
                }

                SkrMenuItem {
                    height: model.isTrashable && deleteActionEnabled ? undefined : 0
                    visible: model.isTrashable && deleteActionEnabled
                    action: Action {
                        text: qsTr("Delete definitively")
                        //shortcut: "Del"
                        icon {
                            source: "qrc:///icons/backup/edit-delete-shred.svg"
                        }
                        enabled: deleteActionEnabled && contextMenuItemIndex === model.index  && root.enabled && model.indent !== -1
                        onTriggered: {
                            console.log("delete action", model.projectId,
                                        model.paperId)
                            deleteDefinitivelyCalled(model.projectId, model.paperId)
                        }
                    }
                }


            }

            ListView.onRemove: SequentialAnimation {
                PropertyAction {
                    target: delegateRoot
                    property: "ListView.delayRemove"
                    value: true
                }
                NumberAnimation {
                    target: delegateRoot
                    property: "height"
                    to: 0
                    easing.type: Easing.InOutQuad
                }
                PropertyAction {
                    target: delegateRoot
                    property: "ListView.delayRemove"
                    value: false
                }
            }

            //----------------------------------------------------------

            ListView.onAdd: SequentialAnimation {
                PropertyAction {
                    target: delegateRoot
                    property: "height"
                    value: 0
                }
                NumberAnimation {
                    target: delegateRoot
                    property: "height"
                    to: delegateRoot.height
                    duration: 250
                    easing.type: Easing.InOutQuad
                }
            }

            // move :
        }
    }


    remove: Transition {

        SequentialAnimation {
            id: removePaperAnimation
            PropertyAction {
                property: "ListView.delayRemove"
                value: true
            }
            PropertyAction {
                property: "state"
                value: "unset_anchors"
            }

            NumberAnimation {
                property: "x"
                to: root.width
                duration: 250
                easing.type: Easing.InBack
            }
            PropertyAction {
                property: "ListView.delayRemove"
                value: false
            }
        }
    }

    removeDisplaced: Transition {
        SequentialAnimation {
            PauseAnimation{duration: 250}
            NumberAnimation { properties: "x,y"; duration: 250 }
        }

    }

}
