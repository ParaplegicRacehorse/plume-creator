import QtQuick 2.4

DockForm {
    signal addDockClicked()
    signal closeDockClicked()

    tabView.onCountChanged: populateListModel()

    function populateListModel(){

        function createListElement(tabText, tabIndex) {
            return {
                "text": tabText,
                "index": tabIndex
            };
        }
        dockTitleBar.listModel.clear()
        for (var i = 0; i < tabView.count ; i++) {
            var tabText = tabView.getTab(i).title;
            var tabIndex = i;
            dockTitleBar.listModel.append(createListElement(tabText, tabIndex));
        };
    }
    dockTitleBar.dock_comboBox.onCurrentIndexChanged: tabView.currentIndex = dockTitleBar.listModel.get(dockTitleBar.dock_comboBox.currentIndex).index


    //dockTitleBar.close_toolButton.onClicked: baseItem.visible = false
    dockTitleBar.close_toolButton.onClicked: closeDockClicked()
    dockTitleBar.add_toolButton.onClicked: addDockClicked()
    dockTitleBar.onWidthChanged: dockTitleBar.width = width


}
