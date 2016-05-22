import QtQuick 2.4
import "singletons" 1.0

SheetTreePanelForm {
// tree settings :
    sheetTreeView.treeView.onDoubleClicked:  {
        if(index.isValid === true){
            sheet_id = sheetTreeView.treeView.data(index, "sheet_id")
            SignalHub.openSheetInWritePageSignal(sheet_id)
        }
    }
}
