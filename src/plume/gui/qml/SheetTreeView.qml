import QtQuick 2.4
import QtQuick.Controls 1.4
import QtQml.Models 2.2
import QtQuick.Layouts 1.1

SheetTreeViewForm {

    signal openSheetSignal(int sheet_id)

    function init() {
        treeView.model = sheet_tree_model_0
        treeView.rowDelegate = itemDelegate

    }

    Component {
        id: itemDelegate
        Rectangle {
            id: wrapper
            border.color: "#595959"
            radius: 2
            focus: true
            border.width: wrapper.TreeView.isCurrentItem ? 2 : 1
            RowLayout {
                id: row
                Text {
                    id: itemTitle
                    width: wrapper.width
                    elide: Text.ElideLeft
                    text: "<b>" + model.sheet_title + " :</b>"
                    //                    color: wrapper.ListView.isCurrentItem ? "red" : "black"
                }
                Text {
                    id: itemContent
                    x:20
                    elide: Text.ElideLeft
                    width: wrapper.width
                    wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                    maximumLineCount: 1
                    text: model.sheet_id
                    //                    color: wrapper.ListView.isCurrentItem ? "red" : "black"
                }

            }

            MouseArea {
                id: mouseArea
                anchors.fill: parent
                acceptedButtons: Qt.LeftButton | Qt.RightButton
                onClicked: {

                    var xPoint = mouseArea.mapToItem(treeView,mouse.x, mouse.y).x
                    var yPoint = mouseArea.mapToItem(treeView,mouse.x, mouse.y).y
                    var index = treeView.indexAt(xPoint, yPoint)
                    console.debug(xPoint, "   ", yPoint)

                    if (mouse.button === Qt.LeftButton)
                    {
                        if(index.isValid)
                            console.debug('eeee')
                        treeView.activated(index)
                        if(treeView.isExpanded(index))
                            treeView.collapse(index)
                        else
                            treeView.expand(index)

                    }
                    else if (mouse.button === Qt.RightButton)
                    {
                        treeView.activated(index)

                    }
                }
                onDoubleClicked:
                    if (mouse.button === Qt.LeftButton)
                    {
                        openSheetSignal(model.sheet_id)
                    }
            }
        }
    }



    //    DelegateModel {
    //          id: visualModel
    //          model: sheet_tree_model_0
    ////          delegate: /*itemDelegate*/

    ////              Rectangle {
    ////              height: 25
    ////              width: 100
    ////              Text { text: "Name: " + name}
    ////          }
    //      }
    //    treeView.model: visualModel

    Component.onCompleted: init()

}
