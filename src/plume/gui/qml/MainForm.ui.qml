import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import QtQuick.Layouts 1.2
import QtQuick.Extras 1.4

Item {
    id: item1
    property alias tab_view: tab_view
    property alias welcome_tab: welcome_tab
    property alias write_tab: write_tab
    anchors.fill: parent

    RowLayout {
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0
        anchors.fill: parent
        spacing: 0
        layoutDirection: Qt.LeftToRight

        Rectangle {
            width: 60
            gradient: Gradient {
                GradientStop { position: 0.0; color: "lightsteelblue" }
                GradientStop { position: 1.0; color: "blue" }
            }
            Layout.fillHeight: true
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0
            anchors.top: parent.top
            anchors.topMargin: 0
            Column {
                spacing: 3
                Repeater {
                    model: tab_view.count
                    Rectangle {
                        width: 60
                        height: 60
                        color: "#00000000"
                        Text {
                            id: icon_tab_text
                            text: tab_view.getTab(index).title
                            font.pointSize: 10
                            anchors.bottom: parent.bottom
                            anchors.bottomMargin: 2
                            anchors.horizontalCenter: parent.horizontalCenter

                        }
                        Image{
                            id: icon_tab_image
                            anchors.margins: 0
                            fillMode: Image.PreserveAspectFit
                            sourceSize.height: 48
                            sourceSize.width: 48
                            source: tab_view.getTab(index).iconSource
                            anchors.horizontalCenter: parent.horizontalCenter
                            anchors.top: parent.top
                            anchors.topMargin: 2
                            anchors.bottom: icon_tab_text.top
                            anchors.bottomMargin: 2
                        }
                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            onClicked: tab_view.currentIndex = index
                        }
                    }
                }
            }
        }

        Item {
            id: item2
            width: 200
            height: 200
            Layout.fillHeight: true
            Layout.fillWidth: true

            TabView {
                id: tab_view
                anchors.fill: parent


                IconTab {
                    id: welcome_tab
                    title: "Welcome"
                    iconSource: "pics/plume-creator.png"
                    WelcomePage {
                        id: welcomePage
                        visible: true
                    }
                }
                IconTab {
                    id: write_tab
                    title: "Write"
                    iconSource: "pics/48x48/scribus.png"
                    WritePage {
                        id: writePage
                        visible: true
                    }
                }

                style: TabViewStyle {
                    tab: Item {}
                }




            }
        }


    }

}
