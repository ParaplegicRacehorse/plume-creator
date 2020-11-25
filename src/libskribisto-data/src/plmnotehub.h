/***************************************************************************
*   Copyright (C) 2016 by Cyril Jacquet                                 *
*   cyril.jacquet@skribisto.eu                                        *
*                                                                         *
*  Filename: plmnotehub.h                                                   *
*  This file is part of Skribisto.                                    *
*                                                                         *
*  Skribisto is free software: you can redistribute it and/or modify  *
*  it under the terms of the GNU General Public License as published by   *
*  the Free Software Foundation, either version 3 of the License, or      *
*  (at your option) any later version.                                    *
*                                                                         *
*  Skribisto is distributed in the hope that it will be useful,       *
*  but WITHOUT ANY WARRANTY; without even the implied warranty of         *
*  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          *
*  GNU General Public License for more details.                           *
*                                                                         *
*  You should have received a copy of the GNU General Public License      *
*  along with Skribisto.  If not, see <http://www.gnu.org/licenses/>. *
***************************************************************************/
#ifndef PLMNOTEHUB_H
#define PLMNOTEHUB_H

#include <QObject>
#include "plmpaperhub.h"
#include "skribisto_data_global.h"


class EXPORT PLMNoteHub : public PLMPaperHub {
    Q_OBJECT

public:

    PLMNoteHub(QObject *parent);

    QHash<QString, QVariant>getNoteData(int projectId,
                                        int noteId) const;
    Q_INVOKABLE  SKRResult   addNoteRelatedToSheet(int projectId,
                                                  int sheetId);
    Q_INVOKABLE int         getSynopsisNoteId(int projectId,
                                              int sheetId) const;
    Q_INVOKABLE QList<int>  getNotesFromSheetId(int projectId,
                                                int sheetId) const;
    Q_INVOKABLE QList<int>  getSheetsFromNoteId(int projectId,
                                                int noteId) const;
    Q_INVOKABLE SKRResult    setSheetNoteRelationship(int  projectId,
                                                     int  sheetId,
                                                     int  noteId,
                                                     bool isSynopsis = false);
    Q_INVOKABLE SKRResult removeSheetNoteRelationship(int projectId,
                                                     int sheetId,
                                                     int noteId);

    Q_INVOKABLE int  getSheetFromSynopsisId(int projectId,
                                                int synopsisId) const;
    Q_INVOKABLE  SKRResult      createSynopsis(int projectId,
                                              int sheetId);

    Q_INVOKABLE  int           getSynopsisFolderId(int projectId);
      SKRResult cleanUpSynopsis(int projectId);
    Q_INVOKABLE  bool          isSynopsis(int projectId,
                                          int noteId);

    Q_INVOKABLE  QList<QString>getAttributes(int projectId,
                                             int paperId) override;
    Q_INVOKABLE  bool          hasAttribute(int            projectId,
                                            int            paperId,
                                            const QString& attribute) override;
    Q_INVOKABLE  SKRResult      addAttribute(int            projectId,
                                            int            paperId,
                                            const QString& attribute) override;
    Q_INVOKABLE SKRResult       removeAttribute(int            projectId,
                                               int            paperId,
                                               const QString& attribute) override;

signals:

    void sheetNoteRelationshipChanged(int projectId,
                                      int sheetId,
                                      int noteId);
    void sheetNoteRelationshipRemoved(int projectId,
                                      int sheetId,
                                      int noteId);
    void sheetNoteRelationshipAdded(int projectId,
                                    int sheetId,
                                    int noteId);

private slots:

};

#endif // PLMNOTEHUB_H
