pragma Singleton
import QtQuick 2.0

QtObject {
    id: signalHub
    signal openSheetInWritePageSignal(int sheet_id)
}
