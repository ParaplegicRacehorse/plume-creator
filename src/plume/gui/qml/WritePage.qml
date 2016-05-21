import QtQuick 2.4
import QtQuick.Layouts 1.1

WritePageForm {

    //    function readSettings(){
    //    }

    //    Component.onCompleted: {readSettings()
    //        fillDocks()}



    function init(){
        leftBase.onBaseWidthChanged.connect(changeLeftBaseWidth)
        rightBase.onBaseWidthChanged.connect(changeRightBaseWidth)
    }

    function changeLeftBaseWidth(value){
        if(value < 170)
            value = 170

        leftBase.implicitWidth = value
        leftBase.Layout.maximumWidth = value
        leftBase.Layout.minimumWidth = value
    }
    function changeRightBaseWidth(value){
        if(value < 170)
            value = 170

        rightBase.implicitWidth = value
        rightBase.Layout.maximumWidth = value
        rightBase.Layout.minimumWidth = value
    }






//        Component.onDestruction: {
//            settings.write_left_base_impl_width = leftBase.implicitWidth
//            settings.write_left_base_max_width = leftBase.maximumWidth
//            settings.write_left_base_min_width = leftBase.minimumWidth
//        }




    Component.onCompleted: init()
}
