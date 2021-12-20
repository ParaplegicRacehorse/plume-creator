import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../Items"
import "../Commons"
import ".."

Item {

    property alias stackView: stackView

    SkrPane {
        id: pane1
        anchors.fill: parent


        StackView {
            id: stackView

            anchors.fill: parent

            clip: true

        }

    }
}

/*##^##
Designer {
    D{i:0;height:800;width:800}
}
##^##*/

