import QtQuick 2.0

Item {


        ListModel {
        id: listModel
    ListElement {
        name: "Bill Smith"
        number: "555 3264"
    }
    ListElement {
        name: "John Brown"
        number: "555 8426"
    }
    ListElement {
        name: "Sam Wise"
        number: "555 0473"
    }
}

ListView {
        anchors.fill: parent

    width: 180; height: 200

    model: listModel
    delegate: Text {
        text: name + ": " + number
    }
}

    }


