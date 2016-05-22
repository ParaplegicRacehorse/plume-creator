import QtQuick 2.4

DockBaseForm {
    property int orientation

    // size handle :

    signal baseWidthChanged(int value)

    handleMouseArea.acceptedButtons: Qt.LeftButton

    handleMouseArea.onEntered: handleMouseArea.cursorShape = Qt.SizeHorCursor
    handleMouseArea.onExited: handleMouseArea.cursorShape = Qt.ArrowCursor

    handleMouseArea.onPressed: {
        sizeHandle.anchors.top = undefined
        sizeHandle.anchors.topMargin = undefined
        sizeHandle.anchors.bottom = undefined
        sizeHandle.anchors.bottomMargin = undefined
        sizeHandle.anchors.right = undefined
        sizeHandle.anchors.rightMargin = undefined
        sizeHandle.anchors.left = undefined
        sizeHandle.anchors.leftMargin = undefined

        if(orientation === Qt.RightEdge){
        handleMouseArea.drag.minimumX = base.width - 300
        handleMouseArea.drag.maximumX = base.width - 170
        }

    }
    handleMouseArea.onReleased: {


        if(orientation === Qt.LeftEdge){
            var distance_left = sizeHandle.x
            baseWidthChanged(distance_left)

            sizeHandle.anchors.top = sizeHandle.parent.top
            sizeHandle.anchors.topMargin = 0
            sizeHandle.anchors.bottom = sizeHandle.parent.bottom
            sizeHandle.anchors.bottomMargin = 0
            sizeHandle.anchors.right = sizeHandle.parent.right
            sizeHandle.anchors.rightMargin = 0
            sizeHandle.anchors.left = undefined
            sizeHandle.anchors.leftMargin = undefined
        }
        if(orientation === Qt.RightEdge){
            var distance_right = base.width - sizeHandle.x
            baseWidthChanged(distance_right)

            sizeHandle.anchors.top = sizeHandle.parent.top
            sizeHandle.anchors.topMargin = 0
            sizeHandle.anchors.bottom = sizeHandle.parent.bottom
            sizeHandle.anchors.bottomMargin = 0
            sizeHandle.anchors.right = undefined
            sizeHandle.anchors.rightMargin = undefined
            sizeHandle.anchors.left = sizeHandle.parent.left
            sizeHandle.anchors.leftMargin = 0
        }
    }

    handleMouseArea.drag.target: sizeHandle
    onOrientationChanged: {
        if(orientation === Qt.LeftEdge){
            sizeHandle.anchors.top = sizeHandle.parent.top
            sizeHandle.anchors.topMargin = 0
            sizeHandle.anchors.bottom = sizeHandle.parent.bottom
            sizeHandle.anchors.bottomMargin = 0
            sizeHandle.anchors.right = sizeHandle.parent.right
            sizeHandle.anchors.rightMargin = 0
            sizeHandle.anchors.left = undefined
            sizeHandle.anchors.leftMargin = undefined

            handleMouseArea.drag.axis = Drag.XAxis
            handleMouseArea.drag.minimumX = 170
            handleMouseArea.drag.maximumX = 300
        }
        if(orientation === Qt.RightEdge){
            sizeHandle.anchors.top = sizeHandle.parent.top
            sizeHandle.anchors.topMargin = 0
            sizeHandle.anchors.bottom = sizeHandle.parent.bottom
            sizeHandle.anchors.bottomMargin = 0
            sizeHandle.anchors.right = undefined
            sizeHandle.anchors.rightMargin = undefined
            sizeHandle.anchors.left = sizeHandle.parent.left
            sizeHandle.anchors.leftMargin = -4

            handleMouseArea.drag.axis = Drag.XAxis
        }
    }




    property var dockList: []

    function closeDock(dock){
        if(checkIfNoDock())
            setOneDockVisible()
        if(checkIfLastDock()){
            hide()
            return
        }
        dock.visible = false
    }

    function setOneDockVisible() {
        for(var i = 0; i < dockList.length; ++i){
            if(dockList[i].visible === false){
                dockList[i].visible = true;
                return;
            }

        }
    }

    function checkIfNoDock() {
        return _countOfVisibleDocks() === 0 ? true : false

    }

    function checkIfLastDock() {
        return _countOfVisibleDocks() === 1 ? true : false
    }
    function _countOfVisibleDocks() {
        var count = 0
        for(var i = 0; i < dockList.length; ++i)
            if(dockList[i].visible === true)
                count += 1
        return count
    }


    //hide base :
    function hide(){
        if(orientation === Qt.LeftEdge){
            visible = false
        }
        if(orientation === Qt.RightEdge){
            visible = false
        }
    }

}
