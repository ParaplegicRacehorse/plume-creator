import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.2
import QtQuick.Controls.Material 2.15
import "../Items"
import ".."
Item {
    width: 400
    height: 400
    property alias projectSwipeView: projectSwipeView
    property alias tabBar: tabBar

    SkrPane{
        anchors.fill: parent

        ColumnLayout {
            id: columnLayout
            anchors.fill: parent

            SkrTabBar {
                id: tabBar
                Layout.fillWidth: true
            }

            SwipeView {
                id: projectSwipeView
                Layout.fillHeight: true
                Layout.fillWidth: true
                interactive: false
                clip: true

            }
        }
    }
}
